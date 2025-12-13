# Reflection Agent

Agent that reflects on its outputs and iteratively improves them using LangGraph.

## 🎯 What is Reflection?

Reflection is a pattern where an agent:
1. **Generates** an initial response
2. **Critiques** its own output
3. **Revises** based on the critique
4. **Repeats** until satisfied

## 🔄 Reflection Loop

```
Generate → Reflect → Revise → Reflect → Revise → Final Answer
```

## 🚀 Quick Start

```bash
cd reflection-agent
uv sync
uv run python main.py
```

## 📁 Key Files

- `chains.py` - Generation and reflection chains
- `main.py` - LangGraph implementation with reflection loop

## ✨ Benefits

- **Self-Improvement** - Agent improves its own outputs
- **Quality Control** - Built-in critique mechanism
- **Iterative Refinement** - Multiple revision cycles
- **No Human Feedback** - Autonomous improvement

## 🔧 How It Works

1. **Generate** - Create initial answer
2. **Reflect** - Identify issues and improvements
3. **Revise** - Update answer based on reflection
4. **Loop** - Repeat until quality threshold met

## 📚 Learn More

- [Reflexion Paper](https://arxiv.org/abs/2303.11366)
- [Self-Refine Paper](https://arxiv.org/abs/2303.17651)

## 🎓 Next Steps

- **reflexion-agent** - Add search for external information
- **agentic-rag** - Combine reflection with RAG and grading
