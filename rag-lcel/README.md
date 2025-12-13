# RAG with LCEL

Modern RAG implementation using LangChain Expression Language (LCEL).

## 🎯 What is LCEL?

LCEL (LangChain Expression Language) is a declarative way to compose chains:
- **Pipeable** - Use `|` operator to chain components
- **Streamable** - Built-in streaming support
- **Async-ready** - Native async/await support
- **Optimized** - Automatic batching and parallelization

## 🚀 Quick Start

```bash
cd rag-lcel
uv sync

# Ingest documents
uv run python ingestion.py

# Run RAG with LCEL
uv run python main.py
```

## 🔧 LCEL Syntax

```python
# Traditional approach
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(input)

# LCEL approach
chain = prompt | llm | output_parser
result = chain.invoke(input)
```

## ✨ Benefits of LCEL

- **Cleaner code** - More readable chain composition
- **Better streaming** - Stream intermediate results
- **Type safety** - Better IDE support
- **Debugging** - Easier to inspect chain steps

## 📚 Learn More

- [LCEL Documentation](https://python.langchain.com/docs/expression_language/)
- [LCEL Cookbook](https://python.langchain.com/docs/expression_language/cookbook/)

## 🎓 Next Steps

- **agentic-rag** - Production-ready RAG with advanced features
