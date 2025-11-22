# Adding Custom Tools

Learn how to create and integrate custom tools into your agents. Tools are the primary way agents interact with the world - from API calls to file operations to custom business logic.

## 🛠️ Tool Basics

### The @tool Decorator

All tools use LangChain's `@tool` decorator:

```python
from langchain_core.tools import tool

@tool
def my_tool(param1: str, param2: int) -> str:
    """
    Brief description of what this tool does.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
        
    Returns:
        Description of what the tool returns
    """
    # Your logic here
    return f"Result: {param1} processed {param2} times"
```

### Tool Design Principles

1. **Single Responsibility** - Each tool should do one thing well
2. **Clear Documentation** - The LLM reads your docstring to understand the tool
3. **Type Hints** - Help with parameter validation and IDE support
4. **Error Handling** - Return useful error messages, don't raise exceptions
5. **Deterministic** - Same inputs should produce same outputs when possible

## 📝 Basic Tool Examples

### API Integration Tool

```python
@tool
def get_weather_api(city: str, country_code: str = "US") -> str:
    """Get real weather data from API."""
    try:
        import requests
        
        # Example with OpenWeatherMap API
        api_key = "your_api_key_here"
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": f"{city},{country_code}",
            "appid": api_key,
            "units": "metric"
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return f"Weather in {city}: {temp}°C, {description}"
        else:
            return f"Could not get weather for {city}"
            
    except Exception as e:
        return f"Weather API error: {str(e)}"

# Add to agent
agent.add_tool(get_weather_api)
```

### File Operations Tool

```python
@tool
def read_file_content(file_path: str) -> str:
    """Read and return the contents of a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Truncate if too long
        if len(content) > 2000:
            content = content[:2000] + "... (truncated)"
            
        return f"File contents:\n{content}"
        
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

@tool  
def write_file_content(file_path: str, content: str) -> str:
    """Write content to a text file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return f"Successfully wrote {len(content)} characters to {file_path}"
        
    except Exception as e:
        return f"Error writing file: {str(e)}"

# Add to agent
agent.add_tools([read_file_content, write_file_content])
```

### Database Query Tool

```python
@tool
def query_database(sql_query: str) -> str:
    """Execute a safe SELECT query on the database."""
    try:
        import sqlite3
        
        # Safety check - only allow SELECT queries
        if not sql_query.strip().upper().startswith('SELECT'):
            return "Error: Only SELECT queries are allowed"
        
        # Connect to database
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        
        # Execute query
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        # Format results
        if results:
            # Get column names
            columns = [description[0] for description in cursor.description]
            
            # Format as table
            result_str = "Query Results:\n"
            result_str += " | ".join(columns) + "\n"
            result_str += "-" * (len(" | ".join(columns))) + "\n"
            
            for row in results[:10]:  # Limit to 10 rows
                result_str += " | ".join(str(cell) for cell in row) + "\n"
                
            if len(results) > 10:
                result_str += f"... and {len(results) - 10} more rows"
                
            return result_str
        else:
            return "Query executed successfully, no results returned"
            
    except Exception as e:
        return f"Database error: {str(e)}"
    finally:
        if 'conn' in locals():
            conn.close()

# Add to agent
agent.add_tool(query_database)
```

## 🔧 Advanced Tool Patterns

### Tool with Configuration

```python
class EmailTool:
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
    
    @tool
    def send_email(self, to: str, subject: str, body: str) -> str:
        """Send an email to the specified recipient."""
        try:
            import smtplib
            from email.mime.text import MIMEText
            
            # Create message
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = to
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
                
            return f"Email sent successfully to {to}"
            
        except Exception as e:
            return f"Failed to send email: {str(e)}"

# Configure and use
email_tool = EmailTool(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    username="your-email@gmail.com", 
    password="your-app-password"
)

agent.add_tool(email_tool.send_email)
```

### Stateful Tool

