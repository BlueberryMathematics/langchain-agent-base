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

## 🧪 **Creating Custom Agents from Scratch**

Build your own specialized agents without using the pre-built factories:

### **Custom Math Agent from Ground Up**

```python
from src.base import Agent
from src.tools import advanced_calculator, solve_quadratic
from src.protocol import register_agent, AgentStatus
from langchain_core.tools import tool

# Create custom tool for your math domain
@tool
def statistical_analysis(data: str) -> str:
    """Perform statistical analysis on comma-separated numbers."""
    try:
        numbers = [float(x.strip()) for x in data.split(',')]
        mean = sum(numbers) / len(numbers)
        variance = sum((x - mean)**2 for x in numbers) / len(numbers)
        std_dev = variance ** 0.5
        return f"Mean: {mean:.2f}, Std Dev: {std_dev:.2f}, Count: {len(numbers)}"
    except Exception as e:
        return f"Error: {str(e)}"

# Register your custom agent with the protocol system
@register_agent("custom_math", version="1.0.0", domain="mathematics", 
                status=AgentStatus.DEVELOPMENT)
class CustomMathAgent(Agent):
    """My custom mathematics agent with statistics."""
    def __init__(self):
        super().__init__(
            system_prompt="I am a custom mathematics agent specializing in calculations and statistical analysis.",
            enable_memory=True,  # Enable persistent conversation memory
            enable_commands=True  # Enable direct command execution
        )
        
        # Add tools gradually
        self.add_tool(advanced_calculator)
        self.add_tool(statistical_analysis)
        
# Create and use your custom agent
my_math_agent = CustomMathAgent()
response = my_math_agent.chat("Analyze this data: 12, 15, 18, 22, 25, 19, 16")
print(response)  # Statistical analysis with your custom tool
```

### **Custom Science Agent with Domain-Specific Tools**

```python
from src.tools import unit_converter, chemistry_helper

@tool
def lab_safety_check(chemical: str, procedure: str) -> str:
    """Provide safety recommendations for lab procedures."""
    safety_db = {
        "HCl": "Wear safety goggles, use fume hood, have neutralizing agent ready",
        "NaOH": "Avoid skin contact, wear gloves, keep away from acids",
        "H2SO4": "Extreme caution: concentrated acid, add to water never reverse"
    }
    
    base_safety = safety_db.get(chemical, "Follow standard lab safety protocols")
    return f"Safety for {chemical} in {procedure}: {base_safety}"

@register_agent("lab_assistant", version="1.0.0", domain="chemistry",
                status=AgentStatus.PRODUCTION)
class LabAssistantAgent(Agent):
    """Laboratory assistant for chemistry work."""
    def __init__(self):
        super().__init__(
            system_prompt="I am a laboratory assistant specializing in chemistry safety and calculations.",
            enable_memory=True
        )
        
        # Add tools specific to lab work
        self.add_tools([unit_converter, chemistry_helper, lab_safety_check])

# Create lab assistant
lab_agent = LabAssistantAgent()
response = lab_agent.chat("I need to prepare 500mL of 0.1M HCl solution")
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

## 📈 **Evolving Agents Over Time**

Start simple and add capabilities as your needs grow:

### **Agent Evolution Strategy**

```python
# Version 1.0: Basic calculator
@register_agent("evolving_math", version="1.0.0", domain="mathematics")
class BasicMathAgent(Agent):
    def __init__(self):
        super().__init__(
            system_prompt="I can do basic calculations.",
            tools=[advanced_calculator]
        )

# Version 1.1: Add equation solving
@register_agent("evolving_math", version="1.1.0", domain="mathematics")
class EnhancedMathAgent(Agent):
    def __init__(self):
        super().__init__(
            system_prompt="I can calculate and solve equations.",
            tools=[advanced_calculator, solve_quadratic]
        )

# Version 2.0: Add memory and statistics
@register_agent("evolving_math", version="2.0.0", domain="mathematics")
class AdvancedMathAgent(Agent):
    def __init__(self):
        super().__init__(
            system_prompt="Advanced math with memory and statistical analysis.",
            enable_memory=True,
            tools=[advanced_calculator, solve_quadratic, statistical_analysis]
        )
```

### **Adding Tools Dynamically**

```python
# Start with basic agent
agent = Agent(enable_memory=True)

# Add tools based on user needs
if user_needs_math:
    from src.tools import get_math_tools
    agent.add_tools(get_math_tools())
    print("Added math capabilities")

if user_needs_science:
    from src.tools import get_science_tools  
    agent.add_tools(get_science_tools())
    print("Added science capabilities")

# Create custom tools on the fly
@tool
def domain_specific_tool(query: str) -> str:
    """Handle domain-specific queries."""
    return f"Processing {query} with domain logic"

agent.add_tool(domain_specific_tool)

