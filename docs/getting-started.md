# Getting Started with LangChain Agent Base

**The Ultimate Import Library for AI Agents** - Get up and running with powerful AI agents in minutes!

## 🎯 Quick Overview

LangChain Agent Base is a production-ready, class-based system for building LangChain agents using Groq's blazing-fast `gpt-oss-120b` model. Simply import and instance powerful agents in seconds!

### Key Benefits
- **🔥 Ultra-Fast**: 10x faster than OpenAI with Groq's gpt-oss-120b
- **📦 Import Ready**: `from src.base import Agent` - Done!
- **🎪 Instant Specialization**: Pre-built Math, Science, Coding agents
- **📚 Built-in RAG**: Document search in any agent
- **🔧 15+ Tools**: Comprehensive tool collections
- **🤖 Multi-Agent**: Coordinate teams of specialists

## 🚀 Installation

### Option 1: Use in Existing Project (Recommended)

1. **Copy the `src/` folder** into your project:
   ```bash
   cp -r langchain-agent-base/src/ ./src/
   ```

2. **Install core dependencies**:
   ```bash
   pip install langchain>=1.0.0 langchain-groq groq langchain-huggingface sentence-transformers
   ```

3. **Set your API key**:
   ```bash
   export GROQ_API_KEY="your_groq_api_key_here"
   ```

4. **Start using**:
   ```python
   from src.base import Agent
   agent = Agent()
   response = agent.chat("Hello world!")
   ```

### Option 2: Clone Full Template

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd langchain-agent-base
   ```

2. **Install all dependencies**:
   ```bash
   pip install -r requirements.txt
   # OR using the pyproject.toml
   pip install langchain>=1.0.8 langchain-groq groq langchain-huggingface sentence-transformers langgraph langsmith langchain-community qdrant-client langchain-qdrant beautifulsoup4
   ```

3. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## 🎯 Your First Agent (30 Seconds)

```python
# 1. Import the Agent class
from src.base import Agent

# 2. Create an agent
agent = Agent()

# 3. Chat with your agent
response = agent.chat("What's the weather like?")
print(response)  # "The weather in [location] is Sunny."
```

**That's it!** You now have a working AI agent.

## 🔧 Adding Capabilities

### Add Tools to Any Agent

```python
from src.base import Agent
from src.tools import get_math_tools, get_science_tools

# Create agent
agent = Agent()

# Add math capabilities
agent.add_tools(get_math_tools())

# Add science capabilities  
agent.add_tools(get_science_tools())

# Now your agent can do math and science!
response = agent.chat("Calculate the square root of 144 and convert 100°F to Celsius")
```

## 🚀 Protocol System (Advanced)

### Create Registered Agents with Auto-API

```python
from src.protocol import register_agent, AgentStatus
from src.base import Agent
from src.tools import get_math_tools

# Create specialized agent with automatic registration
@register_agent("math_expert", version="1.0.0", domain="mathematics", 
                status=AgentStatus.PRODUCTION)
class MathAgent(Agent):
    def __init__(self):
        super().__init__(
            system_prompt="Advanced mathematical assistant with specialized tools",
            tools=get_math_tools()
        )

# Automatically generates:
# - REST API endpoints (/chat, /commands, /tools)
# - Agent metadata (AgentCard) stored in Qdrant
# - Version management and discovery
```

### Run Protocol Server

```python
from src.server import run_protocol_server

# Start server with all registered agents
run_protocol_server(host="0.0.0.0", port=8000)

# Visit http://localhost:8000/docs for auto-generated API
# All registered agents available via REST endpoints
```

### Use Pre-Built Specialists

```python
from src.base import create_math_agent, create_science_agent, create_coding_agent

# Pre-configured specialist agents
math_expert = create_math_agent()      # Calculator, equations, matrices
science_expert = create_science_agent()  # Unit conversion, chemistry, physics
coding_expert = create_coding_agent()   # Code analysis, regex, JSON tools

# Each specialist is ready to use immediately
result = math_expert.chat("Solve x² + 5x + 6 = 0")
```

### Add Document Search (RAG)

```python
from src.base import Agent

# Create agent with document search
agent = Agent()
agent.add_rag("./my_documents/")  # Indexes all files automatically

# Now search documents
response = agent.chat("What does the contract say about payment terms?")
```

## ⚡ Commands for Speed

Skip the LLM overhead for direct tool execution:

```python
# Enable commands
agent.enable_commands()

# Direct tool execution (faster)
result = agent.execute_command("/calc", expression="15 * 23 + 7")
# vs slower chat: agent.chat("Calculate 15 * 23 + 7")

# List available commands
print(agent.list_commands())
```

## 🤝 Multi-Agent Systems

```python
from src.base import create_multi_agent_supervisor

# Create supervisor that coordinates specialists
supervisor = await create_multi_agent_supervisor()

# Complex query handled by multiple specialists
response = supervisor.chat(
    "Calculate kinetic energy for 50kg at 10 m/s, then write Python code for the formula"
)
# Supervisor delegates to math and coding agents automatically
```

## 🛡️ Human-in-the-Loop

```python
from src.base import HITLAgent

# Create agent requiring approval for sensitive operations
hitl_agent = HITLAgent(interrupt_tools=["file_operations", "api_calls"])

# Agent will ask for permission before using sensitive tools
response = hitl_agent.chat("Delete the old log files")
# → Triggers approval workflow instead of executing immediately
```

## 📚 What's Next?

- **[API Reference](api-reference.md)** - Complete class and method documentation
- **[Tool Collections](tool-collections.md)** - All available tools and how to use them
- **[Advanced Usage](advanced-usage.md)** - Multi-agent, RAG, HITL patterns
- **[Examples](examples.md)** - Real-world application patterns
- **[Contributing](contributing.md)** - How to add your own tools and features

## 🎯 Ready to Build!

You're now ready to create powerful AI agents. Start with a basic agent and gradually add the capabilities you need. The modular design makes it easy to scale from simple chatbots to complex multi-agent systems.

**Happy building! 🚀**