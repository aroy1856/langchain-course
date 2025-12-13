from typing import Any, Dict

from graph.state import GraphState
from ingestion import retriever
from logger import get_logger

logger = get_logger("nodes.retrieve")


def retrieve(state: GraphState) -> Dict[str, Any]:
    """
    Retrieve documents from the vector store.
    """
    logger.info("Retrieving documents from vector store")
    question = state["question"]
    retrieved_docs = retriever.invoke(question)
    logger.debug(f"Retrieved {len(retrieved_docs)} documents for question: {question}")
    return {"documents": retrieved_docs, "question": question}
