from langgraph.prebuilt.tool_node import ToolNode
from typing import Annotated
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, ToolMessage, AIMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from chains import first_responder, revisor, search_tool
from typing_extensions import TypedDict

load_dotenv()

MAX_ITERATIONS = 2

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def draft_node(state: State):
    response = first_responder.invoke({"messages": state["messages"]})
    # Convert structured output to AIMessage with tool_calls
    tool_calls = [{
        "name": "tavily_search",
        "args": {"query": query},
        "id": f"call_{i}"
    } for i, query in enumerate(response.search_queries)]
    
    return {"messages": [AIMessage(
        content=f"Draft Answer:\n{response.answer}\n\nReflection:\n- Missing: {response.reflection.missing}\n- Superfluous: {response.reflection.superfluous}",
        tool_calls=tool_calls
    )]}


def revise_node(state: State):
    response = revisor.invoke({"messages": state["messages"]})
    # Check if there are more queries to run
    if response.search_queries:
        tool_calls = [{
            "name": "tavily_search",
            "args": {"query": query},
            "id": f"call_rev_{i}"
        } for i, query in enumerate(response.search_queries)]
        
        return {"messages": [AIMessage(
            content=f"Revised Answer:\n{response.answer}\n\nReferences:\n" + "\n".join(response.references),
            tool_calls=tool_calls
        )]}
    else:
        # No more queries, just return the final answer
        return {"messages": [AIMessage(
            content=f"Final Answer:\n{response.answer}\n\nReferences:\n" + "\n".join(response.references)
        )]}


def execute_tools_node(state: State):
    tool_node = ToolNode([search_tool])
    return tool_node.invoke(state)

def should_continue_draft(state: State) -> str:
    last_msg = state["messages"][-1]
    if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
        return "tools"
    return "revise"

def should_continue_revise(state: State) -> str:
    last_msg = state["messages"][-1]
    # Count how many tool executions we've done
    tool_count = sum(1 for msg in state["messages"] if isinstance(msg, ToolMessage))
    
    # If we've exceeded max iterations, stop
    if tool_count >= MAX_ITERATIONS:
        return END
    
    # If LLM made tool calls, execute them
    if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
        return "tools"
    
    # No more tool calls and haven't exceeded limit, we're done
    return END

builder = StateGraph(State)

builder.add_node("draft", draft_node)
builder.add_node("tools", execute_tools_node)
builder.add_node("revise", revise_node)

builder.add_conditional_edges("draft", "tools")
builder.add_edge("tools", "revise")
builder.add_conditional_edges("revise", should_continue_revise, {"tools": "tools", END: END})

builder.set_entry_point("draft")

if __name__ == "__main__":
    from langchain_core.messages import HumanMessage
    
    graph = builder.compile()
    
    res = graph.invoke({
        "messages": [HumanMessage(content="Write about AI-Powered SOC / autonomous soc problem domain, list startups that do that and raised capital.")]
    })
    
    print("=== Final Answer ===")
    print(res["messages"][-1].content)
    
    print("\n=== Message Flow ===")
    for i, msg in enumerate(res["messages"]):
        msg_type = msg.__class__.__name__
        content_preview = msg.content[:150] if msg.content else "[tool_calls]"
        print(f"{i+1}. {msg_type}: {content_preview}...")