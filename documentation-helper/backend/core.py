from typing import Dict, List
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_history_aware_retriever
from langchain_classic import hub

load_dotenv()

def run_llm(query: str, chat_history: List[Dict[str, str]] = []):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large", 
        dimensions=1024,
        show_progress_bar=True, 
        chunk_size=50, 
        retry_min_seconds=10
    )
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    vector_store = PineconeVectorStore(
        index_name=os.getenv("PINECONE_INDEX_NAME"),
        embedding=embeddings
    )
    
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

    stuff_documents_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)

    history_aware_retriever = create_history_aware_retriever(   
        llm=llm, retriever=vector_store.as_retriever(), prompt=rephrase_prompt
    )
    qa = create_retrieval_chain(
        retriever=history_aware_retriever, 
        combine_docs_chain=stuff_documents_chain
    )
    
    result = qa.invoke(input={"input": query, "chat_history": chat_history})
    new_result = {
        "query": query,
        "result": result["answer"],
        "source_documents": result["context"],
        "chat_history": result["chat_history"]
    }
    return new_result

if __name__ == "__main__":
    print(run_llm("What is the langchain?"))
    