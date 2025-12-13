# Documentation Helper

AI-powered documentation assistant with RAG capabilities for answering questions about your documentation.

## 🎯 Features

- **Document Ingestion** - Load and process documentation
- **Semantic Search** - Find relevant information quickly
- **Q&A Interface** - Ask questions in natural language
- **Context-Aware** - Provides answers based on your docs

## 🚀 Quick Start

```bash
cd documentation-helper
uv sync

# Ingest your documentation
uv run python ingestion.py

# Run the assistant
uv run python main.py
```

## 📁 Project Structure

- `backend/` - Core RAG logic
  - `core.py` - RAG chain implementation
- `ingestion.py` - Document loading and processing
- `logger.py` - Logging configuration
- `main.py` - Main application

## 🔧 Customization

### Add Your Documentation

Edit `ingestion.py` to point to your documentation:
```python
# Load from URLs
loader = WebBaseLoader("https://your-docs.com")

# Or load from files
loader = DirectoryLoader("./docs")
```

### Adjust Chunk Size

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Adjust based on your needs
    chunk_overlap=200
)
```

## 📚 Use Cases

- Internal documentation Q&A
- API reference assistant
- Knowledge base search
- Technical support automation

## 🎓 Next Steps

- **rag-lcel** - Learn modern LCEL patterns
- **agentic-rag** - Add intelligent routing and grading
