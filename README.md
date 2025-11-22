# LangChain Agent Base

**Production-ready AI agents in 3 lines of code** - A modular system for building LangChain 1.0 agents with Groq's blazing-fast inference, comprehensive tools, and advanced features like RAG, multi-agent coordination, and human-in-the-loop workflows.

<div align="center">

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangChain 1.0+](https://img.shields.io/badge/langchain-1.0+-green.svg)](https://python.langchain.com/)
[![Groq](https://img.shields.io/badge/groq-powered-orange.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**[📚 Documentation](docs/)** • **[🎯 Building Agents](docs/building-agents.md)** • **[🛠️ Adding Tools](docs/adding-tools.md)** • **[📈 Upgrading Agents](docs/upgrading-agents.md)** • **[🧠 Memory & RAG](docs/memory-and-rag.md)**

</div>

## ✨ **Key Features**

- **⚡ Groq Integration** - 10x faster inference than OpenAI
- **🎪 Specialist Agents** - Pre-built Math, Science, Coding agents  
- **📚 Built-in RAG** - Document search and retrieval
- **🤖 Multi-Agent Systems** - Coordinate teams of specialists
- **🛡️ Human-in-the-Loop** - Approval workflows for sensitive operations
- **🔧 15+ Tools** - Math, science, coding, and utility tools
- **⚡ Command System** - Direct tool execution bypassing chat
- **🌐 Protocol System** - Auto-generated APIs with versioning and metadata
- **📦 Agent Cards** - JSON-based metadata with Qdrant storage
- **🔍 Auto-Discovery** - Dynamic tool and agent registration
- **🧠 Conversation Memory** - Persistent chat history with smart compression
- **📚 Unified RAG** - Cross-system document and conversation search
- **⚡ Memory-Enhanced Agents** - Agents that remember previous discussions

## 🚀 **Installation**

### 1. Clone and Install
```bash
git clone https://github.com/BlueberryMathematician/langchain-agent-base.git
cd langchain-agent-base
pip install langchain>=1.0.8 langchain-groq groq langchain-huggingface sentence-transformers fastapi uvicorn qdrant-client semver
```

### 2. Set API Key
```bash
export GROQ_API_KEY="your_groq_api_key_here"
# Get free API key: https://console.groq.com/
```

### 3. Copy to Your Project
```bash
# Copy the src/ folder to your project
cp -r src/ /path/to/your/project/src/
```

## 💫 **Basic Usage**

### Simple Agent
```python
from src.base import Agent

agent = Agent()
response = agent.chat("What's 2 + 2?")
print(response)  # Uses built-in calculator tool
```

### Math Specialist
```python
from src.base import create_math_agent

math_agent = create_math_agent()
result = math_agent.chat("Solve x² + 5x + 6 = 0")
print(result)  # "Two real roots: x₁ = -2, x₂ = -3"
```

### Add Custom Tools
```python
from langchain_core.tools import tool

@tool
def my_tool(query: str) -> str:
    """My custom business logic."""
    return f"Result: {query.upper()}"

agent.add_tool(my_tool)
response = agent.chat("Use my tool with 'hello'")
```

## 📁 **Project Structure**

```
langchain-agent-base/
├── 📂 src/                           # 🎯 Core framework (copy to your project!)
│   ├── base.py                      # Agent & HITLAgent classes + factories
│   ├── tools.py                     # 15+ organized tools (math, science, coding)
│   ├── rag.py                       # RAG system & URL collection manager
│   ├── commands.py                  # Command system for direct execution
│   ├── protocol.py                  # Agent protocol & registry system
│   ├── server.py                    # Auto-generated FastAPI server
│   ├── storage.py                   # Qdrant integration for agent cards
│   └── discovery.py                 # Dynamic tool/agent discovery
├── 📂 examples/                     # 🚀 Complete implementation examples
│   └── math_agent_evolution.py     # Math agent v1.0 → v4.0 progression
├── 📂 guide/                        # 🎓 Interactive learning materials
│   ├── Using LangChain 1.0.ipynb   # "How to build" step-by-step tutorial
│   ├── Agent Usage Examples.ipynb  # "How to use" the src/ library
│   └── agent.py                     # Original tutorial functions
├── 📂 docs/                         # 📚 Complete documentation
│   ├── building-agents.md           # Create agents from Agent Usage Examples
│   ├── adding-tools.md              # Custom tool development guide
│   ├── upgrading-agents.md          # Agent evolution strategies
│   ├── agent-memory-loop.md         # System architecture deep-dive
│   ├── advanced-usage.md            # Multi-agent, RAG, HITL patterns
│   └── contributing.md              # Contribution guidelines
├── 📄 pyproject.toml                # Dependencies and project config
├── 📄 .env.example                  # Environment variables template
└── 📄 README.md                     # This overview (you are here!)
```

## 📚 **Documentation**

### 🚀 **Getting Started**
- **[Building Your First Agent](docs/building-agents.md)** - Step-by-step agent creation
- **[Adding Custom Tools](docs/adding-tools.md)** - Extend agent capabilities
- **[Upgrading Agents](docs/upgrading-agents.md)** - Evolve agents over time
- **[Math Agent Example](examples/math_agent_evolution.py)** - Complete v1.0→v4.0 evolution

### 📖 **Reference**  
- **[System Architecture](docs/agent-memory-loop.md)** - Deep dive into agent memory and loops
- **[Advanced Usage](docs/advanced-usage.md)** - Multi-agent, RAG, HITL patterns
- **[Contributing Guide](docs/contributing.md)** - How to contribute

### 🎓 **Learning**
- **["How to Build" Tutorial](guide/Using%20LangChain%201.0.ipynb)** - Learn LangChain 1.0 patterns
- **["How to Use" Examples](guide/Agent%20Usage%20Examples.ipynb)** - Library usage patterns

### 🌐 **Protocol System**
- **Automatic API Generation** - FastAPI endpoints for all agents
- **Agent Versioning** - Semantic versioning with metadata
- **Dynamic Discovery** - Auto-registration of tools and commands
- **Qdrant Storage** - Persistent agent cards with semantic search

## 🧠 **Memory & RAG System**

### Memory-Enhanced Agents

```python
from src.base import create_memory_enhanced_agent

# Agent with conversation memory + comprehensive tools
agent = create_memory_enhanced_agent()

# Remembers context across conversations
response1 = agent.chat("I'm working on a Python ML project")
response2 = agent.chat("What did we discuss about my project?")  # Remembers!

# Search previous conversations
response3 = agent.chat("Find our discussions about machine learning from last week")
```

### Unified Storage System

```python
from src.storage import UnifiedQdrantStorage

# Single Qdrant instance for all data types
storage = UnifiedQdrantStorage()

# Specialized storage interfaces
agent_storage = storage.get_agent_storage()         # Agent cards
memory_storage = storage.get_conversation_storage() # Chat history  
rag_storage = storage.get_rag_storage("docs")      # Documents
```

**💡 Key Features**:
- **Smart Compression** - Automatic conversation summarization
- **Temporal Search** - Find conversations by time range
- **URL Tracking** - Link conversations to specific resources
- **Cross-System RAG** - Search across conversations, documents, and agent cards
- **Session Management** - Persistent memory per user/project

## 🌐 **Protocol System Usage**

### Run Agent Protocol Server
```bash
# Start the auto-generated FastAPI server
python -m src.server

# API documentation available at:
# http://localhost:8000/docs
```

### Register Custom Agents
```python
from src.protocol import register_agent, AgentStatus
from src.base import Agent

@register_agent("my_domain", version="1.0.0", domain="custom")
class MySpecializedAgent(Agent):
    def __init__(self):
        super().__init__(
            system_prompt="I am specialized for my domain",
            tools=my_custom_tools()
        )

# Automatically generates API endpoints:
# POST /chat - Chat with any registered agent
# POST /command - Execute commands directly  
# GET /agents - List all registered agents
```

## 💡 **Why LangChain Agent Base?**

- **🚀 Production Ready** - Battle-tested patterns with error handling
- **🌐 Auto-Generated APIs** - FastAPI server with versioning and metadata
- **⚡ Blazing Fast** - Groq inference is 10x faster than OpenAI
- **🔧 Infinitely Extensible** - Protocol-driven architecture for any domain
- **🎯 Specialized Examples** - Math, science, and coding agent templates
- **📦 Agent Cards** - JSON metadata with Qdrant vector storage
- **🔍 Smart Discovery** - Automatic tool and agent registration

## 🤝 **Contributing**

We welcome contributions! See [Contributing Guide](docs/contributing.md) for details.

## 🙏 **Acknowledgments**

This project builds upon the excellent work by **AI Maker Space**:
- 📺 [LangChain 1.0 Complete Guide](https://www.youtube.com/watch?v=lSfAPNJx3xQ)
- 📦 [AI-Maker-Space/LangChain1.0](https://github.com/AI-Maker-Space/LangChain1.0)

---

**🎯 Ready to build powerful AI agents? Start with the [Getting Started Guide](docs/getting-started.md)!** 🚀