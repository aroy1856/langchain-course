from typing import Any, Dict

from graph.chains.retrieval_grader import grader_chain
from graph.state import GraphState
from logger import get_logger

logger = get_logger("nodes.grade_documents")


def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """
    logger.info("Grading document relevance")
    question = state["question"]
    retrieved_docs = state["documents"]

    graded_docs = []
    web_search = False
    for doc in retrieved_docs:
        graded_doc = grader_chain.invoke(
            {"question": question, "document": doc.page_content}
        )
        if graded_doc.binary_score.lower() == "yes":
            graded_docs.append(doc)
            logger.debug(f"Document graded as relevant")
        else:
            web_search = True
            logger.debug(f"Document graded as irrelevant, will trigger web search")
            continue

    logger.info(
        f"Grading complete: {len(graded_docs)}/{len(retrieved_docs)} documents relevant, web_search={web_search}"
    )
    return {"documents": graded_docs, "question": question, "web_search": web_search}