```python
class CalculatorTool:
    def __init__(self):
        self.memory = 0
        self.history = []
    
    @tool
    def calculate(self, expression: str) -> str:
        """Calculate mathematical expressions and remember the result."""
        try:
            # Evaluate safely
            result = eval(expression, {"__builtins__": {}}, {
                "sin": math.sin, "cos": math.cos, "sqrt": math.sqrt,
                "pi": math.pi, "e": math.e, "memory": self.memory
            })
            
            # Update memory and history
            self.memory = result
            self.history.append(f"{expression} = {result}")
            
            return f"Result: {result} (stored in memory)"
            
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    @tool
    def get_memory(self) -> str:
        """Get the current memory value."""
        return f"Memory: {self.memory}"
    
    @tool
    def get_history(self) -> str:
        """Get calculation history."""
        if not self.history:
            return "No calculation history"
        
        return "Calculation History:\n" + "\n".join(self.history[-5:])  # Last 5
    
    @tool
    def clear_memory(self) -> str:
        """Clear memory and history."""
        self.memory = 0
        self.history = []
        return "Memory and history cleared"

# Use stateful calculator
calc = CalculatorTool()
agent.add_tools([calc.calculate, calc.get_memory, calc.get_history, calc.clear_memory])
```

## 🏗️ Building Tool Collections

### Organize Related Tools

```python
# business_tools.py
from langchain_core.tools import tool

@tool
def get_customer_info(customer_id: str) -> str:
    """Get customer information by ID."""
    # Your business logic
    return f"Customer {customer_id}: John Doe, Premium Account"

@tool
def process_order(product_id: str, quantity: int, customer_id: str) -> str:
    """Process a customer order."""
    # Your order processing logic
    total = quantity * 29.99  # Mock price
    return f"Order processed: {quantity}x Product {product_id} for Customer {customer_id}. Total: ${total:.2f}"

@tool
def check_inventory(product_id: str) -> str:
    """Check current inventory levels."""
    # Your inventory logic
    return f"Product {product_id}: 150 units in stock"

def get_business_tools():
    """Get all business-related tools."""
    return [get_customer_info, process_order, check_inventory]

# Use the collection
from business_tools import get_business_tools
agent.add_tools(get_business_tools())
```

### Math Tools Example (Production-Ready)

Here's how the math agent tools are actually implemented:

```python
@tool
def advanced_calculator(expression: str) -> str:
    """
    Evaluate mathematical expressions safely.
    Supports basic arithmetic, trigonometry, logarithms, and constants.
    
    Examples:
    - "2 + 3 * 4"
    - "sin(pi/2)" 
    - "log(10)"
    - "sqrt(16)"
    """
    try:
        import math
        
        # Safe evaluation with math functions available
        allowed_names = {
            k: v for k, v in math.__dict__.items() 
            if not k.startswith("__")
        }
        allowed_names.update({
            "abs": abs, "round": round, "min": min, "max": max, "sum": sum,
        })
        
        # Replace common mathematical notation
        expression = expression.replace("^", "**")  # Power operator
        
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"{expression} = {result}"
        
    except Exception as e:
        return f"Error evaluating '{expression}': {str(e)}"

@tool
def solve_quadratic(a: float, b: float, c: float) -> str:
    """
    Solve quadratic equation ax² + bx + c = 0.
    Returns the roots of the equation.
    """
    try:
        import math
        
        discriminant = b**2 - 4*a*c
        
        if discriminant > 0:
            root1 = (-b + math.sqrt(discriminant)) / (2*a)
            root2 = (-b - math.sqrt(discriminant)) / (2*a)
            return f"Two real roots: x₁ = {root1}, x₂ = {root2}"
        elif discriminant == 0:
            root = -b / (2*a)
            return f"One real root: x = {root}"
        else:
            real_part = -b / (2*a)
            imag_part = math.sqrt(-discriminant) / (2*a)
            return f"Two complex roots: x₁ = {real_part} + {imag_part}i, x₂ = {real_part} - {imag_part}i"
            
    except Exception as e:
        return f"Error solving quadratic equation: {str(e)}"

def get_math_tools():
    """Get mathematics-focused tools."""
    return [advanced_calculator, solve_quadratic]
```

## 🔐 Security Considerations

### Input Validation

```python
@tool
def safe_file_reader(file_path: str) -> str:
    """Safely read files with path validation."""
    import os
    
    # Validate file path
    if ".." in file_path:
        return "Error: Path traversal not allowed"
    
    # Only allow certain directories
    allowed_dirs = ["/safe/directory", "./documents"]
    if not any(file_path.startswith(dir) for dir in allowed_dirs):
        return "Error: File not in allowed directory"
    
    # Check file exists and is readable
    if not os.path.exists(file_path):
        return f"Error: File does not exist: {file_path}"
        
    if not os.path.isfile(file_path):
        return f"Error: Not a file: {file_path}"
    
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"
```

