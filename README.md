# LangChain Course Projects

A comprehensive collection of LangChain and LangGraph projects demonstrating various AI agent patterns, RAG implementations, and advanced LLM workflows.

## 📚 Projects Overview

### 1. **Hello World** (`hello-world/`)
Basic introduction to LangChain with simple LLM interactions.
- **Key Concepts**: LangChain basics, ChatOpenAI, simple prompts
- **Tech Stack**: LangChain, OpenAI

### 2. **RAG (Retrieval-Augmented Generation)** (`rag/`)
Traditional RAG implementation using vector stores and document retrieval.
- **Key Concepts**: Vector stores, embeddings, document retrieval, RAG chain
- **Tech Stack**: LangChain, Chroma, OpenAI Embeddings

### 3. **RAG with LCEL** (`rag-lcel/`)
Modern RAG implementation using LangChain Expression Language (LCEL).
- **Key Concepts**: LCEL, chain composition, streaming
- **Tech Stack**: LangChain, Chroma, LCEL

### 4. **Documentation Helper** (`documentation-helper/`)
AI-powered documentation assistant with RAG capabilities.
- **Key Concepts**: Document ingestion, semantic search, Q&A
- **Tech Stack**: LangChain, Chroma, FastAPI

### 5. **Search Agent** (`search-agent/`)
Agent that can perform web searches to answer questions.
- **Key Concepts**: Tool use, web search, agent reasoning
- **Tech Stack**: LangChain, Tavily Search

### 6. **Search Agent (Original)** (`search-agent-og/`)
Original implementation of search agent with custom schemas.
- **Key Concepts**: Structured outputs, custom tools, Pydantic schemas
- **Tech Stack**: LangChain, Tavily, Pydantic

### 7. **ReAct Agent Implementation** (`react-agent-impl/`)
Implementation of the ReAct (Reasoning + Acting) pattern.
- **Key Concepts**: ReAct pattern, thought-action-observation loop
- **Tech Stack**: LangChain, custom callbacks

### 8. **ReAct with LangGraph** (`react-langgraph/`)
ReAct agent built using LangGraph for better control flow.
- **Key Concepts**: LangGraph, StateGraph, agent nodes
- **Tech Stack**: LangGraph, LangChain, Tavily

### 9. **Reflection Agent** (`reflection-agent/`)
Agent that reflects on its outputs and iteratively improves them.
- **Key Concepts**: Self-reflection, iterative improvement, critique
- **Tech Stack**: LangGraph, structured outputs

### 10. **Reflexion Agent** (`reflexion-agent/`)
Advanced reflection pattern with search query generation and answer revision.
- **Key Concepts**: Reflexion pattern, search-based improvement, structured outputs
- **Tech Stack**: LangGraph, Tavily, Pydantic

### 11. **Agentic RAG** (`agentic-rag/`) ⭐
Production-ready agentic RAG system with intelligent routing, grading, and validation.
- **Key Concepts**: Agentic RAG, routing, hallucination detection, answer grading
- **Tech Stack**: LangGraph, Chroma, Tavily, comprehensive logging
- **Features**:
  - Intelligent question routing (vectorstore vs web search)
  - Document relevance grading
  - Hallucination detection
  - Answer quality validation
  - Structured logging system
  - Full test suite

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI API key
- Tavily API key (for search agents)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/aroy1856/langchain-course.git
   cd langchain-course
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

3. **Navigate to a project**
   ```bash
   cd agentic-rag  # or any other project
   ```

4. **Install dependencies**
   ```bash
   uv sync
   ```

5. **Run the project**
   ```bash
   uv run python main.py
   ```

## 🧪 Running Tests

Most projects include test suites. To run tests:

```bash
cd <project-directory>
uv run pytest . -s -v
```

## 📖 Learning Path

Recommended order for learning:

1. **hello-world** - Understand LangChain basics
2. **rag** - Learn traditional RAG
3. **rag-lcel** - Modern LCEL approach
4. **search-agent** - Introduction to agents and tools
5. **react-agent-impl** - ReAct pattern fundamentals
6. **react-langgraph** - LangGraph basics
7. **reflection-agent** - Self-improvement patterns
8. **reflexion-agent** - Advanced reflection with search
9. **agentic-rag** - Production-ready agentic system

## 🛠️ Tech Stack

- **LangChain** - LLM application framework
- **LangGraph** - Graph-based agent orchestration
- **OpenAI** - LLM provider
- **Chroma** - Vector database
- **Tavily** - Web search API
- **Pydantic** - Data validation
- **pytest** - Testing framework
- **uv** - Fast Python package manager

## 📝 Project Structure

Each project follows a consistent structure:
```
project-name/
├── .python-version    # Python version specification
├── pyproject.toml     # Project dependencies
├── uv.lock           # Locked dependencies
├── README.md         # Project documentation
├── main.py           # Entry point
└── ...               # Project-specific files
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🔗 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI API](https://platform.openai.com/docs/)
- [Tavily Search API](https://tavily.com/)

## 👤 Author

**Abhishek Roy**
- GitHub: [@aroy1856](https://github.com/aroy1856)
