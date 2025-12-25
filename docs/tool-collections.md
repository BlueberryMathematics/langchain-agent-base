# Tool Collections

Complete reference for all available tools organized by domain. Each tool collection provides specialized capabilities that can be added to any agent.

## 🧮 Math Tools (`get_math_tools()`)

Mathematical computation and problem-solving tools.

### Advanced Calculator
```python
from src.tools import advanced_calculator

# Complex mathematical expressions
result = advanced_calculator("sqrt(144) + log(100, 10)")
# Returns: "14.0"

# Scientific notation and constants
result = advanced_calculator("2 * pi * e")
# Returns: "17.077..."
```

**Features:**
- Basic arithmetic: `+`, `-`, `*`, `/`, `**` (power)
- Functions: `sqrt()`, `log()`, `sin()`, `cos()`, `tan()`, `abs()`
- Constants: `pi`, `e`
- Parentheses and complex expressions

### Quadratic Equation Solver
```python
from src.tools import solve_quadratic

# Solve x² + 5x + 6 = 0
result = solve_quadratic(a=1, b=5, c=6)
# Returns: "Solutions: x = -2.0, x = -3.0"

# Handle complex solutions
result = solve_quadratic(a=1, b=2, c=5)
# Returns: "Complex solutions: x = -1.0+2.0i, x = -1.0-2.0i"
```

### Matrix Operations
```python
from src.tools import matrix_operations

# Matrix multiplication
result = matrix_operations("multiply", "[[1,2],[3,4]]", "[[5,6],[7,8]]")
# Returns: "[[19, 22], [43, 50]]"

# Matrix determinant
result = matrix_operations("determinant", "[[1,2],[3,4]]")
# Returns: "-2"
```

**Supported Operations:**
- `multiply` - Matrix multiplication
- `determinant` - Calculate determinant
- `transpose` - Matrix transpose
- `add` - Matrix addition
- `inverse` - Matrix inverse

### Command Shortcuts
When commands are enabled (`agent.enable_commands()`):

```python
# Direct calculator access
result = agent.execute_command("/calc", expression="15 * 23 + 7")

# Solve equations quickly  
result = agent.execute_command("/solve", a=1, b=-5, c=6)
```

## 🔬 Science Tools (`get_science_tools()`)

Scientific computation and conversion tools.

### Unit Converter
```python
from src.tools import unit_converter

# Temperature conversion
result = unit_converter(100, "celsius", "fahrenheit")
# Returns: "100°C = 212.0°F"

# Distance conversion
result = unit_converter(1, "mile", "kilometer")  
# Returns: "1 mile = 1.609344 km"

# Weight conversion
result = unit_converter(2.5, "kilogram", "pound")
# Returns: "2.5 kg = 5.511556554621939 lbs"
```

**Supported Units:**
- **Temperature**: celsius, fahrenheit, kelvin
- **Length**: meter, kilometer, centimeter, mile, foot, inch
- **Weight**: kilogram, gram, pound, ounce
- **Volume**: liter, milliliter, gallon, quart, pint
- **Energy**: joule, calorie, kilocalorie, btu

### Chemistry Helper
```python
from src.tools import chemistry_helper

# Molecular weight calculation
result = chemistry_helper("molecular_weight", "H2O")
# Returns: "Molecular weight of H2O: 18.015 g/mol"

# Balancing equations
result = chemistry_helper("balance", "H2 + O2 -> H2O")
# Returns: "Balanced equation: 2H2 + O2 -> 2H2O"

# Periodic table info
result = chemistry_helper("element", "Carbon")
# Returns: "Carbon (C): Atomic number 6, Mass 12.011"
```

**Functions:**
- `molecular_weight` - Calculate molecular weight
- `balance` - Balance chemical equations
- `element` - Periodic table information
- `ph_calculator` - pH and pOH calculations

