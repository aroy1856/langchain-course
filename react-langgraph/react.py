from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_tavily import TavilySearch

load_dotenv()

@tool
def triple(num: float) -> float:
    """
    triple a number.
    
    Args:
        num (float): The number to triple.
    
    Returns:
        float: The triple of the input number.
    """
    return num * 3

tools = [triple, TavilySearch(max_results=1)]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)