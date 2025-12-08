import os
from typing import List
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document

load_dotenv()


class DocumentIngestion:
    """Handles document loading, splitting, and ingestion into Pinecone vector store."""
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 100,
        embedding_model: str = "text-embedding-3-small",
        embedding_dimensions: int = 1024
    ):
        """
        Initialize the document ingestion pipeline.
        
        Args:
            chunk_size: Maximum size of each text chunk
            chunk_overlap: Number of characters to overlap between chunks
            embedding_model: OpenAI embedding model to use
            embedding_dimensions: Dimension of the embedding vectors
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.embeddings = OpenAIEmbeddings(
            model=embedding_model,
            dimensions=embedding_dimensions
        )
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
        
    def load_document(self, file_path: str) -> List[Document]:
        """
        Load a document from a file path.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            List of Document objects
        """
        loader = TextLoader(file_path)
        documents = loader.load()
        print(f"Loaded {len(documents)} document(s) from {file_path}")
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks.
        
        Args:
            documents: List of documents to split
            
        Returns:
            List of split document chunks
        """
        texts = self.text_splitter.split_documents(documents)
        print(f"Split into {len(texts)} chunks")
        return texts
    
    def ingest_to_pinecone(self, texts: List[Document]) -> PineconeVectorStore:
        """
        Ingest document chunks into Pinecone vector store.
        
        Args:
            texts: List of document chunks to ingest
            
        Returns:
            PineconeVectorStore instance
        """
        print(f"Ingesting {len(texts)} chunks to Pinecone index: {self.index_name}")
        vector_store = PineconeVectorStore.from_documents(
            texts,
            self.embeddings,
            index_name=self.index_name
        )
        print("Successfully ingested documents to Pinecone!")
        return vector_store
    
    def ingest_file(self, file_path: str) -> PineconeVectorStore:
        """
        Complete ingestion pipeline: load, split, and ingest a file.
        
        Args:
            file_path: Path to the file to ingest
            
        Returns:
            PineconeVectorStore instance
        """
        print(f"Starting ingestion pipeline for: {file_path}")
        documents = self.load_document(file_path)
        texts = self.split_documents(documents)
        vector_store = self.ingest_to_pinecone(texts)
        return vector_store


if __name__ == "__main__":
    # Example usage
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'mediumblog1.txt')
    
    ingestion = DocumentIngestion()
    ingestion.ingest_file(file_path)
