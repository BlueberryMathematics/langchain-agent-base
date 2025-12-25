# Toolbox System - Dynamic Tool Management

## 🎯 Overview

The Toolbox System is a comprehensive framework for **dynamically creating, storing, validating, and managing tools** for your LangChain agents. It supports:

- ✅ **LLM-Assisted Tool Generation** - Generate tools from natural language descriptions
- ✅ **Manual Tool Creation** - Add tools from code strings or function objects  
- ✅ **Persistent Storage** - Tools saved as Python files, organized by category
- ✅ **Validation & Safety** - Automatic code validation and security checks
- ✅ **Version Control** - Track tool versions and improvements
- ✅ **Testing Framework** - Built-in test runner for tools
- ✅ **Agent Integration** - Seamlessly load tools into agents
- ✅ **Duplicate Detection** - Prevent duplicate tools using code hashing
- ✅ **Category Organization** - Math, Science, Coding, Business, Custom, Generated
- ✅ **Export & Sharing** - Export tool collections to distributable files

---

## 🚀 Quick Start

### 1. Basic Usage

```python
from src.toolbox import ToolboxManager

# Initialize toolbox
toolbox = ToolboxManager()

# Add a tool from code
tool_code = '''
@tool
def my_calculator(x: int, y: int) -> str:
    """Add two numbers."""
    return f"{x} + {y} = {x + y}"
'''

success, message, tool = toolbox.add_tool_from_code(
    tool_code,
    category="math",
    author="me"
)

# Use the tool
result = tool.invoke({'x': 5, 'y': 3})
print(result)  # "5 + 3 = 8"
```

### 2. LLM-Assisted Generation

```python
from src.tool_generator import generate_tool

# Generate a tool from natural language
success, message, tool = generate_tool(
    description="Calculate the median of a list of numbers",
    category="math"
)

# Tool is automatically created, validated, and saved!
```

### 3. Agent Integration

```python
from src.base import Agent

agent = Agent()

# Load tools from toolbox
agent.load_tools_from_toolbox(category="math")

# Or generate a new tool on-the-fly
agent.generate_and_add_tool(
    description="Calculate factorial of a number",
    category="math"
)

# Use in conversation
response = agent.chat("What's the factorial of 5?")
```

---

## 📋 Core Components

### 1. ToolboxManager

Main class for tool management.

```python
from src.toolbox import ToolboxManager

toolbox = ToolboxManager(
    toolbox_dir="my_toolbox",       # Where to store tools
    registry_file="registry.json",  # Metadata storage
    auto_load=True                  # Load existing tools on init
)
```

**Key Methods:**

```python
# Add tool from code
success, msg, tool = toolbox.add_tool_from_code(code, category="math")

# Add tool from function
success, msg = toolbox.add_tool_from_function(my_tool, category="math")

# Get tools
tool = toolbox.get_tool("tool_name")
math_tools = toolbox.get_tools_by_category("math")
llm_tools = toolbox.get_tools_by_author("llm")
all_tools = toolbox.get_all_tools()

# List tools with metadata
tools = toolbox.list_tools(category="math")

# Test a tool
results = toolbox.test_tool("tool_name", test_cases=[
    {'input': {'x': 5}, 'expected': '5'}
])

# Remove tool
success, msg = toolbox.remove_tool("tool_name")

# Export tools
toolbox.export_tools("output.py", category="math")
```

### 2. ToolGenerator

LLM-powered tool generation.

```python
from src.tool_generator import ToolGenerator

generator = ToolGenerator(
    model_name="openai/gpt-oss-120b",
    temperature=0.2
)
```

**Key Methods:**

```python
# Generate a single tool
success, msg, tool = generator.generate_tool(
    description="What the tool should do",
    category="math",
    tool_name="specific_name",      # Optional
    examples=["example 1", "..."],  # Optional
    dependencies=["numpy", "..."]   # Optional
)

# Generate tool collection
success, msg, tools = generator.generate_tool_collection(
    domain="statistics",
    num_tools=5
)

# Improve existing tool
success, msg, tool = generator.improve_tool(
    tool_name="existing_tool",
    improvements="Make it faster and add error handling"
)
```

