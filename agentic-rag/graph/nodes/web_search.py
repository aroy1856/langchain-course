from typing import Any, Dict

from dotenv import load_dotenv
from langchain_core.documents.base import Document
from langchain_tavily import TavilySearch

from graph.state import GraphState
from logger import get_logger

load_dotenv()

logger = get_logger("nodes.web_search")
web_search_tool = TavilySearch(max_results=3)


def web_search(state: GraphState) -> Dict[str, Any]:
    """
    Performs a web search to find relevant documents.
    """
    logger.info("Performing web search")
    question = state["question"]

    if "documents" in state:
        documents = state["documents"]
    else:
        documents = None

    result = web_search_tool.invoke(question)["results"]
    combined_docs = "\n".join(res["content"] for res in result)
    logger.debug(f"Web search returned {len(result)} results")

    web_result = Document(page_content=combined_docs)
    if documents is not None:
        documents.append(web_result)
    else:
        documents = [web_result]
    return {"documents": documents, "question": question}
