# How to Use LangChain Agent Base in Your Project - Simple Explanation

## 🎯 **The Big Picture**

Think of the LangChain Agent Base as a **pre-built car engine**. You don't need to build the engine from scratch - you just need to:
1. **Copy the engine** (the `src/` folder)
2. **Add your custom parts** (your math tools)
3. **Configure it** (tell it what you want to do)
4. **Drive it** (use your agent!)

---

## 🚗 **Step-by-Step: Building Your Ultimate Math Agent**

### **Step 1: Create Your New Project** (2 minutes)

```bash
# Create a new folder for your project
mkdir my-ultimate-math-agent
cd my-ultimate-math-agent

# Create the structure
mkdir src custom_tools agents
```

**What you have now:**
```
my-ultimate-math-agent/
├── src/              ← Will hold the framework
├── custom_tools/     ← Your custom math tools go here
└── agents/           ← Your agent definition goes here
```

---

### **Step 2: Copy the Framework** (1 minute)

```bash
# Clone this repo somewhere
cd ..
git clone https://github.com/BlueberryMathematician/langchain-agent-base.git

# Copy the src/ folder to your project
cp -r langchain-agent-base/src my-ultimate-math-agent/src
```

**What you copied:**
- `base.py` - The Agent class (the brain)
- `tools.py` - Pre-built math/science/coding tools
- `memory.py` - Conversation memory system
- `protocol.py` - Registration and versioning
- All the other framework files

**Important:** You're NOT copying the examples or docs - just the `src/` folder!

---

### **Step 3: Install Dependencies** (2 minutes)

```bash
cd my-ultimate-math-agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install required packages
pip install langchain>=1.0.8 langchain-groq groq langchain-huggingface \
    sentence-transformers fastapi uvicorn qdrant-client
```

---

### **Step 4: Get Your API Key** (1 minute)

1. Go to https://console.groq.com/
2. Sign up (free)
3. Get your API key
4. Create `.env` file:

```bash
# .env
GROQ_API_KEY=your_actual_key_here
```

---

### **Step 5: Create Your First Custom Tool** (5 minutes)

Create `custom_tools/calculus.py`:

```python
from langchain_core.tools import tool

@tool
def derivative(expression: str) -> str:
    """Calculate the derivative of a math expression."""
    import sympy as sp
    x = sp.Symbol('x')
    expr = sp.sympify(expression)
    result = sp.diff(expr, x)
    return f"d/dx({expression}) = {result}"
```

Create `custom_tools/__init__.py`:

```python
from custom_tools.calculus import derivative

def get_all_custom_tools():
    return [derivative]
```

**That's it!** You've created a custom tool.

---

### **Step 6: Create Your Agent** (5 minutes)

Create `agents/math_agent.py`:

```python
from src.base import Agent
from src.tools import get_math_tools
from custom_tools import get_all_custom_tools

class UltimateMathAgent(Agent):
    def __init__(self):
        super().__init__(
            system_prompt="I am an ultimate math assistant.",
            enable_memory=True
        )
        
        # Add built-in tools from the framework
        self.add_tools(get_math_tools())
        
        # Add YOUR custom tools
        self.add_tools(get_all_custom_tools())

def create_ultimate_math_agent():
    return UltimateMathAgent()
```

---

### **Step 7: Use Your Agent!** (Now!)

Create `test_agent.py`:

```python
from agents.math_agent import create_ultimate_math_agent

# Create your agent
agent = create_ultimate_math_agent()

# Use it!
response = agent.chat("Calculate the derivative of x^2 + 3x")
print(response)

# It remembers context!
response2 = agent.chat("What did we just calculate?")
print(response2)
```

Run it:
```bash
python test_agent.py
```

**🎉 THAT'S IT! You have a working custom math agent!**

---

## 🔄 **Daily Workflow: Adding More Tools**

Every day/week, you can add more capabilities:

### **Monday: Add Integration Tool**

Create `custom_tools/calculus.py` (add to existing file):

```python
@tool
def integrate(expression: str) -> str:
    """Calculate the integral."""
    import sympy as sp
    x = sp.Symbol('x')
    expr = sp.sympify(expression)
    result = sp.integrate(expr, x)
    return f"∫({expression}) dx = {result} + C"
```

Update `custom_tools/__init__.py`:

```python
from custom_tools.calculus import derivative, integrate

def get_all_custom_tools():
    return [derivative, integrate]  # Add new tool here
```

**Your agent NOW has integration!** No need to change agent code!

### **Tuesday: Add Statistics**

Create `custom_tools/statistics.py`:

```python
@tool
def calculate_mean(numbers: str) -> str:
    """Calculate the mean of comma-separated numbers."""
    nums = [float(x) for x in numbers.split(',')]
    mean = sum(nums) / len(nums)
    return f"Mean: {mean}"
```

Update `__init__.py`, and boom - your agent can do statistics!

---

## 🎯 **The Pattern (This is the Key!)**

```
1. Write a @tool function
2. Export it in __init__.py
3. Agent automatically has access
```

You DON'T need to:
- ❌ Modify the agent loop
- ❌ Handle memory yourself
- ❌ Write API endpoints
- ❌ Deal with LLM communication

The framework does ALL of that!

---

## 📊 **What You Get for Free**

When you use this framework:

✅ **Conversation Memory**
```python
agent = Agent(enable_memory=True)
# Agent remembers everything in the conversation
```

✅ **Fast Commands**
```python
agent.enable_commands()
result = agent.execute_command("/calc", expression="2+2")
# Skips LLM, executes directly
```

✅ **REST API** (Optional)
```python
# Just run this:
python -m src.server
# Your agent is now available at http://localhost:8000
```

✅ **Versioning**
```python
@register_agent("my_agent", version="1.0.0")
class MyAgent(Agent):
    pass
# Framework tracks versions automatically
```

---

## 🚀 **From Zero to Production**

### **Week 1: Start Small**
```python
# 1 agent + 1 custom tool
@tool
def my_first_tool(x: str) -> str:
    return f"You said: {x}"
```

### **Week 2: Add More Tools**
```python
# 1 agent + 5 custom tools
# Just keep adding @tool functions!
```

### **Week 3: Add Memory**
```python
agent = Agent(enable_memory=True)
# Conversations persist automatically
```

### **Week 4: Deploy API**
```bash
python -m src.server
# Your agent is now a web service!
```

### **Month 2+: Keep Growing**
- Add more specialized tools as you need them
- Create multiple agents for different domains
- Build a library of reusable tools
- Never rewrite the core framework!

---

## 💡 **Key Insights**

### **1. The Framework is Like a Library**

```python
# You import what you need
from src.base import Agent  # The agent class
from src.tools import get_math_tools  # Pre-built tools
from src.memory import get_memory_manager  # Memory system
```

### **2. Tools are Plug-and-Play**

```python
# This tool...
@tool
def my_tool(x: str) -> str:
    return x.upper()

# ...automatically works with ANY agent
agent.add_tool(my_tool)
```

### **3. Memory is Automatic**

```python
# Enable once
agent = Agent(enable_memory=True)

# It just works forever
agent.chat("My name is Alice")  # Stored
agent.chat("What's my name?")   # Remembers "Alice"
```

### **4. You Only Write Business Logic**

**You write:**
- ✅ Custom tools (your math formulas)
- ✅ Agent prompts (what it should do)
- ✅ Tool selection (which tools to include)

**Framework handles:**
- ✅ Agent loop
- ✅ Memory management
- ✅ API generation
- ✅ Error handling
- ✅ Tool calling
- ✅ LLM communication

---

## 🎓 **Mental Model**

Think of it like building with LEGO:

1. **Framework = LEGO Base** (the plate everything sits on)
2. **Pre-built Tools = LEGO sets** (car kit, house kit, etc.)
3. **Your Custom Tools = Custom LEGO pieces** (you 3D print your own)
4. **Your Agent = Your Creation** (combine everything how you want)

You don't build LEGO bricks from scratch - you use them to build cool stuff!

---

## ✅ **Summary: Your 3-Step Process**

```bash
# 1. Copy framework
cp -r langchain-agent-base/src my-project/src

# 2. Write custom tools
# Create custom_tools/my_tool.py with @tool functions

# 3. Create agent
# Create agents/my_agent.py that imports and adds tools
```

**That's literally it!**

---

## 🎯 **Next Steps**

1. **Read**: `examples/building-ultimate-math-agent/README.md` (comprehensive guide)
2. **Look at**: `examples/building-ultimate-math-agent/example_math_agent.py` (working code)
3. **Try**: `python quick_start.py my-agent` (automatic project setup)
4. **Reference**: Original `docs/` folder (detailed API documentation)

---

## ❤️ **The Beauty of This System**

- **Start simple**: 1 agent, 1 tool, 20 minutes
- **Grow naturally**: Add 1 tool at a time
- **Never rewrite**: Same structure works forever
- **Scale easily**: From toy to production without changes

**You focus on WHAT the agent should do, not HOW it works internally!**

That's the power of this framework. 🚀