### 3. ToolAssistant

Interactive tool management helper.

```python
from src.tool_generator import ToolAssistant

assistant = ToolAssistant()
```

**Key Methods:**

```python
# Suggest tools for a task
suggestions = assistant.suggest_tools_for_task(
    "I need to analyze statistical data"
)

# Create tool for agent
success, msg, tool = assistant.create_tool_for_agent(
    agent=my_agent,
    tool_description="Calculate standard deviation",
    add_to_agent=True
)

# Batch create tools
results = assistant.batch_create_tools([
    "Calculate mean",
    "Calculate mode",
    "Calculate range"
], category="math")
```

### 4. ToolValidator

Validates and ensures tool safety.

```python
from src.toolbox import ToolValidator

is_valid, message, ast_tree = ToolValidator.validate_code(code)
tool_info = ToolValidator.extract_tool_info(code)
```

**Validation Checks:**
- ✅ Syntax validation
- ✅ @tool decorator presence
- ✅ Forbidden imports (subprocess, eval, exec)
- ✅ Dangerous operations
- ✅ Parameter extraction
- ✅ Dependency analysis

---

## 🗂️ Tool Organization

### Categories

Tools are organized into categories:

- **math** - Mathematical operations (calculus, algebra, statistics)
- **science** - Scientific calculations (physics, chemistry)
- **coding** - Programming utilities (regex, json, analysis)
- **business** - Business logic tools
- **custom** - User-created custom tools
- **generated** - LLM-generated tools

### Storage Structure

```
toolbox/
├── math/
│   ├── fibonacci.py
│   ├── factorial.py
│   └── median.py
├── science/
│   ├── temperature_converter.py
│   └── unit_converter.py
├── generated/
│   └── llm_created_tools.py
└── tool_registry.json  # Metadata for all tools
```

### Tool Metadata

Each tool has comprehensive metadata:

```python
{
    "name": "calculate_median",
    "description": "Calculate median of numbers",
    "category": "math",
    "author": "llm",
    "version": "1.0.0",
    "created_at": "2024-01-01T12:00:00",
    "function_signature": "calculate_median(numbers: str)",
    "code_hash": "abc123...",
    "parameters": {"numbers": "str"},
    "tags": ["statistics", "median"],
    "tested": true,
    "dependencies": ["math"]
}
```

---

## 🛡️ Safety & Validation

### Forbidden Operations

The validator blocks:
- ❌ `subprocess` - Shell command execution
- ❌ `eval`/`exec` - Arbitrary code execution
- ❌ `__import__` - Dynamic imports
- ❌ Dangerous file operations

### Allowed Imports

Safe libraries are whitelisted:
- ✅ `math`, `json`, `re`, `typing`, `dataclasses`
- ✅ `datetime`, `collections`
- ✅ `sympy`, `numpy`, `scipy`, `pandas`
- ✅ `langchain_core.tools`
- ✅ `requests` (for API calls)

### Code Requirements

All tools must:
1. Use `@tool` decorator
2. Have type hints
3. Include docstring
4. Handle errors gracefully (return strings, not exceptions)
5. Be self-contained

---

## 🧪 Testing Tools

### Built-in Test Runner

```python
test_results = toolbox.test_tool("my_tool", [
    {
        'input': {'x': 5, 'y': 3},
        'expected': '8'
    },
    {
        'input': {'x': 10, 'y': -2},
        'expected': '8'
    }
])

print(f"Passed: {test_results['passed']}/{test_results['total_tests']}")
```

### Test Results

```python
{
    'tool_name': 'my_tool',
    'total_tests': 2,
    'passed': 2,
    'failed': 0,
    'test_results': [
        {
            'test_number': 1,
            'passed': True,
            'input': {'x': 5, 'y': 3},
            'expected': '8',
            'actual': 'Result: 8'
        }
    ]
}
```

---

## 🔄 Complete Workflow Example

