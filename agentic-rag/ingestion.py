from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

documents = [WebBaseLoader(url).load() for url in urls]
docs = [subitem for sublist in documents for subitem in sublist]

text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=0)
splitted_docs = text_splitter.split_documents(docs)

embeddings = OpenAIEmbeddings()

# # Run this once to create the vector database
# vectorstore = Chroma.from_documents(
#     documents=splitted_docs,
#     embedding=embeddings,
#     persist_directory="./chroma_db",
#     collection_name="agentic-rag-chroma",
# )

retriever = Chroma(
    collection_name="agentic-rag-chroma",
    persist_directory="./chroma_db",
    embedding_function=embeddings,
).as_retriever()
