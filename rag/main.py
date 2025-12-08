import os
from dotenv import load_dotenv
from ingestion import DocumentIngestion
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_classic import hub
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import PromptTemplate
from langchain_pinecone import PineconeVectorStore


load_dotenv()


def main():
    """Main entry point for the RAG application."""
    # Get the file path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'mediumblog1.txt')
    
    # Create ingestion instance and ingest the document
    ingestion = DocumentIngestion(
        chunk_size=1000,
        chunk_overlap=100,
        embedding_model="text-embedding-3-small",
        embedding_dimensions=1024
    )
    
    # Ingest the file
    vector_store = ingestion.ingest_file(file_path)
    print("Ingestion complete!")


if __name__ == "__main__":
    # main()
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    vector_store = PineconeVectorStore(
        index_name=os.getenv("PINECONE_INDEX_NAME"),
        embedding=embeddings
    )
    
    retrival_qa_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_documents_chain = create_stuff_documents_chain(llm, retrival_qa_prompt)
    retrieval_chain = create_retrieval_chain(vector_store.as_retriever(), combine_documents_chain)

    query = "what is Pinecone in machine learning?"
    result = retrieval_chain.invoke(input={"input": query})
    print(result)