### Physics Calculator
```python
from src.tools import physics_calculator

# Kinetic energy
result = physics_calculator("kinetic_energy", mass=50, velocity=10)
# Returns: "Kinetic Energy = 0.5 * 50 * 10² = 2500.0 J"

# Force calculation
result = physics_calculator("force", mass=10, acceleration=9.8)
# Returns: "Force = 10 * 9.8 = 98.0 N"

# Ohm's law
result = physics_calculator("ohms_law", voltage=12, resistance=4)
# Returns: "Current = 12V / 4Ω = 3.0 A"
```

**Calculations:**
- `kinetic_energy` - KE = ½mv²
- `potential_energy` - PE = mgh  
- `force` - F = ma
- `ohms_law` - V = IR
- `power` - P = VI
- `momentum` - p = mv

### Command Shortcuts
```python
# Quick unit conversion
result = agent.execute_command("/convert", value=100, from_unit="F", to_unit="C")

# Fast chemistry lookup
result = agent.execute_command("/element", symbol="Au")
```

## 💻 Coding Tools (`get_coding_tools()`)

Programming and development assistance tools.

### Code Analyzer
```python
from src.tools import code_analyzer

# Python code analysis
code = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''

result = code_analyzer(code, "python")
# Returns: Analysis with complexity, suggestions, potential issues
```

**Analysis Features:**
- Syntax validation
- Complexity analysis
- Security vulnerability detection
- Performance suggestions
- Code style recommendations

### Regex Helper
```python
from src.tools import regex_helper

# Pattern testing
result = regex_helper("test", r"\d{3}-\d{2}-\d{4}", "123-45-6789")
# Returns: "Match found: 123-45-6789"

# Pattern explanation
result = regex_helper("explain", r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
# Returns: "Email validation pattern: matches valid email addresses..."

# Find all matches
result = regex_helper("findall", r"\d+", "There are 123 apples and 456 oranges")
# Returns: "Matches found: ['123', '456']"
```

**Functions:**
- `test` - Test pattern against string
- `explain` - Explain regex pattern  
- `findall` - Find all matches
- `substitute` - Replace matches
- `split` - Split string by pattern

### JSON Formatter
```python
from src.tools import json_formatter

# Format JSON
messy_json = '{"name":"John","age":30,"city":"New York"}'
result = json_formatter("format", messy_json)
# Returns: Pretty-formatted JSON with proper indentation

# Validate JSON
result = json_formatter("validate", '{"invalid": json}')
# Returns: "Invalid JSON: Expecting property name enclosed in double quotes"

# Minify JSON
result = json_formatter("minify", formatted_json)
# Returns: Compact JSON without whitespace
```

**Operations:**
- `format` - Pretty-print JSON with indentation
- `validate` - Check JSON syntax  
- `minify` - Remove whitespace
- `extract` - Extract specific fields
- `merge` - Combine JSON objects

### Command Shortcuts
```python
# Quick code check
result = agent.execute_command("/analyze", code="def test(): return 42")

# Fast regex test
result = agent.execute_command("/regex", pattern=r"\d+", text="abc123def")

# JSON formatting
result = agent.execute_command("/json", operation="format", data='{"a":1}')
```

## 🌍 Basic Tools (`get_basic_tools()`)

Essential utility tools for general-purpose agents.

### Weather Tool
```python
from src.tools import get_weather

# Current weather
result = get_weather("Paris")
# Returns: "The weather in Paris is Sunny with a temperature of 22°C"

# Weather with details
result = get_weather("New York", detailed=True)
# Returns: Detailed weather including humidity, wind, pressure
```

### Magic Calculator  
```python
from src.tools import magic_calculator

# Smart calculation with natural language
result = magic_calculator("What's 15% of 240?")
# Returns: "36.0"

result = magic_calculator("Square root of 144 plus 5")
# Returns: "17.0"
```

## 🔗 RAG Tools (Document Search)

