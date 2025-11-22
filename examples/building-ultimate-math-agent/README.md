# Building Your Ultimate Math Agent - Complete Guide

**Step-by-step guide to creating your own specialized math agent using the LangChain Agent Base framework**

## 🎯 **What You'll Build**

An advanced mathematical assistant that:
- Starts with basic calculator functions
- Grows over time with new capabilities
- Has persistent conversation memory
- Includes custom math tools you create
- Deploys as a REST API
- Lives in its own GitHub repository

---

## 📁 **Project Structure**

Here's what your new project should look like:

```
my-ultimate-math-agent/
├── 📁 src/                           # Copy from langchain-agent-base
│   ├── base.py                       # Core Agent classes
│   ├── tools.py                      # Built-in tool collections
│   ├── commands.py                   # Command system
│   ├── protocol.py                   # Agent registration
│   ├── server.py                     # FastAPI server
│   ├── memory.py                     # Conversation memory
│   ├── storage.py                    # Qdrant storage
│   ├── rag.py                        # Document search
│   └── discovery.py                  # Auto-discovery
│
├── 📁 custom_tools/                  # Your custom math tools
│   ├── __init__.py
│   ├── calculus.py                   # Derivatives, integrals
│   ├── linear_algebra.py             # Vectors, matrices
│   ├── statistics.py                 # Stats and probability
│   ├── number_theory.py              # Prime numbers, factorization
│   └── symbolic_math.py              # Symbolic computation
│
├── 📁 agents/                        # Your agent definitions
│   ├── __init__.py
│   └── math_agent.py                 # Your ultimate math agent
│
├── 📁 tests/                         # Test your agent
│   ├── test_tools.py
│   └── test_agent.py
│
├── 📁 docs/                          # Your documentation
│   ├── usage.md
│   └── custom_tools.md
│
├── main.py                           # CLI entry point
├── pyproject.toml                    # Dependencies
├── README.md                         # Your project README
├── .env.example                      # Environment template
├── .gitignore                        # Git ignore file
└── LICENSE                           # Apache 2.0 license
```

---

## 🚀 **Step-by-Step Setup**

### **Step 1: Create Your New Repository**

```bash
# Create your project directory
mkdir my-ultimate-math-agent
cd my-ultimate-math-agent

# Initialize git repository
git init

# Create initial structure
mkdir -p src custom_tools agents tests docs
```

### **Step 2: Copy the LangChain Agent Base Framework**

```bash
# Clone the base framework (in a separate location)
cd ..
git clone https://github.com/BlueberryMathematician/langchain-agent-base.git

# Copy the src/ directory to your project
cp -r langchain-agent-base/src my-ultimate-math-agent/src

# Copy useful reference files
cp langchain-agent-base/pyproject.toml my-ultimate-math-agent/
cp langchain-agent-base/.gitignore my-ultimate-math-agent/
cp langchain-agent-base/main.py my-ultimate-math-agent/

cd my-ultimate-math-agent
```

### **Step 3: Set Up Python Environment**

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -e .

# Or install manually:
pip install langchain>=1.0.8 langchain-groq groq langchain-huggingface \
    sentence-transformers fastapi uvicorn qdrant-client semver
```

### **Step 4: Configure Environment**

Create `.env` file:

```bash
# .env
GROQ_API_KEY=your_groq_api_key_here

# Optional: LangSmith for debugging
# LANGSMITH_API_KEY=your_langsmith_key
# LANGSMITH_TRACING=true
```

Create `.env.example` (template for others):

```bash
# .env.example
GROQ_API_KEY=get_from_https://console.groq.com/
LANGSMITH_API_KEY=optional_for_debugging
```

---

## 🔧 **Building Your Math Agent**

### **File 1: `custom_tools/calculus.py`**

Create your first custom tool:

```python
"""
Custom Calculus Tools for Ultimate Math Agent
"""

from langchain_core.tools import tool
import sympy as sp

@tool
def derivative(expression: str, variable: str = "x") -> str:
    """
    Calculate the derivative of a mathematical expression.
    
    Args:
        expression: Math expression like "x**2 + 3*x + 2"
        variable: Variable to differentiate with respect to (default: x)
    
    Returns:
        The derivative as a string
    """
    try:
        x = sp.Symbol(variable)
        expr = sp.sympify(expression)
        result = sp.diff(expr, x)
        return f"d/d{variable}({expression}) = {result}"
    except Exception as e:
        return f"Error calculating derivative: {str(e)}"