```python
from src.toolbox import get_toolbox
from src.tool_generator import generate_tool
from src.base import Agent

# 1. Generate a tool
print("📝 Generating tool...")
success, message, tool = generate_tool(
    description="Calculate prime factors of a number",
    category="math"
)

if not success:
    print(f"Failed: {message}")
    exit()

print(f"✅ Generated: {tool.name}")

# 2. Test the tool
print("\n🧪 Testing tool...")
toolbox = get_toolbox()
results = toolbox.test_tool(tool.name, [
    {'input': {'number': 12}, 'expected': '2, 3'},
    {'input': {'number': 17}, 'expected': '17'}
])

print(f"Tests: {results['passed']}/{results['total_tests']} passed")

# 3. Use in agent
print("\n🤖 Using in agent...")
agent = Agent()
agent.add_tool(tool)

response = agent.chat("What are the prime factors of 84?")
print(f"Agent: {response}")

# 4. Load more tools
print("\n📦 Loading related tools...")
agent.load_tools_from_toolbox(category="math")

# 5. Generate more tools on-the-fly
print("\n⚡ Generating additional tool...")
agent.generate_and_add_tool(
    description="Check if a number is perfect square",
    category="math"
)

# 6. Export tools for reuse
print("\n💾 Exporting tools...")
toolbox.export_tools("my_math_tools.py", category="math")

print("\n✅ Complete!")
```

---

## 🎯 Use Cases

### 1. Math Agent Expansion

```python
# Start with basic math agent
agent = create_math_agent()

# Add specialized tools dynamically
agent.generate_and_add_tool(
    "Calculate eigenvalues of a matrix",
    category="math"
)

agent.generate_and_add_tool(
    "Solve differential equations numerically",
    category="math"
)
```

### 2. Domain-Specific Toolbox

```python
# Create finance toolbox
generator = ToolGenerator()

success, msg, tools = generator.generate_tool_collection(
    domain="financial analysis",
    num_tools=10
)

# All tools automatically saved and ready to use
finance_agent = Agent()
finance_agent.load_tools_from_toolbox(tags=["finance"])
```

### 3. Collaborative Tool Library

```python
# Team member 1 creates tools
toolbox1 = ToolboxManager("shared_toolbox")
toolbox1.add_tool_from_code(code1, author="alice")

# Team member 2 adds more
toolbox2 = ToolboxManager("shared_toolbox")
toolbox2.add_tool_from_code(code2, author="bob")

# Everyone can use all tools
agent = Agent()
agent.load_tools_from_toolbox()  # Loads all team tools
```

### 4. Tool Evolution

```python
# Version 1.0 - basic tool
toolbox.add_tool_from_code(basic_code, version="1.0.0")

# Version 2.0 - improved by LLM
generator.improve_tool(
    "my_tool",
    improvements="Add caching and better error messages"
)

# Version history tracked automatically
```

---

## 🚀 Advanced Features

### Duplicate Detection

```python
# Identical tools detected by code hash
success, msg, _ = toolbox.add_tool_from_code(code1)
success, msg, _ = toolbox.add_tool_from_code(code1)  # Rejected!
# Message: "Identical tool already exists as 'tool_name'"
```

### Tool Tagging

```python
# Add tools with tags
toolbox.add_tool_from_code(
    code,
    tags=["statistics", "descriptive", "advanced"]
)

# Find tools by tags
tools = toolbox.get_tools_by_tags(["statistics", "advanced"])
```

### Tool Export

```python
# Export specific category
toolbox.export_tools("math_tools.py", category="math")

# Export creates a distributable file:
"""
from langchain_core.tools import tool

# fibonacci
@tool
def fibonacci(n: int) -> str:
    ...

# factorial
@tool  
def factorial(n: int) -> str:
    ...

def get_exported_tools():
    return [fibonacci, factorial]
"""
```

---

## 📚 Best Practices

### 1. Tool Design

- ✅ Single responsibility per tool
- ✅ Clear, descriptive names
- ✅ Comprehensive docstrings
- ✅ Type hints for all parameters
- ✅ Return strings (for LLM consumption)
- ✅ Handle all edge cases
- ✅ Include usage examples in docstring

