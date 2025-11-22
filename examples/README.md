# Examples Directory

This directory contains comprehensive examples demonstrating the LangChain Agent Base Protocol system.

## 📁 Available Examples

### 🏗️ **Building Your Ultimate Math Agent** (`building-ultimate-math-agent/`)
**Complete guide to creating your own specialized agent project**

A comprehensive tutorial showing:
- How to set up a new project using this framework
- Complete project structure with all files
- Step-by-step instructions for building a custom math agent
- How to add your own custom tools
- Deployment options (CLI, API, web app integration)
- Daily development workflow

```bash
# Read the comprehensive guide
cat examples/building-ultimate-math-agent/README.md
```

**Perfect for:**
- Starting your own agent project from scratch
- Understanding how to use the framework in production
- Learning best practices for agent development
- Building domain-specific AI assistants

### 🧮 **Math Agent Evolution** (`math_agent_evolution.py`)
**Complete agent evolution from basic to advanced**

Demonstrates:
- Agent versioning (v1.0 → v4.0-beta)
- Progressive capability enhancement
- Custom tool development
- Factory function patterns
- Production deployment strategies

```bash
# Run the math agent demonstration
python examples/math_agent_evolution.py
```

**Agent Versions Shown:**
- **v1.0**: Basic calculator with simple arithmetic
- **v2.0**: Enhanced with linear algebra and matrix operations
- **v3.0**: Ultimate with symbolic math, statistics, and number theory
- **v4.0-beta**: Experimental with AI-powered theorem proving

### 🌐 **Protocol System Usage** (`protocol_usage.py`)
**Complete protocol system demonstration**

Demonstrates:
- Custom agent registration with `@register_agent`
- Automatic API generation and versioning
- Agent cards and metadata management
- Dynamic discovery and tool registration
- REST API usage and client interactions

```bash
# Run the complete protocol demonstration
python examples/protocol_usage.py
```

**Features Shown:**
- Business domain agent with customer/order tools
- Enhanced science agent with chemistry predictions
- Multi-domain consultant agent
- REST API examples with curl commands

## 🚀 **Quick Start Guide**

### 1. **Start with Math Agent Evolution**
```bash
python examples/math_agent_evolution.py
```
This shows the progression from basic to advanced agents and serves as the foundation for understanding agent development patterns.

### 2. **Explore Protocol System**
```bash
python examples/protocol_usage.py
```
This demonstrates the full protocol system with custom agents, registration, and API generation.

### 3. **Run the Protocol Server**
```bash
python main.py server
```
Then visit `http://localhost:8000/docs` to see the auto-generated API documentation.

## 🎯 **Learning Path**

1. **📖 Read Documentation First**
   - [Building Agents](../docs/building-agents.md) - Learn the basics
   - [Adding Tools](../docs/adding-tools.md) - Create custom tools
   - [Upgrading Agents](../docs/upgrading-agents.md) - Evolution strategies

2. **🧮 Study Math Agent Evolution**
   - Understand versioning and capability progression
   - Learn tool composition patterns
   - See factory function usage

3. **🌐 Explore Protocol System**
   - Learn agent registration and discovery
   - Understand API auto-generation
   - Practice REST API interactions

4. **🛠 Build Your Own Agent**
   - Choose a domain (finance, healthcare, etc.)
   - Create custom tools for your domain
   - Register with the protocol system
   - Deploy with auto-generated APIs

## 📋 **Code Patterns Reference**

### Agent Registration
```python
from src.protocol import register_agent, AgentStatus
from src.base import Agent

@register_agent("my_domain", version="1.0.0", domain="custom")
class MyAgent(Agent):
    def __init__(self):
        super().__init__(
            system_prompt="I am specialized for my domain",
            tools=my_custom_tools()
        )
```

### Custom Tool Creation
```python
from langchain_core.tools import tool

@tool
def my_tool(param: str) -> str:
    """Tool description for the LLM."""
    return f"Processed: {param}"
```

### Factory Functions
```python
def create_my_agent(**kwargs):
    """Factory function for easy agent creation."""
    return MyAgent(**kwargs)
```

### API Server Usage
```python
from src.server import run_protocol_server

# Start server with all registered agents
run_protocol_server(host="0.0.0.0", port=8000)
```

## 🔧 **Customization Examples**

### Domain-Specific Agents
- **Finance Agent**: Portfolio analysis, risk assessment, market data
- **Healthcare Agent**: Medical calculations, drug interactions, diagnostic support
- **Legal Agent**: Contract analysis, legal research, compliance checking
- **Education Agent**: Lesson planning, student assessment, curriculum design

### Tool Categories
- **API Integration**: External service connections
- **Data Processing**: File manipulation, format conversion
- **Calculations**: Domain-specific mathematical operations
- **Knowledge Base**: RAG integration with specialized documents

### Command Systems
- **Direct Execution**: Bypass chat for simple operations
- **Batch Processing**: Multiple operations in sequence
- **Monitoring**: Performance and usage tracking
- **Administration**: Agent management and configuration

## 🌟 **Best Practices Demonstrated**

1. **Semantic Versioning**: Clear version progression with compatibility
2. **Modular Design**: Separate tools, commands, and agent logic
3. **Error Handling**: Graceful degradation and user feedback
4. **Documentation**: Clear docstrings and usage examples
5. **Testing**: Validation of agent capabilities and tool functionality
6. **API Design**: RESTful endpoints with proper HTTP methods
7. **Metadata Management**: Rich agent cards with searchable information

## 🎭 **Running All Examples**

```bash
# Math agent evolution
python examples/math_agent_evolution.py

# Protocol system demonstration  
python examples/protocol_usage.py

# Start protocol server (combines everything)
python main.py server

# Auto-discovery demonstration
python main.py discover

# File system watcher
python main.py watch ./examples/
```

## 📚 **Next Steps**

After exploring these examples:

1. **Build Your Domain Agent** - Use the patterns to create agents for your specific use case
2. **Contribute Examples** - Add new domain examples to help the community
3. **Extend the Protocol** - Enhance the system with new features
4. **Deploy in Production** - Use the protocol server for real applications

Happy building! 🚀