@tool
def integrate(expression: str, variable: str = "x") -> str:
    """
    Calculate the indefinite integral of a mathematical expression.
    
    Args:
        expression: Math expression like "x**2 + 3*x + 2"
        variable: Variable to integrate with respect to (default: x)
    
    Returns:
        The integral as a string
    """
    try:
        x = sp.Symbol(variable)
        expr = sp.sympify(expression)
        result = sp.integrate(expr, x)
        return f"∫({expression}) d{variable} = {result} + C"
    except Exception as e:
        return f"Error calculating integral: {str(e)}"

@tool
def definite_integral(expression: str, variable: str, lower: float, upper: float) -> str:
    """
    Calculate the definite integral of a mathematical expression.
    
    Args:
        expression: Math expression
        variable: Variable to integrate
        lower: Lower bound
        upper: Upper bound
    
    Returns:
        The definite integral value
    """
    try:
        var = sp.Symbol(variable)
        expr = sp.sympify(expression)
        result = sp.integrate(expr, (var, lower, upper))
        return f"∫[{lower}, {upper}]({expression}) d{variable} = {result}"
    except Exception as e:
        return f"Error calculating definite integral: {str(e)}"
```

### **File 2: `custom_tools/__init__.py`**

Export your tools:

```python
"""
Custom Math Tools Collection
"""

from custom_tools.calculus import derivative, integrate, definite_integral

# Add more imports as you create more tools
# from custom_tools.statistics import mean, std_dev, correlation
# from custom_tools.linear_algebra import dot_product, cross_product

def get_calculus_tools():
    """Get all calculus tools."""
    return [derivative, integrate, definite_integral]

def get_all_custom_tools():
    """Get all custom math tools."""
    return get_calculus_tools()
    # Add more as you build them:
    # return [
    #     *get_calculus_tools(),
    #     *get_statistics_tools(),
    #     *get_linear_algebra_tools(),
    # ]
```

### **File 3: `agents/math_agent.py`**

Create your ultimate math agent:

```python
"""
Ultimate Math Agent - Your Custom Mathematical Assistant
"""

from src.base import Agent
from src.tools import get_math_tools
from src.protocol import register_agent, AgentStatus
from src.commands import create_math_commands
from custom_tools import get_all_custom_tools

@register_agent(
    name="ultimate_math",
    version="1.0.0",
    domain="mathematics",
    category="specialist",
    description="Ultimate mathematical assistant with calculus, algebra, and custom tools",
    author="Your Name",
    status=AgentStatus.PRODUCTION
)
class UltimateMathAgent(Agent):
    """
    The ultimate mathematical assistant combining:
    - Built-in math tools from the framework
    - Your custom calculus, statistics, and algebra tools
    - Conversation memory for context
    - Command system for fast operations
    """
    
    def __init__(self, enable_memory: bool = True, **kwargs):
        # Enhanced system prompt
        super().__init__(
            system_prompt="""I am the Ultimate Math Agent, a specialized mathematical assistant.
            
            I can help with:
            - Basic arithmetic and advanced calculations
            - Calculus: derivatives, integrals, limits
            - Linear algebra: matrices, vectors, eigenvalues
            - Statistics: mean, variance, probability
            - Number theory: primes, factorization, GCD
            - Symbolic mathematics and equation solving
            
            I show my work step-by-step and explain mathematical concepts clearly.
            I remember our conversation history to provide contextual assistance.""",
            enable_memory=enable_memory,
            enable_commands=True,
            **kwargs
        )
        
        # Add built-in math tools from the framework
        self.add_tools(get_math_tools())
        
        # Add your custom tools
        self.add_tools(get_all_custom_tools())
        
        # Add math commands for fast operations
        for cmd in create_math_commands():
            self.add_command(cmd)
        
        print(f"✅ Ultimate Math Agent initialized with {len(self.tools)} tools")
        print(f"📊 Available tools: {self.list_tools()}")
        print(f"⚡ Available commands: {self.list_commands()}")


def create_ultimate_math_agent(**kwargs):
    """Factory function for easy agent creation."""
    return UltimateMathAgent(**kwargs)


