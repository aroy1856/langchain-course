# ReAct Agent Implementation

Implementation of the ReAct (Reasoning + Acting) pattern with custom callbacks.

## 🎯 What is ReAct?

ReAct is an agent framework that interleaves:
- **Thought** - Reasoning about what to do
- **Action** - Executing a tool
- **Observation** - Processing the result

## 🔄 ReAct Loop

```
Thought: I need to search for information
Action: tavily_search
Action Input: "query here"
Observation: [search results]
Thought: Based on the results, I can answer
Final Answer: [answer]
```

## 🚀 Quick Start

```bash
cd react-agent-impl
uv sync
uv run python main.py
```

## 📁 Key Files

- `callbacks.py` - Custom callbacks for observability
- `main.py` - ReAct agent implementation

## ✨ Features

- **Custom Callbacks** - Track agent reasoning
- **Tool Integration** - Web search capabilities
- **Transparent Reasoning** - See agent's thought process

## 📚 Learn More

- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [LangChain Callbacks](https://python.langchain.com/docs/modules/callbacks/)

## 🎓 Next Steps

- **react-langgraph** - More control with LangGraph
- **reflection-agent** - Add self-reflection