# Agent capabilities now include all added tools
print(f"Agent now has {len(agent.list_tools())} tools available")
```

## 🗂️ **Managing Your Agent Library**

Build applications that discover and use your collection of agents:

### **Agent Discovery and Management**

```python
from src.protocol import get_agent_registry, AgentStatus
from src.storage import UnifiedQdrantStorage

# Get the global agent registry
registry = get_agent_registry()

# List all registered agents
all_agents = registry.list_agents()
print(f"Found {len(all_agents)} registered agents:")

for agent_card in all_agents:
    print(f"- {agent_card.name} v{agent_card.version} ({agent_card.domain})")
    print(f"  Status: {agent_card.status}")
    print(f"  Tools: {len(agent_card.tools)}")
    print(f"  Description: {agent_card.description}")
```

### **Building Applications with Agent Libraries**

```python
class AgentManager:
    """Manage a library of specialized agents for applications."""
    
    def __init__(self):
        self.registry = get_agent_registry()
        self.storage = UnifiedQdrantStorage()
        self.active_agents = {}
    
    def get_agents_by_domain(self, domain: str) -> List[str]:
        """Get all agents for a specific domain."""
        agents = self.registry.list_agents(domain=domain)
        return [(a.name, a.version) for a in agents if a.status == AgentStatus.PRODUCTION]
    
    def load_agent(self, name: str, version: str = None):
        """Load an agent by name and version."""
        agent_card = self.registry.get_agent_card(name, version)
        if agent_card:
            agent_class = self.registry.get_agent_class(name, version)
            self.active_agents[f"{name}:{version or 'latest'}"] = agent_class()
            return True
        return False
    
    def chat_with_agent(self, agent_key: str, message: str, session_id: str = None):
        """Chat with a specific loaded agent."""
        if agent_key in self.active_agents:
            agent = self.active_agents[agent_key]
            if hasattr(agent, 'memory_session_id') and session_id:
                agent.memory_session_id = session_id
            return agent.chat(message)
        return "Agent not found or not loaded"
    
    def search_agents(self, query: str) -> List[dict]:
        """Search for agents by capabilities."""
        return self.storage.get_agent_storage().search_agents(query)

# Example application
app = AgentManager()

# Find math agents
math_agents = app.get_agents_by_domain("mathematics")
print(f"Available math agents: {math_agents}")

# Load specific agents
app.load_agent("custom_math", "2.0.0")
app.load_agent("lab_assistant", "1.0.0")

# Use agents in application
math_response = app.chat_with_agent("custom_math:2.0.0", 
                                   "Calculate mean of: 10,20,30,40", 
                                   session_id="user_123")

lab_response = app.chat_with_agent("lab_assistant:1.0.0",
                                  "Safety check for handling HCl",
                                  session_id="lab_session_456")
```

### **Production Agent Server**

```python
# Start server with all registered agents available via API
from src.server import run_protocol_server

# This automatically exposes all registered agents via REST API
run_protocol_server(host="0.0.0.0", port=8000)

# API endpoints automatically generated:
# GET /agents - List all available agents
# POST /agents/{name}/chat - Chat with specific agent
# GET /agents/{name}/tools - Get agent capabilities
# GET /agents/{name}/versions - Get all versions of an agent
```

### **Client Application Example**

```python
import requests

class AgentClient:
    """Client for interacting with agent server."""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def list_agents(self):
        """Get all available agents from server."""
        response = requests.get(f"{self.base_url}/agents")
        return response.json()
    
    def chat_with_agent(self, agent_name: str, message: str, session_id: str = None):
        """Send message to specific agent."""
        data = {
            "message": message,
            "session_id": session_id or "default"
        }
        response = requests.post(f"{self.base_url}/agents/{agent_name}/chat", json=data)
        return response.json()

# Use client in your application
client = AgentClient()
agents = client.list_agents()
print(f"Server has {len(agents['agents'])} available agents")

# Chat with agents remotely
response = client.chat_with_agent("custom_math", "What's the square root of 144?", "user_session")
print(response["response"])
```

## 📚 What's Next?

- **[API Reference](api-reference.md)** - Complete class and method documentation
- **[Tool Collections](tool-collections.md)** - All available tools and how to use them
- **[Advanced Usage](advanced-usage.md)** - Multi-agent, RAG, HITL patterns
- **[Examples](examples.md)** - Real-world application patterns
- **[Contributing](contributing.md)** - How to add your own tools and features

## 🎯 Ready to Build!

You now have everything needed to:
- **Create custom agents** from scratch with specialized tools
- **Evolve agents over time** by adding capabilities and versioning
- **Build applications** that discover and manage agent libraries
- **Deploy production systems** with automatic API generation

Start with a simple custom agent, register it with the protocol system, and build applications that leverage your growing agent library!

**Happy building! 🚀**