### Rate Limiting

```python
import time
from functools import wraps

def rate_limit(calls_per_minute: int):
    """Decorator to rate limit tool calls."""
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                return f"Rate limited. Wait {min_interval - elapsed:.1f} seconds."
            
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@tool
@rate_limit(calls_per_minute=10)  # Max 10 calls per minute
def expensive_api_call(query: str) -> str:
    """Make an expensive API call with rate limiting."""
    # Your expensive API logic
    return f"API result for: {query}"
```

## 🧪 Testing Tools

### Unit Testing Tools

```python
def test_calculator_tool():
    """Test the calculator tool functionality."""
    
    # Test basic arithmetic
    result = advanced_calculator("2 + 3")
    assert "5" in result
    
    # Test trigonometry
    result = advanced_calculator("sin(0)")
    assert "0" in result
    
    # Test error handling
    result = advanced_calculator("invalid expression")
    assert "Error" in result
    
    print("✅ Calculator tool tests passed")

def test_quadratic_solver():
    """Test quadratic equation solver."""
    
    # Test two real roots
    result = solve_quadratic(1, 5, 6)
    assert "x₁ = -2" in result and "x₂ = -3" in result
    
    # Test one root
    result = solve_quadratic(1, -4, 4)
    assert "x = 2" in result
    
    # Test complex roots
    result = solve_quadratic(1, 0, 1)
    assert "complex" in result
    
    print("✅ Quadratic solver tests passed")

# Run tests
test_calculator_tool()
test_quadratic_solver()
```

### Integration Testing

```python
def test_math_agent_integration():
    """Test math agent with real scenarios."""
    from src.base import create_math_agent
    
    agent = create_math_agent()
    
    # Test calculator integration
    response = agent.chat("What is 15 * 23 + 7?")
    assert "352" in response
    
    # Test quadratic solver integration  
    response = agent.chat("Solve the equation x² - 5x + 6 = 0")
    assert "x₁ = 3" in response and "x₂ = 2" in response
    
    print("✅ Math agent integration tests passed")

test_math_agent_integration()
```

## 🎯 Best Practices

### 1. Clear Tool Descriptions

```python
# ❌ Bad: Vague description
@tool
def process_data(data: str) -> str:
    """Process some data."""
    pass

# ✅ Good: Clear, specific description
@tool
def calculate_compound_interest(principal: float, rate: float, years: int, compounds_per_year: int = 12) -> str:
    """
    Calculate compound interest for an investment.
    
    Args:
        principal: Initial investment amount in dollars
        rate: Annual interest rate as decimal (e.g., 0.05 for 5%)
        years: Number of years to invest
        compounds_per_year: How many times per year interest compounds (default: 12)
        
    Returns:
        Formatted string with final amount and total interest earned
        
    Example:
        calculate_compound_interest(1000, 0.05, 10) -> Final: $1643.62, Interest: $643.62
    """
    pass
```

### 2. Error Handling

```python
@tool
def robust_tool(input_data: str) -> str:
    """A well-designed tool with proper error handling."""
    try:
        # Validate inputs
        if not input_data or not input_data.strip():
            return "Error: Input data cannot be empty"
        
        # Process data
        result = process_input(input_data)
        
        # Validate output
        if result is None:
            return "Error: Processing failed to produce result"
        
        return f"Success: {result}"
        
    except ValueError as e:
        return f"Input error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
```

### 3. Performance Optimization

```python
from functools import lru_cache

@tool
def cached_expensive_operation(input_value: str) -> str:
    """Expensive operation with caching."""
    
    @lru_cache(maxsize=100)
    def _expensive_calculation(value: str) -> str:
        # Simulate expensive operation
        import time
        time.sleep(1)  # Simulate delay
        return f"Processed: {value.upper()}"
    
    try:
        return _expensive_calculation(input_value)
    except Exception as e:
        return f"Error: {str(e)}"
```

## 🚀 Next Steps

1. **[Upgrading Agents](upgrading-agents.md)** - Learn to evolve agents over time
2. **[Advanced Usage](advanced-usage.md)** - Multi-agent systems, RAG, HITL  
3. **[Tool Collections](tool-collections.md)** - Browse all available tools
4. **[Examples](examples.md)** - See real-world tool implementations

Start with simple tools and gradually add complexity. The math agent tools are a great reference for production-ready implementations!