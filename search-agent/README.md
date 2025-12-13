# Search Agent

Agent that can perform web searches to answer questions using Tavily.

## 🎯 What You'll Learn

- How to give agents access to tools
- Web search integration with Tavily
- Tool calling and result processing
- Agent reasoning loops

## 🚀 Quick Start

```bash
cd search-agent
uv sync
uv run python main.py
```

## 🔧 How It Works

1. **Question** - User asks a question
2. **Reasoning** - Agent decides if it needs to search
3. **Tool Call** - Agent calls Tavily search
4. **Observation** - Agent processes search results
5. **Answer** - Agent formulates final answer

## 🔑 Prerequisites

- OpenAI API key
- Tavily API key

## 📚 Learn More

- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- [Tavily Search](https://tavily.com/)

## 🎓 Next Steps

- **react-agent-impl** - Understand ReAct pattern
- **react-langgraph** - Build agents with LangGraph