Document retrieval and search capabilities.

### Setup RAG Tools
```python
from src.rag import setup_rag_tools

# From URLs
rag_tools = await setup_rag_tools(urls=["https://example.com/docs"])

# From documents
rag_tools = await setup_rag_tools(documents=["doc1.txt", "doc2.txt"])

# Add to agent
agent.add_tools(rag_tools)
```

### Document Search
```python
# Search documents
result = agent.chat("What does the contract say about payment terms?")
# Searches indexed documents and provides contextual answer
```

## 🛠️ Custom Tools

### Creating Custom Tools

```python
from langchain_core.tools import tool
from src.base import Agent

@tool
def my_custom_tool(input_text: str) -> str:
    """Custom tool that processes text."""
    return f"Processed: {input_text.upper()}"

# Add to agent
agent = Agent()
agent.add_tool(my_custom_tool)
```

### Tool Collections

```python
def get_my_tools():
    """Return collection of custom tools."""
    return [my_custom_tool, another_tool, yet_another_tool]

# Add collection
agent.add_tools(get_my_tools())
```

### Commands for Custom Tools

```python
from src.commands import command

@command("process", "Process text input", "/process <text>")
def process_command(text: str) -> str:
    """Command version of custom tool."""
    return f"Command processed: {text.upper()}"

# Enable and use
agent.enable_commands()
result = agent.execute_command("/process", text="hello world")
```

## 🎯 Tool Usage Patterns

### Adding Multiple Collections

```python
from src.tools import get_math_tools, get_science_tools, get_coding_tools

agent = Agent()
agent.add_tools(get_math_tools())
agent.add_tools(get_science_tools())  
agent.add_tools(get_coding_tools())

# Now agent has all capabilities
```

### Selective Tool Addition

```python
from src.tools import advanced_calculator, unit_converter, code_analyzer

agent = Agent()
agent.add_tool(advanced_calculator)
agent.add_tool(unit_converter)
agent.add_tool(code_analyzer)

# Agent has only specific tools
```

### Factory Functions with Tools

```python
from src.base import create_math_agent, create_science_agent

# Pre-configured with relevant tools
math_agent = create_math_agent()      # Has all math tools
science_agent = create_science_agent()  # Has all science tools

# Already ready to use
result = math_agent.chat("Calculate sin(30°)")
```

## 📋 Tool Management

### List Available Tools
```python
tools = agent.list_tools()
print(tools)
# ['advanced_calculator', 'solve_quadratic', 'unit_converter', ...]
```

### Remove Tools
```python
agent.remove_tool("advanced_calculator")
```

### Check Tool Availability
```python
if "unit_converter" in agent.list_tools():
    result = agent.chat("Convert 100°F to Celsius")
```

## ⚡ Performance Tips

1. **Use Commands for Speed**: Direct tool execution is faster than chat
2. **Selective Tools**: Only add tools you need to reduce context size
3. **Batch Operations**: Group related calculations in one request
4. **Cache Results**: Store frequently used calculations
5. **Specialized Agents**: Use factory functions for domain-specific tasks

## 🔍 Troubleshooting

### Common Issues

**Tool Not Found**
```python
# Check if tool is added
print(agent.list_tools())
agent.add_tools(get_math_tools())  # Add missing collection
```

**Command Not Working**  
```python
# Enable commands first
agent.enable_commands()
print(agent.list_commands())  # Check available commands
```

**Import Errors**
```python
# Ensure dependencies installed
pip install numpy scipy sympy
```

### Getting Help

Each tool includes detailed docstrings:
```python
help(advanced_calculator)
help(unit_converter)
```

Command help:
```python
result = agent.execute_command("/help")  # List all commands
result = agent.execute_command("/help", command="calc")  # Specific help
```

---

**Ready to use these tools? Check the [API Reference](api-reference.md) for complete method signatures and the [Examples](examples.md) for real-world usage patterns!**