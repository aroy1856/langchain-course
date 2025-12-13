# Search Agent (Original)

Original implementation of search agent with custom Pydantic schemas and structured outputs.

## 🎯 Key Features

- **Structured Outputs** - Custom Pydantic schemas for type safety
- **Tool Integration** - Tavily search with structured results
- **Schema Validation** - Ensures correct data formats

## 🚀 Quick Start

```bash
cd search-agent-og
uv sync
uv run python main.py
```

## 📁 Key Files

- `schema.py` - Pydantic models for structured outputs
- `prompt.py` - Custom prompts for the agent
- `main.py` - Agent implementation

## 🔧 Structured Outputs

Uses Pydantic models to ensure:
- Type safety
- Data validation
- Clear interfaces
- Better debugging

## 📚 Learn More

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)

## 🎓 Next Steps

- **reflexion-agent** - Advanced patterns with structured outputs
- **agentic-rag** - Production system with comprehensive schemas
