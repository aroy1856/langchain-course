from dotenv import load_dotenv
from langgraph.graph import END, StateGraph

from graph.chains.answer_grader import answer_grader
from graph.chains.hallucination_grader import hallucination_grader
from graph.chains.router import question_router
from graph.consts import GENERATE, GRADE_DOCUMENTS, RETRIEVE, WEBSEARCH
from graph.nodes import generate, grade_documents, retrieve, web_search
from graph.state import GraphState
from logger import get_logger

load_dotenv()

logger = get_logger("graph")


def decides_to_generate(state: GraphState) -> str:
    decision = WEBSEARCH if state["web_search"] else GENERATE
    logger.info(f"Routing decision: {'web search' if state['web_search'] else 'generate'}")
    return decision


def grade_generation_grounded_in_documents_and_question(state: GraphState) -> str:
    logger.info("Checking hallucinations and answer quality")
    question = state["question"]
    generation = state["generation"]
    documents = state["documents"]

    score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation, "question": question}
    )
    hallucination_score = score.binary_score.lower() == "yes"

    if hallucination_score:
        logger.info("DECISION: Generation is grounded in documents")
        logger.info("Grading generation vs question")
        score = answer_grader.invoke({"question": question, "generation": generation})
        answer_score = score.binary_score.lower() == "yes"
        if answer_score:
            logger.info("DECISION: Generation addresses question - USEFUL")
            return "useful"
        else:
            logger.warning("DECISION: Generation does not address question - NOT USEFUL")
            return "not useful"
    else:
        logger.warning("DECISION: Generation is not grounded in documents - RETRY")
        return "not supported"


def route_question(state: GraphState) -> str:
    res = question_router.invoke({"question": state["question"]})
    decision = RETRIEVE if res.datasource == "vectorstore" else WEBSEARCH
    logger.info(f"Routing question to: {res.datasource}")
    return decision


workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)

workflow.set_conditional_entry_point(
    route_question,
    {
        RETRIEVE: RETRIEVE,
        WEBSEARCH: WEBSEARCH,
    },
)
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decides_to_generate,
    {
        GENERATE: GENERATE,
        WEBSEARCH: WEBSEARCH,
    },
)
workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documents_and_question,
    {
        "useful": END,
        "not useful": WEBSEARCH,
        "not supported": GENERATE,
    },
)
workflow.add_edge(WEBSEARCH, GENERATE)
workflow.add_edge(GENERATE, END)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")