### 2. Organization

- 📁 Use appropriate categories
- 🏷️ Tag tools for discoverability
- 👤 Set meaningful author names
- 📝 Write clear descriptions
- 🧪 Test before deploying

### 3. Safety

- 🛡️ Never use `eval` or `exec`
- 🚫 Avoid file system operations unless necessary
- ⚠️ Validate all user inputs
- 🔒 Use try-except blocks
- ✅ Return error messages, don't raise exceptions

### 4. Performance

- ⚡ Keep tools focused and fast
- 💾 Cache expensive computations
- 🎯 Limit tool complexity
- 📊 Test with various inputs

---

## 🐛 Troubleshooting

### Tool Generation Fails

```python
# Check validation errors
is_valid, message, tree = ToolValidator.validate_code(code)
if not is_valid:
    print(f"Validation error: {message}")
```

### Tool Not Loading

```python
# Check if tool exists
tool = toolbox.get_tool("tool_name")
if tool is None:
    print("Tool not found in toolbox")

# List all available tools
tools = toolbox.list_tools()
print([t['name'] for t in tools])
```

### Agent Can't Use Tool

```python
# Verify tool is added to agent
print(agent.list_tools())  # Should include your tool

# Reload agent
agent._rebuild_agent()
```

---

## 🎉 Examples

See `examples/toolbox_demo.py` for comprehensive demonstrations including:

1. Basic toolbox operations
2. LLM-assisted tool generation
3. Agent integration
4. Tool validation and safety
5. Advanced management features
6. Complete workflows

Run the demo:

```bash
python examples/toolbox_demo.py
```

---

## 🔗 Integration with Framework

The toolbox system integrates seamlessly with the existing framework:

- **Agents** - Load tools via `load_tools_from_toolbox()` or `generate_and_add_tool()`
- **Discovery** - Automatically discover tools in toolbox directories
- **Protocol** - Register tools with the protocol system
- **Server** - Expose toolbox tools via REST API
- **RAG** - Use tool documentation in retrieval

---

## 📖 API Reference

### ToolboxManager

```python
class ToolboxManager:
    def __init__(toolbox_dir, registry_file, auto_load)
    def add_tool_from_code(code, category, author, version, tags, force) -> (bool, str, Callable)
    def add_tool_from_function(tool_func, category, author, version, tags) -> (bool, str)
    def get_tool(tool_name) -> Callable
    def get_tools_by_category(category) -> List[Callable]
    def get_tools_by_tags(tags) -> List[Callable]
    def get_tools_by_author(author) -> List[Callable]
    def get_all_tools() -> List[Callable]
    def list_tools(category, author) -> List[Dict]
    def remove_tool(tool_name) -> (bool, str)
    def test_tool(tool_name, test_cases) -> Dict
    def export_tools(output_file, category)
```

### ToolGenerator

```python
class ToolGenerator:
    def __init__(model_name, temperature, toolbox)
    def generate_tool(description, category, tool_name, examples, dependencies, return_code_only) -> (bool, str, Callable)
    def improve_tool(tool_name, improvements) -> (bool, str, Callable)
    def generate_tool_collection(domain, num_tools, specific_tools) -> (bool, str, List[Callable])
```

### ToolAssistant

```python
class ToolAssistant:
    def __init__(toolbox)
    def suggest_tools_for_task(task_description) -> List[Dict]
    def create_tool_for_agent(agent, tool_description, category, add_to_agent) -> (bool, str, Callable)
    def batch_create_tools(tool_descriptions, category) -> Dict
```

---

## 🤝 Contributing

The toolbox system is designed to be extended! Consider contributing:

- 🧪 More test cases
- 🔧 Additional validation rules
- 🎨 Better categorization
- 📊 Tool analytics
- 🌐 Remote toolbox sync
- 🔍 Semantic tool search

---

## 📄 License

Apache 2.0 - Same as the main framework

---

**Built with ❤️ for the LangChain Agent Base framework**
