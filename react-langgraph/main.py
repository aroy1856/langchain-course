from dotenv import load_dotenv
from langgraph.graph import StateGraph, END, MessagesState
from langchain.messages import HumanMessage

from nodes import run_agent_reasoning, tool_node

load_dotenv()

AGENT_REASONING = "agent_reason"
LAST = -1
ACT = "act"

def should_continiue(state: MessagesState) -> str:
    return ACT if state["messages"][LAST].tool_calls else END

flow = StateGraph(MessagesState)

flow.add_node(AGENT_REASONING, run_agent_reasoning)
flow.add_node(ACT, tool_node)

flow.set_entry_point(AGENT_REASONING)

flow.add_conditional_edges(AGENT_REASONING, should_continiue, {
    ACT:ACT,
    END:END,
})
flow.add_edge(ACT, AGENT_REASONING)

if __name__ == "__main__":
    graph = flow.compile()
    # graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

    res = graph.invoke({"messages": [HumanMessage(content="What is the temperature in New York today? List it and then triple it")]} )
    
    print(res["messages"][LAST].content)
