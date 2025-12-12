from langgraph.graph.state import StateGraph, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage

from chains import reflection_chain, generation_chain

load_dotenv()


class MessagesGraph(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    
REFLECT = 'reflect'
GENERATE = 'generate'

def generation_node(state: MessagesGraph):
    return {"messages": [generation_chain.invoke({"messages": state["messages"]})]}

def reflection_node(state: MessagesGraph):
    ref = reflection_chain.invoke({"messages": state["messages"]})
    return {"messages": [HumanMessage(content=ref.content)]}

def should_continue(state: MessagesGraph):
    return END if len(state["messages"]) > 6 else REFLECT

builder = StateGraph(MessagesGraph)
builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_node)

builder.set_entry_point(GENERATE)

builder.add_edge(REFLECT, GENERATE)
builder.add_conditional_edges(GENERATE, should_continue, {END: END, REFLECT: REFLECT})


if __name__ == "__main__":
    graph = builder.compile()

    inputs = {
        "messages": [
            HumanMessage(
                content="""Make this tweet better:
                                    @LangChainAI
                        — newly Tool Calling feature is seriously underrated.
                        After a long wait, it's  here- making the implementatqion of agents across different models with function calling - super easy.
                        Made a video covering their newest blog post
                    """
            )
        ]
    }
    response = graph.invoke(inputs)
    print(response)
    