# Example usage
if __name__ == "__main__":
    # Create the agent
    agent = create_ultimate_math_agent()
    
    # Test basic functionality
    print("\n🧪 Testing Ultimate Math Agent:")
    
    test_queries = [
        "Calculate the derivative of x^3 + 2x^2 - 5x + 1",
        "What's the integral of sin(x)?",
        "Solve the quadratic equation x^2 - 5x + 6 = 0",
        "Calculate the determinant of [[1,2],[3,4]]"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        response = agent.chat(query)
        print(f"Agent: {response}")
```

### **File 4: `main.py`**

Your CLI entry point:

```python
"""
Ultimate Math Agent CLI
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.math_agent import create_ultimate_math_agent
from src.server import run_protocol_server
from src.discovery import auto_discover_all
import argparse

def main():
    parser = argparse.ArgumentParser(description="Ultimate Math Agent CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Chat command
    chat_parser = subparsers.add_parser('chat', help='Chat with the math agent')
    chat_parser.add_argument('--memory', action='store_true', help='Enable conversation memory')
    
    # Server command
    server_parser = subparsers.add_parser('server', help='Start API server')
    server_parser.add_argument('--host', default='0.0.0.0', help='Server host')
    server_parser.add_argument('--port', type=int, default=8000, help='Server port')
    
    # Discover command
    discover_parser = subparsers.add_parser('discover', help='Discover all agents and tools')
    
    args = parser.parse_args()
    
    if args.command == 'chat':
        # Interactive chat session
        agent = create_ultimate_math_agent(enable_memory=args.memory)
        print("🤖 Ultimate Math Agent - Interactive Chat")
        print("Type 'exit' or 'quit' to end the session")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                if user_input.lower() in ['exit', 'quit']:
                    print("Goodbye! 👋")
                    break
                
                if not user_input:
                    continue
                
                response = agent.chat(user_input)
                print(f"\nAgent: {response}")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"\nError: {e}")
    
    elif args.command == 'server':
        # Start API server
        print(f"🚀 Starting Ultimate Math Agent API Server")
        print(f"📍 http://{args.host}:{args.port}")
        print(f"📚 API docs: http://{args.host}:{args.port}/docs")
        
        # Auto-discover agents
        auto_discover_all()
        
        # Run server
        run_protocol_server(host=args.host, port=args.port)
    
    elif args.command == 'discover':
        # Discover all agents and tools
        results = auto_discover_all()
        print(f"✅ Discovery complete!")
        print(f"📋 Tools: {len(results['tools'])}")
        print(f"⚡ Commands: {len(results['commands'])}")
        print(f"🤖 Agents: {len(results['agents'])}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

### **File 5: `pyproject.toml`**

Your project dependencies:

```toml
[project]
name = "ultimate-math-agent"
version = "1.0.0"
description = "Ultimate mathematical AI agent with custom tools"
readme = "README.md"
requires-python = ">=3.11"
authors = [
    {name = "Your Name"}
]
license = {text = "Apache-2.0"}

dependencies = [
    # Core LangChain
    "langchain>=1.0.8",
    "langgraph>=1.0.3",
    "langchain-groq>=0.2.0",
    "groq>=0.11.0",
    "langchain-huggingface>=0.1.0",
    
    # Protocol & API
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "pydantic>=2.0.0",
    
    # Storage
    "qdrant-client>=1.16.0",
    "sentence-transformers>=2.2.2",
    
    # Math tools
    "sympy>=1.12",
    "numpy>=1.24.0",
    "scipy>=1.11.0",
]

[project.scripts]
math-agent = "main:main"
```

### **File 6: `README.md`**

Your project README:

```markdown
# Ultimate Math Agent

Advanced mathematical AI assistant built with LangChain Agent Base.

## Features

- 🧮 Calculus: derivatives, integrals, limits
- 📊 Statistics: mean, variance, distributions
- 🔢 Linear Algebra: matrices, vectors, transformations
- 🔐 Number Theory: primes, factorization, modular arithmetic
- 🧠 Conversation Memory: remembers context across sessions
- ⚡ Fast Commands: direct tool execution
- 🌐 REST API: auto-generated FastAPI endpoints

## Installation

\`\`\`bash
# Clone the repository
git clone https://github.com/yourusername/ultimate-math-agent.git
cd ultimate-math-agent

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Set up environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
\`\`\`

## Usage

### Interactive Chat

\`\`\`bash
python main.py chat --memory
\`\`\`

### Start API Server

\`\`\`bash
python main.py server
# Visit http://localhost:8000/docs for API documentation
\`\`\`

### Python Integration

\`\`\`python
from agents.math_agent import create_ultimate_math_agent

agent = create_ultimate_math_agent()
response = agent.chat("Calculate the derivative of x^2 + 3x + 2")
print(response)
\`\`\`

## Adding Custom Tools

1. Create new tool file in `custom_tools/`
2. Import and export in `custom_tools/__init__.py`
3. Tools automatically available to the agent!

## License

Apache 2.0 - See LICENSE file
```

---

## 🎯 **How to Use in Your Project**

### **Quick Start (3 steps)**

```bash
# 1. Create project and copy framework
mkdir my-ultimate-math-agent && cd my-ultimate-math-agent
cp -r ../langchain-agent-base/src ./src

# 2. Install dependencies
python -m venv .venv && source .venv/bin/activate
pip install langchain>=1.0.8 langchain-groq groq fastapi uvicorn qdrant-client

# 3. Create your agent
# (Use the code examples above)
```

### **Daily Development Workflow**

1. **Add a new tool**: Create file in `custom_tools/`, write `@tool` function
2. **Test the tool**: Import in agent, chat with it
3. **Add to collection**: Export in `custom_tools/__init__.py`
4. **It works!**: Agent automatically has access

### **Growing Your Agent Over Time**

```python
# Version 1.0: Basic calculus
@register_agent("ultimate_math", version="1.0.0")
class UltimateMathAgent:
    # Just derivatives and integrals

# Version 2.0: Add statistics
@register_agent("ultimate_math", version="2.0.0")  
class UltimateMathAgent:
    # Add mean, variance, correlation

# Version 3.0: Add linear algebra
@register_agent("ultimate_math", version="3.0.0")
class UltimateMathAgent:
    # Add matrix operations, eigenvalues
```

---

## 🚀 **Deployment Options**

### **Option 1: Local Use**

```python
from agents.math_agent import create_ultimate_math_agent

agent = create_ultimate_math_agent()
response = agent.chat("Your math question")
```

### **Option 2: REST API**

```bash
python main.py server
# API available at http://localhost:8000
```

```python
import requests

response = requests.post("http://localhost:8000/chat", json={
    "agent_name": "ultimate_math",
    "message": "Calculate derivative of x^2"
})
print(response.json()["response"])
```

### **Option 3: Web Application**

```python
# In your Flask/Django/FastAPI app
from agents.math_agent import create_ultimate_math_agent

agent = create_ultimate_math_agent(enable_memory=True)

@app.post("/math/solve")
def solve_math(request):
    user_query = request.json["query"]
    session_id = request.json["session_id"]
    
    # Agent remembers conversation per user
    agent.memory_session_id = session_id
    response = agent.chat(user_query)
    
    return {"response": response}
```

---

## 💡 **Key Concepts**

### **1. The Framework Does the Heavy Lifting**

You DON'T need to write:
- ❌ Agent loop logic
- ❌ Memory management
- ❌ API server code
- ❌ Tool registration
- ❌ Command parsing

You ONLY write:
- ✅ Your custom tools (`@tool` functions)
- ✅ Your agent definition (system prompt + tools)
- ✅ Your business logic

### **2. Tools are Just Python Functions**

```python
@tool
def my_math_tool(input: str) -> str:
    """What the tool does (LLM reads this)."""
    # Your logic here
    return result
```

That's it! The framework handles:
- Calling the tool when needed
- Passing parameters
- Error handling
- Making it available via API

### **3. Memory is Automatic**

```python
# Enable memory when creating agent
agent = UltimateMathAgent(enable_memory=True)

# Conversation 1
agent.chat("My name is Alice")

# Conversation 2 (later)
agent.chat("What's my name?")  # Agent remembers: "Alice"
```

### **4. Commands for Speed**

```python
# Slow: Goes through LLM
response = agent.chat("Calculate 2 + 2")

# Fast: Direct tool execution
result = agent.execute_command("/calc", expression="2 + 2")
```

---

## 🎓 **Learning Path**

1. **Week 1**: Copy framework, create basic agent with 1 custom tool
2. **Week 2**: Add 5 more tools, test with different queries
3. **Week 3**: Add conversation memory, enable commands
4. **Week 4**: Deploy API server, integrate with your app
5. **Week 5+**: Keep adding tools as you need them!

---

## 🤝 **Getting Help**

- **Framework Docs**: `langchain-agent-base/docs/`
- **Examples**: `langchain-agent-base/examples/`
- **Code Reference**: Look at `src/base.py` for Agent class

---

## ✅ **You're Ready!**

The beauty of this system:
- **Start simple**: Basic agent + 1 tool
- **Grow naturally**: Add tools as needed
- **No rewrites**: Same code structure scales
- **Memory included**: Conversations persist automatically
- **API ready**: Deploy when you're ready

**Now go build your ultimate math agent! 🚀**
