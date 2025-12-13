# ReAct Agent with LangGraph

ReAct (Reasoning + Acting) agent built using LangGraph for better control flow.

## 🎯 What is ReAct?

ReAct is an agent pattern that combines:
- **Reasoning** - Think about what to do
- **Acting** - Execute actions using tools
- **Observing** - Process results and continue

## 🏗️ Why LangGraph?

LangGraph provides:
- **Explicit control flow** - Define exact agent behavior
- **State management** - Track conversation and tool results
- **Debugging** - Visualize agent execution
- **Flexibility** - Customize every step

## 🚀 Quick Start

```bash
cd react-langgraph
uv sync
uv run python main.py
```

## 📊 Graph Visualization

The project includes `graph.png` showing the agent flow:
```
Start → Agent → Tools → Agent → End
```

## 🔧 Key Components

- `nodes.py` - Agent and tool execution nodes
- `react.py` - ReAct logic implementation
- `main.py` - Graph construction and execution

## 📚 Learn More

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)

## 🎓 Next Steps

- **reflection-agent** - Add self-reflection capabilities
- **agentic-rag** - Combine agents with RAG
