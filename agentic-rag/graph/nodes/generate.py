from typing import Any, Dict

from graph.chains.generation import generation_chain
from graph.state import GraphState
from logger import get_logger

logger = get_logger("nodes.generate")


def generate(state: GraphState) -> Dict[str, Any]:
    """
    Generates a response to the question using the generation chain.
    """
    logger.info("Generating response using RAG chain")
    question = state["question"]
    retrieved_docs = state["documents"]

    response = generation_chain.invoke(
        {"question": question, "context": retrieved_docs}
    )
    logger.debug(f"Generated response length: {len(response)} characters")

    return {"generation": response, "question": question, "documents": retrieved_docs}
