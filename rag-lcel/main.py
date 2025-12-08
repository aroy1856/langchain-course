import os
from dotenv import load_dotenv
from ingestion import DocumentIngestion
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
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

def format_docs(docs):
    return "\n".join([doc.page_content for doc in docs])


if __name__ == "__main__":
    # main()
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    vector_store = PineconeVectorStore(
        index_name=os.getenv("PINECONE_INDEX_NAME"),
        embedding=embeddings
    )
    
    template = """Answer the question based only on the following context:
        {context}

        Question: {question}

        Answer:
    """

    prompt_template = ChatPromptTemplate.from_template(template)

    rag_chain = (
        {
            "context": vector_store.as_retriever() | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt_template
        | llm
    )

    query = "What is Pinecone in machine learning?"
    result = rag_chain.invoke(query)
    print(f"\nQuestion: {query}")
    print(f"\nAnswer: {result}")

