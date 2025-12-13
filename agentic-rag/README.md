# Agentic RAG

A production-ready agentic Retrieval-Augmented Generation (RAG) system built with LangGraph. Features intelligent routing, document grading, hallucination detection, and comprehensive logging.

## 🌟 Features

### Core Capabilities
- **Intelligent Question Routing** - Automatically routes questions to vectorstore or web search based on content
- **Document Relevance Grading** - Filters out irrelevant documents before generation
- **Hallucination Detection** - Validates that generated answers are grounded in source documents
- **Answer Quality Grading** - Ensures answers actually address the user's question
- **Web Search Fallback** - Falls back to web search when vectorstore documents are insufficient
- **Iterative Refinement** - Regenerates answers if quality checks fail

### Technical Features
- **Structured Logging** - Console and file logging with appropriate log levels
- **Comprehensive Test Suite** - Tests for all graders and routing logic
- **Graph Visualization** - Mermaid diagram of the workflow
- **Type Safety** - Full type hints with Pydantic models
- **Modular Architecture** - Clean separation of concerns

## 🏗️ Architecture

```
┌─────────────┐
│   Question  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Question Router │ ◄── Routes to vectorstore or web search
└────┬────────┬───┘
     │        │
     ▼        ▼
┌─────────┐  ┌──────────┐
│Retrieve │  │Web Search│
└────┬────┘  └────┬─────┘
     │            │
     ▼            │
┌──────────────┐  │
│Grade Documents│  │
└────┬─────────┘  │
     │            │
     ▼            ▼
┌─────────────────┐
│    Generate     │ ◄── RAG generation
└────┬────────────┘
     │
     ▼
┌──────────────────┐
│ Grade Generation │ ◄── Hallucination + Answer quality check
└────┬─────────────┘
     │
     ├─► Useful → END
     ├─► Not Useful → Web Search
     └─► Not Supported → Regenerate
```

## 📁 Project Structure

```
agentic-rag/
├── graph/
│   ├── chains/              # LLM chains and graders
│   │   ├── answer_grader.py       # Answer quality grading
│   │   ├── generation.py          # RAG generation chain
│   │   ├── hallucination_grader.py # Hallucination detection
│   │   ├── retrieval_grader.py    # Document relevance grading
│   │   ├── router.py              # Question routing
│   │   └── tests/
│   │       └── test_chains.py     # Chain tests
│   ├── nodes/               # Graph nodes
│   │   ├── generate.py            # Generation node
│   │   ├── grade_documents.py     # Document grading node
│   │   ├── retrieve.py            # Retrieval node
│   │   └── web_search.py          # Web search node
│   ├── consts.py            # Constants
│   ├── graph.py             # Main graph definition
│   └── state.py             # Graph state schema
├── chroma_db/               # Vector database (persisted)
├── logs/                    # Application logs
├── ingestion.py             # Document ingestion
├── logger.py                # Logging configuration
├── main.py                  # Entry point
├── pyproject.toml           # Dependencies
└── README.md                # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- OpenAI API key
- Tavily API key

### Installation

1. **Navigate to project directory**
   ```bash
   cd agentic-rag
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the parent directory with:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

4. **Run ingestion (first time only)**
   ```bash
   uv run python ingestion.py
   ```
   This creates the vector database from the configured URLs.

### Usage

```bash
uv run python main.py
```

The system will:
1. Route your question to vectorstore or web search
2. Retrieve/search for relevant information
3. Grade document relevance
4. Generate an answer
5. Validate the answer for hallucinations and quality
6. Retry with web search or regeneration if needed

## 🧪 Running Tests

```bash
# Run all tests
uv run pytest . -s -v

# Run specific test file
uv run pytest graph/chains/tests/test_chains.py -v

# Run with coverage
uv run pytest --cov=graph --cov-report=html
```

### Test Coverage
- ✅ Retrieval grader (yes/no scenarios)
- ✅ Hallucination grader (grounded/not grounded)
- ✅ Answer grader (addresses/doesn't address question)
- ✅ Question router (vectorstore/websearch routing)

## 📊 Logging

The system uses structured logging with two handlers:

- **Console** (INFO level) - Important events and decisions
- **File** (DEBUG level) - Detailed execution logs in `logs/agentic_rag.log`

Example log output:
```
2025-12-13 15:27:39 - agentic_rag.graph - INFO - Routing question to: websearch
2025-12-13 15:27:39 - agentic_rag.nodes.web_search - INFO - Performing web search
2025-12-13 15:27:40 - agentic_rag.nodes.generate - INFO - Generating response using RAG chain
2025-12-13 15:27:42 - agentic_rag.graph - INFO - DECISION: Generation addresses question - USEFUL
```

## 🔧 Configuration

### Modifying Vector Store Sources

Edit `ingestion.py` to change the URLs:
```python
urls = [
    "https://your-url-1.com",
    "https://your-url-2.com",
]
```

Then re-run ingestion:
```bash
uv run python ingestion.py
```

### Adjusting LLM Models

Edit the chain files in `graph/chains/`:
```python
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
```

### Tuning Parameters

- **Chunk size**: `ingestion.py` - `chunk_size=250`
- **Max iterations**: `graph/graph.py` - Not currently limited
- **Search results**: `graph/nodes/web_search.py` - `max_results=3`

## 🎯 Key Concepts

### Agentic RAG
Unlike traditional RAG, this system makes intelligent decisions:
- Routes questions based on content
- Validates document relevance
- Detects hallucinations
- Ensures answer quality
- Iteratively improves outputs

### Grading System
Three-tier validation:
1. **Document Grading** - Are retrieved docs relevant?
2. **Hallucination Grading** - Is answer grounded in docs?
3. **Answer Grading** - Does answer address the question?

### Routing Logic
- **Vectorstore** - Questions about agents, prompt engineering, adversarial attacks
- **Web Search** - Everything else (current events, general knowledge)

## 🐛 Troubleshooting

### Vector database is empty
Run the ingestion script:
```bash
uv run python ingestion.py
```

### API key errors
Ensure `.env` file exists in parent directory with valid keys.

### Import errors
Make sure you're running from the `agentic-rag` directory:
```bash
cd agentic-rag
uv run python main.py
```

## 📚 Learn More

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Agentic RAG Pattern](https://blog.langchain.dev/agentic-rag/)
- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional grading criteria
- More sophisticated routing logic
- Support for multiple vector stores
- Streaming responses
- Conversation memory

## 📄 License

MIT License
