# RAG (Retrieval-Augmented Generation)

Traditional RAG implementation using vector stores and document retrieval.

## 🎯 What is RAG?

RAG combines retrieval and generation to answer questions based on your own documents:
1. **Retrieve** relevant documents from a vector store
2. **Augment** the prompt with retrieved context
3. **Generate** an answer using the LLM

## 🚀 Quick Start

```bash
cd rag
uv sync

# First time: ingest documents
uv run python ingestion.py

# Run the RAG system
uv run python main.py
```

## 📁 Key Files

- `ingestion.py` - Loads documents and creates vector store
- `main.py` - RAG chain implementation
- `mediumblog1.txt` - Sample document

## 🔧 How It Works

1. **Document Loading** - Loads text from `mediumblog1.txt`
2. **Text Splitting** - Chunks document into smaller pieces
3. **Embedding** - Creates vector embeddings using OpenAI
4. **Storage** - Stores in Chroma vector database
5. **Retrieval** - Finds relevant chunks for questions
6. **Generation** - LLM generates answers using retrieved context

## 📚 Learn More

- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [Vector Stores](https://python.langchain.com/docs/integrations/vectorstores/)

## 🎓 Next Steps

- **rag-lcel** - Modern RAG with LCEL
- **agentic-rag** - Advanced RAG with routing and grading
