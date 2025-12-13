# Reflexion Agent

Advanced reflection pattern with search query generation and answer revision.

## 🎯 What is Reflexion?

Reflexion is an agent pattern that:
1. **Generates** an initial answer
2. **Reflects** on what's missing or superfluous
3. **Searches** for information to improve
4. **Revises** the answer with new information

## 🔄 Workflow

```
Question → Draft Answer → Reflect → Generate Search Queries
    ↓
Search → Gather Results → Revise Answer → Final Answer
```

## 🚀 Quick Start

```bash
cd reflexion-agent
uv sync
uv run python main.py
```

## 🔧 Key Components

- `schemas.py` - Pydantic models for structured outputs
  - `Reflection` - Critique structure
  - `AnswerQuestion` - Initial answer with reflection
  - `ReviseAnswer` - Revised answer with references
- `chains.py` - LLM chains for generation and revision
- `main.py` - StateGraph implementation

## ✨ Features

- **Structured Outputs** - Uses Pydantic for type safety
- **Iterative Improvement** - Multiple revision cycles
- **Search Integration** - Tavily search for information gathering
- **Citations** - Includes references in final answer

## 📚 Learn More

- [Reflexion Paper](https://arxiv.org/abs/2303.11366)
- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)

## 🎓 Next Steps

- **agentic-rag** - Combine reflexion with RAG and grading
