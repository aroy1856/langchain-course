from joblib.externals.loky.process_executor import MAX_DEPTH
import asyncio
import os
import ssl
from typing import List, Any, Dict
import certifi
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from langchain_tavily import TavilyCrawl, TavilyExtract, TavilyMap

from logger import log_info, log_success, log_error, log_warning, log_header, Colors

load_dotenv()

ssl_context = ssl.create_default_context(cafile=certifi.where())
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large", 
    dimensions=1024,
    show_progress_bar=True, 
    chunk_size=50, 
    retry_min_seconds=10
)
vectorestore = PineconeVectorStore(
    index_name=os.getenv("PINECONE_INDEX_NAME"),
    embedding=embeddings
)
tavily_extract = TavilyExtract()
tavily_map = TavilyMap(max_depth=5, max_breadth=20, max_pages=1000)
tavily_crawl = TavilyCrawl()

async def index_documents_async(documents: List[Document], batch_size: int = 50):
    """Process documents in batches asynchronously."""
    log_header("VECTOR STORAGE PHASE")
    log_info(
        f"📚 VectorStore Indexing: Preparing to add {len(documents)} documents to vector store",
        Colors.DARKCYAN,
    )

    # create batches
    batches = [documents[i:i + batch_size] for i in range(0, len(documents), batch_size)]
    log_info(
        f"📚 VectorStore Indexing: Preparing to add {len(documents)} documents to vector store",
        Colors.DARKCYAN,
    )

    async def add_batch(batch: List[Document], batch_num: int):
        try:
            await vectorestore.aadd_documents(batch)
            log_success(
                f"📚 VectorStore Indexing: Successfully added batch {batch_num} to vector store",
            )
        except Exception as e:
            log_error(
                f"📚 VectorStore Indexing: Failed to add batch {batch_num} to vector store",
            )
            return False
        return True
    
    #process batches
    tasks = [add_batch(batch, i+1) for i, batch in enumerate(batches)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # count successfull batches
    success_count = sum(1 for result in results if result)
    
    if success_count == len(results):
        log_success(
            f"📚 VectorStore Indexing: Successfully added {success_count} batches to vector store",
        )
    else:
        log_warning(
            f"📚 VectorStore Indexing: Failed to add {len(results) - success_count} batches to vector store",
        )

async def main():
    """Main async function to orchestrate the entire process."""
    log_header("DOCUMENTATION INGESTION PIPELINE")

    log_info(
        "🗺️  TavilyCrawl: Starting to crawl the documentation site",
        Colors.PURPLE,
    )
    # Crawl the documentation site
    res = await tavily_crawl.ainvoke({
        "url": "https://python.langchain.com/",
        "max_depth": 5,
        "extract_depth": "advanced"
    })
    all_docs = [
        Document(page_content=result['raw_content'], metadata={"source": result['url']}) 
        for result in res['results'] 
        if result.get('raw_content')
    ]

    log_success(f"🗺️  TavilyCrawl: Successfully crawled {len(all_docs)} pages from the documentation site")

    log_header("DOCUMENT CHUNKING PIPELINE")
    log_info(
        f"✂️  Text Splitter: Processing {len(all_docs)} documents with 2000 chunk size and 200 overlap",
        Colors.YELLOW,
    )
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    splitted_docs = text_splitter.split_documents(all_docs)

    log_success(f"✂️  Text Splitter: Successfully split {len(all_docs)} documents into {len(splitted_docs)} chunks")

    await index_documents_async(splitted_docs, batch_size=50)

    log_header("PIPELINE COMPLETE")
    log_success("🎉 Documentation ingestion pipeline finished successfully!")
    log_info("📊 Summary:", Colors.BOLD)
    log_info(f"   • Documents extracted: {len(all_docs)}")
    log_info(f"   • Chunks created: {len(splitted_docs)}")


if __name__ == "__main__":
    asyncio.run(main())