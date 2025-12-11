from dotenv import load_dotenv
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode

from react import tools, llm

load_dotenv()

SYSTEM_PROMPT = """
You are a helpful assistant that can answer questions using the available tools.
"""

def run_agent_reasoning(state: MessagesState) -> MessagesState:
    """
    Run the agent reasoning Node.
    """
    response = llm.invoke([{"role": "system", "content": SYSTEM_PROMPT}, *state["messages"]])
    return {"messages": [response]}

tool_node = ToolNode(tools)