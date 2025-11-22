# LangChain Agent Base

**The Ultimate Import Library for AI Agents** - A production-ready, class-based system for building LangChain agents using Groq's blazing-fast `gpt-oss-120b` model. Simply import and create powerful agents in seconds!

<div align="center">

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangChain 1.0+](https://img.shields.io/badge/langchain-1.0+-green.svg)](https://python.langchain.com/)
[![Groq](https://img.shields.io/badge/groq-powered-orange.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**[📚 Documentation](docs/)** • **[🚀 Quick Start](#-quick-start)** • **[🎯 Examples](#-examples)** • **[🛠️ API Reference](docs/api-reference.md)**

</div>

## 🎯 **Perfect For**

- **🆕 New Projects**: Import and create agents instantly
- **🔧 Existing Codebases**: Drop-in agent functionality 
- **⚡ Rapid Prototyping**: Agents in 3 lines of code
- **🏭 Production Apps**: Scalable, extensible architecture
- **👥 Team Development**: Consistent agent patterns across projects

## ✨ **Key Features**

- **🔥 Ultra-Fast Imports**: `from src.base import Agent` - Done!
- **⚡ Groq Integration**: 10x faster inference than OpenAI
- **🎪 Instant Specialization**: Pre-built Math, Science, Coding agents
- **📚 Built-in RAG**: Document search in any agent
- **🛡️ Human-in-the-Loop**: Approval workflows for sensitive operations
- **🤖 Multi-Agent**: Coordinate teams of specialized agents
- **🔧 15+ Tools**: Comprehensive tool collections
- **⚡ Command System**: Direct tool execution without LLM overhead
- **📖 Complete Documentation**: Comprehensive guides and examples

## 🚀 **Quick Start**

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

4. **Start building**:
   ```python
   from src.base import Agent
   agent = Agent()
   response = agent.chat("Hello world!")
   print(response)
   ```

### Option 2: Clone Full Template

```bash
git clone <repository-url>
cd langchain-agent-base
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
```

## 🎯 **Examples**

### Basic Agent (30 seconds)
```python
from src.base import Agent

# Create and use immediately
agent = Agent()
response = agent.chat("What's 2 + 2?")
```

### Specialist Agents
```python
from src.base import create_math_agent, create_science_agent, create_coding_agent

# Pre-configured specialists
math_agent = create_math_agent()      # Calculator, equations, matrices
science_agent = create_science_agent()  # Unit conversion, chemistry, physics  
coding_agent = create_coding_agent()   # Code analysis, regex, JSON tools

# Ready to use immediately
result = math_agent.chat("Solve x² + 5x + 6 = 0")
```

### Document Search (RAG)
```python
from src.base import create_rag_agent

# Create agent with document search
rag_agent = await create_rag_agent(documents=["doc1.txt", "doc2.txt"])
response = rag_agent.chat("What does the contract say about payments?")
```

### Custom Tools
```python
from src.base import Agent
from langchain_core.tools import tool

@tool
def my_api_call(query: str) -> str:
    """Call my API with query."""
    return f"API result for: {query}"

agent = Agent()
agent.add_tool(my_api_call)
response = agent.chat("Call my API with 'hello'")
```

### **5. Direct Commands (No Chat)**
```python
from src.commands import CommandRegistry

# Skip conversation, get instant results
registry = CommandRegistry()
result = registry.execute("calculate 15 * 23")  # Returns: 345
weather = registry.execute("weather Tokyo")     # Returns weather data
```

### **6. Multi-Agent Teams**
```python
from src.base import create_math_agent, create_science_agent, Agent

# Create team of specialists
math_expert = create_math_agent()
science_expert = create_science_agent()

# Supervisor coordinates them
supervisor = Agent()
supervisor.add_agent_as_tool("math_expert", math_expert)
supervisor.add_agent_as_tool("science_expert", science_expert)

response = supervisor.chat("Calculate the velocity of a 50kg object falling 10 meters")
```

### **7. Human-in-the-Loop**
```python
from src.base import HITLAgent

# Agent asks permission before actions
safe_agent = HITLAgent()
safe_agent.chat("Delete all my files")  # Will ask: "Should I really do this? [y/N]"
```

## 🔧 **Real-World Usage Patterns**

### **Web App Integration**
```python
# Flask example
from flask import Flask, request, jsonify
from src.base import Agent

app = Flask(__name__)
agent = Agent()

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    response = agent.chat(user_message)
    return jsonify({'response': response})
```

### **Data Analysis Pipeline**
```python
from src.base import create_science_agent, Agent
import pandas as df

# Create analysis agent with data tools
analyst = create_science_agent()
analyst.add_rag("./data_reports/")  # Add documentation

# Analyze data
data = pd.read_csv("sales.csv")
result = analyst.chat(f"Analyze this sales data trends: {data.head()}")
```

### **Custom Business Agent**
```python
from src.base import Agent
from langchain_core.tools import tool

@tool
def check_inventory(product: str) -> str:
    """Check product inventory levels."""
    # Your business logic here
    return f"Product {product}: 42 units in stock"

@tool  
def process_order(product: str, quantity: int) -> str:
    """Process customer order."""
    # Your order processing logic
    return f"Order processed: {quantity} units of {product}"

# Create business assistant
assistant = Agent()
assistant.add_tools([check_inventory, process_order])
assistant.chat("Check inventory for laptops and process order for 5 units")
```

## 🛠️ **Available Tools (Pick & Choose)**

### **Import Tool Collections**
```python
from src.tools import (
    get_math_tools,        # 🧮 Calculator, equations, matrix math
    get_science_tools,     # 🔬 Unit conversion, chemistry, physics  
    get_coding_tools,      # 💻 Code analysis, regex, JSON tools
    get_basic_tools        # 🌟 Weather, magic calculator
)

# Add entire collections
agent.add_tools(get_math_tools())     # All math tools at once
agent.add_tools(get_science_tools())  # All science tools

# Or cherry-pick individual tools
from src.tools import advanced_calculator, unit_converter
agent.add_tools([advanced_calculator, unit_converter])
```

### **Individual Tools Reference**
```python
# Math & Calculations
advanced_calculator      # "calculate 2^10 + sqrt(144)"
solve_quadratic         # "solve x² + 5x + 6 = 0"  
matrix_operations       # "multiply [[1,2],[3,4]] by [[5,6],[7,8]]"

# Science & Conversions  
unit_converter          # "convert 100°F to Celsius"
chemistry_helper        # "molecular weight of H2SO4"
physics_calculator      # "kinetic energy of 50kg at 10m/s"

# Programming & Text
code_analyzer           # "analyze complexity of this Python code"
regex_helper            # "create regex for email validation"
json_formatter          # "validate and format this JSON"

# Basic Utilities
get_weather             # "weather in Paris" (returns: "Sunny")
magic_calculator        # "(5 + 3) * 2" (returns: 16)
```

## 🎨 **Customization & Configuration**

### **Create Your Own Agent Class**
```python
from src.base import Agent
from src.tools import get_math_tools

class BusinessAgent(Agent):
    def __init__(self):
        super().__init__(system_prompt="You are a business analyst assistant.")
        self.add_tools(get_math_tools())  # Add math for financial calculations
        
        # Add your custom business tools
        from langchain_core.tools import tool
        
        @tool
        def get_sales_data(month: str) -> str:
            """Get monthly sales data."""
            return f"Sales for {month}: $50,000"
        
        self.add_tool(get_sales_data)

# Use it
business_bot = BusinessAgent()
result = business_bot.chat("What were sales in January and calculate 15% growth")
```

### **Add Custom Tools**
```python
from langchain_core.tools import tool

@tool
def my_custom_tool(param1: str, param2: int) -> str:
    """Description of what this tool does."""
    return f"Result: {param1} × {param2}"

# Add to any agent
agent.add_tool(my_custom_tool)
```

### **Model Settings**
```python
# Custom Groq model settings
agent = Agent(
    model_name="groq/gpt-oss-120b",  # Default: fast inference
    temperature=0.1,                 # Lower = more focused
    system_prompt="You are a helpful assistant."
)
```

### **RAG Document Settings**  
```python
# Configure document search
agent.add_rag(
    documents_path="./my_docs/",
    collection_name="company_docs",
    chunk_size=300,                 # Smaller chunks = more precise
    embedding_model="all-MiniLM-L6-v2"  # Free HuggingFace model
        )
```

## 🚀 **Project Templates**

### **Generate Complete Projects**
```python
# Use the built-in project generator
from project_generator import ProjectGenerator

generator = ProjectGenerator()

# Create a new project with custom agents
generator.create_project(
    name="my_ai_assistant",
    path="./my_projects/",
    agents=["math", "science", "custom_business"]
)

# This creates a full project structure with:
# - Virtual environment setup
# - Dependencies installed  
# - Custom agent classes
# - Usage examples
# - Ready to run!
```

## 🏗️ **Project Structure**

```
langchain-agent-base/              # Copy this src/ folder to your projects
├── src/
│   ├── base.py          # 🤖 Agent & HITLAgent classes + factories
│   ├── tools.py         # 🛠️  15+ tools organized by domain  
│   ├── rag.py           # 📚 RAGManager + document search
│   ├── commands.py      # ⚡ Command system for direct execution
│   └── agent.py         # 🔄 Legacy tutorial functions (preserved)
├── examples.py          # 📖 Usage examples & demos
├── project_generator.py # 🏗️  Generate new agent projects
└── README.md           # 📝 This documentation
```

## 💡 **Why This Design?**

- **Not a Python package** → Copy `src/` and modify freely for your needs
- **LangChain 1.0 compliant** → Uses latest create_agent() patterns
- **Groq optimized** → 10x faster inference than OpenAI  
- **Modular** → Mix and match tools, agents, RAG as needed
- **Production ready** → Human-in-the-loop, multi-agent, command systems

## 🔗 **Legacy Compatibility**

All original LangChain 1.0 tutorial functions are preserved in `src/agent.py`:
```python  
from src.agent import build_simple_agent, build_hitl_agent, build_rag_agent

# These work exactly like the original tutorial
simple_agent = build_simple_agent() 
rag_agent = build_rag_agent()
```

## 📞 **Need Help?**

This codebase gives you everything to build production LangChain agents. The key is the **modular design** - take what you need:

- Just want basic chat? → `Agent()`
- Need math tools? → `create_math_agent()`  
- Want document search? → `agent.add_rag("./docs/")`
- Direct commands? → `CommandRegistry().execute("weather Paris")`
- Custom business logic? → Add your `@tool` functions

**Copy `src/` into your project and start building!** 🚀
- **Production Ready**: Includes error handling, logging, and best practices
- **Educational**: Well-documented code for learning LangChain 1.0 patterns

---

## 📋 **Next Steps Checklist**

### **✅ 30-Second Test**
1. Copy `src/` folder to your project
2. `pip install langchain-groq langchain-community qdrant-client langchain-huggingface`  
3. `export GROQ_API_KEY="your_key"`
4. Test: `python -c "from src.base import Agent; print(Agent().chat('Hello'))"`

### **✅ Add Your Domain**
1. Browse `src/tools.py` → Pick relevant tools
2. Create custom tools with `@tool` decorator  
3. Use factories: `create_math_agent()`, `create_science_agent()`, etc.
4. Test your agent with domain-specific queries

### **✅ Production Integration** 
1. Add documents: `agent.add_rag("./my_docs/")`
2. Use commands: `CommandRegistry().execute("weather NYC")`
3. Add Human-in-the-Loop: `HITLAgent()` for sensitive operations  
4. Deploy with your web framework (Flask, FastAPI, etc.)

### **🛡️ Security Notes**
- Validate inputs for production use
- Sandbox `execute_python` tool in production
- Set API rate limits and error handling
- Review all tools before deployment

---

## 📚 **Resources**

- **[LangChain 1.0 Docs](https://python.langchain.com/docs/)** - Core framework documentation
- **[Groq API Keys](https://console.groq.com/docs)** - Get free fast inference  
- **[LangGraph Docs](https://langchain-ai.github.io/langgraph/)** - Multi-agent workflows

---

### Multi-Agent Systems
```python
from src.base import create_multi_agent_supervisor

# Supervisor coordinates specialists
supervisor = await create_multi_agent_supervisor()
response = supervisor.chat(
    "Calculate kinetic energy for 50kg at 10m/s, then write Python code for it"
)
# Automatically delegates to math and coding agents
```

### Human-in-the-Loop
```python
from src.base import HITLAgent

# Requires approval for sensitive operations
hitl_agent = HITLAgent(interrupt_tools=["file_operations"])
response = hitl_agent.chat("Delete old log files")
# Triggers approval workflow instead of executing immediately
```

### Command System (Fast Direct Execution)
```python
# Enable commands for speed
agent.enable_commands()

# Direct tool execution (faster than chat)
result = agent.execute_command("/calc", expression="15 * 23 + 7")
```

## 📁 **Project Structure**

```
langchain-agent-base/
├── 📂 src/                    # Core library (import this!)
│   ├── base.py               # Agent & HITLAgent classes
│   ├── tools.py              # 15+ organized tools
│   ├── rag.py                # RAG system & setup
│   └── commands.py           # Command system
├── 📂 guide/                 # Learning materials
│   ├── Using LangChain 1.0.ipynb     # "How to build" tutorial
│   ├── Agent Usage Examples.ipynb    # "How to use" examples
│   └── agent.py              # Tutorial functions
├── 📂 docs/                  # Comprehensive documentation
│   ├── getting-started.md    # Installation & first steps
│   ├── api-reference.md      # Complete API documentation
│   ├── tool-collections.md   # All available tools
│   ├── advanced-usage.md     # Multi-agent, RAG, HITL
│   └── examples.md           # Real-world patterns
├── 📄 README.md              # This file
├── 📄 pyproject.toml         # Dependencies
└── 📄 .env.example           # Environment template
```

## 📚 **Documentation**

- **[🚀 Getting Started](docs/getting-started.md)** - Installation and first steps
- **[📖 API Reference](docs/api-reference.md)** - Complete class and method docs
- **[🔧 Tool Collections](docs/tool-collections.md)** - All available tools
- **[⚙️ Advanced Usage](docs/advanced-usage.md)** - Multi-agent, RAG, HITL patterns
- **[💡 Examples](docs/examples.md)** - Real-world application patterns
- **[🤝 Contributing](docs/contributing.md)** - How to add features

## 🎓 **Learning Materials**

- **[📓 "How to Build" Tutorial](guide/Using%20LangChain%201.0.ipynb)** - Learn LangChain 1.0 patterns
- **[📘 "How to Use" Examples](guide/Agent%20Usage%20Examples.ipynb)** - Import and use the library

## 🛠️ **Core Components**

### Agent Classes
- **`Agent`** - Main agent class with tools and commands
- **`HITLAgent`** - Human-in-the-loop for sensitive operations
- **Factory functions** - Pre-configured specialists

### Tool Collections  
- **Math Tools** - Calculator, equations, matrices
- **Science Tools** - Unit conversion, chemistry, physics
- **Coding Tools** - Code analysis, regex, JSON formatting
- **Custom Tools** - Easy to add your own

### Advanced Features
- **RAG System** - Document search and retrieval
- **Command System** - Direct tool execution
- **Multi-Agent** - Coordinate specialist teams
- **HITL Workflows** - Approval-based execution

## 🌟 **Why Choose This Library?**

- **🚀 Production Ready** - Battle-tested patterns and error handling
- **📦 Zero Setup** - Copy `src/` folder and import
- **⚡ Blazing Fast** - Groq's gpt-oss-120b is 10x faster than OpenAI
- **🔧 Extensible** - Easy to add tools, commands, and features
- **📚 Well Documented** - Comprehensive guides and examples
- **🎯 Focused** - Optimized for coding, math, and science tasks
- **🤝 Team Friendly** - Consistent patterns for collaborative development

## 🤝 **Contributing**

We welcome contributions! See [Contributing Guide](docs/contributing.md) for details.

- 🐛 **Bug Reports** - Open an issue
- ✨ **Feature Requests** - Suggest improvements  
- 🔧 **Pull Requests** - Add tools, fix bugs, improve docs
- 📚 **Documentation** - Help improve guides and examples

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **LangChain Team** - For the amazing framework
- **Groq** - For blazing-fast LLM inference
- **HuggingFace** - For free embedding models
- **Community** - For feedback and contributions

---

**🎯 Ready to build powerful AI agents? Start with the [Getting Started Guide](docs/getting-started.md)!** 🚀