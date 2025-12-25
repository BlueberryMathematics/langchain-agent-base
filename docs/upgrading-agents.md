# Upgrading Agents Over Time

Learn how to evolve and upgrade your agents as your needs grow, using the math agent as a primary example. This guide shows practical strategies for agent evolution in production environments.

## 🎯 Math Agent Evolution Journey

### Stage 1: Basic Calculator Agent

Start simple with basic arithmetic:

```python
from src.base import Agent
from src.tools import advanced_calculator

# Version 1.0: Basic calculator
basic_math_agent = Agent(
    system_prompt="You are a calculator assistant. Help with basic arithmetic.",
)
basic_math_agent.add_tool(advanced_calculator)

# Test basic functionality
response = basic_math_agent.chat("What is 15 * 23?")
print(response)  # "15 * 23 = 345"
```

### Stage 2: Add Equation Solving

Add more mathematical capabilities:

```python
from src.tools import solve_quadratic

# Version 2.0: Add equation solving
basic_math_agent.add_tool(solve_quadratic)

# Update system prompt to reflect new capabilities
basic_math_agent.system_prompt = """
You are a mathematical assistant. You can:
- Perform calculations with advanced_calculator
- Solve quadratic equations with solve_quadratic
Always show your work step by step.
"""
basic_math_agent._rebuild_agent()  # Rebuild with new prompt

# Test new functionality
response = basic_math_agent.chat("Solve x² + 5x + 6 = 0")
print(response)  # "Two real roots: x₁ = -2, x₂ = -3"
```

### Stage 3: Advanced Mathematics

Add matrix operations and more complex math:

```python
from src.tools import matrix_operations

# Version 3.0: Advanced mathematics
basic_math_agent.add_tool(matrix_operations)

# Update system prompt again
basic_math_agent.system_prompt = """
You are an advanced mathematics assistant. You can:
- Perform complex calculations (trigonometry, logarithms, etc.)
- Solve quadratic equations  
- Perform matrix operations (multiply, transpose, determinant, inverse)
- Handle scientific notation and complex numbers

Always explain your reasoning and show step-by-step solutions.
"""
basic_math_agent._rebuild_agent()

# Test matrix capabilities
response = basic_math_agent.chat("Multiply [[1,2],[3,4]] by [[5,6],[7,8]]")
print(response)  # Matrix multiplication result
```

### Stage 4: Add Commands for Speed

Enable direct command execution for faster operations:

```python
from src.commands import create_math_commands

# Version 4.0: Add command system
basic_math_agent.enable_commands()
basic_math_agent.add_commands(create_math_commands())

# Now supports direct commands
result = basic_math_agent.execute_command("/calc", expression="sin(pi/2)")
print(result)  # Direct calculation without chat overhead

# List available commands
print("Available commands:", basic_math_agent.list_commands())
```

### Stage 5: Production Math Agent

Use the factory function for a fully-featured math agent:

```python
from src.base import create_math_agent

# Version 5.0: Production-ready math agent
math_agent = create_math_agent(enable_commands=True)

# This includes:
# - All math tools (calculator, quadratic, matrix)
# - Math commands (/calc, /solve)  
# - Agent commands (/help, /tools, /status)
# - Optimized system prompt
# - Error handling and validation

print("Tools:", math_agent.list_tools())
print("Commands:", math_agent.list_commands())
```

## 🔄 Upgrade Strategies

### 1. Incremental Tool Addition

Add tools one at a time and test thoroughly:

```python
class EvolvingMathAgent:
    def __init__(self):
        self.agent = Agent(system_prompt="Basic math assistant")
        self.version = "1.0"
        self.capabilities = []
    
    def add_capability(self, tool, capability_name: str, new_version: str):
        """Add a new capability and update version."""
        print(f"Upgrading from {self.version} to {new_version}")
        print(f"Adding capability: {capability_name}")
        
        # Add tool
        self.agent.add_tool(tool)
        self.capabilities.append(capability_name)
        
        # Update version
        self.version = new_version
        
        # Update system prompt
        self._update_system_prompt()
        
        print(f"✅ Upgrade complete. Current capabilities: {self.capabilities}")
    
    def _update_system_prompt(self):
        """Update system prompt based on current capabilities."""
        prompt = "You are a mathematical assistant with the following capabilities:\n"
        for cap in self.capabilities:
            prompt += f"- {cap}\n"
        prompt += "\nAlways show your work and explain your reasoning."
        
        self.agent.system_prompt = prompt
        self.agent._rebuild_agent()
    
    def chat(self, message: str) -> str:
        return self.agent.chat(message)

# Use evolving agent
math_agent = EvolvingMathAgent()

# Upgrade path
math_agent.add_capability(advanced_calculator, "Basic calculations", "1.1")
math_agent.add_capability(solve_quadratic, "Quadratic equation solving", "1.2") 
math_agent.add_capability(matrix_operations, "Matrix operations", "2.0")
```

### 2. Feature Flags for Safe Rollouts

Test new features before full deployment:

```python
class FeatureFlagAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.features = {
            "advanced_math": False,
            "matrix_ops": False,
            "statistics": False,
            "graphing": False
        }
    
    def enable_feature(self, feature_name: str):
        """Enable a feature and add corresponding tools."""
        if feature_name not in self.features:
            print(f"Unknown feature: {feature_name}")
            return
        
        self.features[feature_name] = True
        
        if feature_name == "advanced_math":
            from src.tools import advanced_calculator
            self.add_tool(advanced_calculator)
            print("✅ Advanced math enabled")
        
        elif feature_name == "matrix_ops":
            from src.tools import matrix_operations
            self.add_tool(matrix_operations) 
            print("✅ Matrix operations enabled")
        
        elif feature_name == "statistics":
            self.add_tool(self._create_stats_tool())
            print("✅ Statistics enabled")
    
    def _create_stats_tool(self):
        from langchain_core.tools import tool
        
        @tool
        def calculate_statistics(data: str) -> str:
            """Calculate basic statistics for dataset."""
            try:
                numbers = [float(x.strip()) for x in data.split(',')]
                mean = sum(numbers) / len(numbers)
                variance = sum((x - mean)**2 for x in numbers) / len(numbers)
                return f"Mean: {mean:.2f}, Variance: {variance:.2f}"
            except Exception as e:
                return f"Statistics error: {e}"
        
        return calculate_statistics

# Use with feature flags
agent = FeatureFlagAgent()

# Test features individually
agent.enable_feature("advanced_math")
# Test advanced math...

agent.enable_feature("matrix_ops") 
# Test matrix operations...

agent.enable_feature("statistics")
# Test statistics...
```

### 3. A/B Testing Agent Versions

Compare different agent configurations:

```python
class AgentVersionManager:
    def __init__(self):
        self.versions = {}
        self.current_version = None
    
    def register_version(self, version_name: str, agent_factory):
        """Register a new agent version."""
        self.versions[version_name] = agent_factory
        print(f"Registered version: {version_name}")
    
    def switch_version(self, version_name: str):
        """Switch to a different agent version."""
        if version_name not in self.versions:
            print(f"Version {version_name} not found")
            return None
        
        self.current_version = version_name
        agent = self.versions[version_name]()
        print(f"Switched to version: {version_name}")
        return agent
    
    def compare_versions(self, test_query: str, versions: list = None):
        """Compare responses across versions."""
        if not versions:
            versions = list(self.versions.keys())
        
        results = {}
        for version in versions:
            agent = self.versions[version]()
            response = agent.chat(test_query)
            results[version] = response
        
        return results

# Setup version manager
manager = AgentVersionManager()

# Register different versions
manager.register_version("basic", lambda: Agent())
manager.register_version("math_v1", lambda: create_math_agent())
manager.register_version("math_v2", lambda: create_math_agent(enable_commands=True))

# Compare versions
results = manager.compare_versions("Solve x² + 5x + 6 = 0")
for version, response in results.items():
    print(f"{version}: {response}")
```

### 4. Data-Driven Upgrades

Track usage patterns to guide upgrades:

```python
import json
from datetime import datetime
from collections import Counter

class SmartMathAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.usage_log = []
        self.tool_stats = Counter()
        self.error_log = []
    
    def chat(self, message: str, **kwargs) -> str:
        """Chat with usage tracking."""
        start_time = datetime.now()
        
        try:
            # Get response
            response = super().chat(message, **kwargs)
            
            # Log successful usage
            self.usage_log.append({
                "timestamp": start_time.isoformat(),
                "message": message,
                "response_length": len(response),
                "success": True
            })
            
            # Track tool usage (simplified)
            for tool in self.tools:
                if tool.name.lower() in message.lower():
                    self.tool_stats[tool.name] += 1
            
            return response
            
        except Exception as e:
            # Log errors
            self.error_log.append({
                "timestamp": start_time.isoformat(), 
                "message": message,
                "error": str(e)
            })
            return f"Error: {str(e)}"
    
    def get_usage_insights(self):
        """Analyze usage patterns for upgrade decisions."""
        total_requests = len(self.usage_log)
        error_rate = len(self.error_log) / max(1, total_requests)
        
        insights = {
            "total_requests": total_requests,
            "error_rate": error_rate,
            "most_used_tools": self.tool_stats.most_common(5),
            "common_errors": Counter([e["error"] for e in self.error_log]).most_common(3)
        }
        
        # Suggest upgrades
        suggestions = []
        if self.tool_stats["advanced_calculator"] > 10:
            suggestions.append("Consider adding scientific functions")
        if error_rate > 0.1:
            suggestions.append("Review error handling and input validation")
        
        insights["upgrade_suggestions"] = suggestions
        return insights

# Use smart agent
smart_agent = SmartMathAgent()

# After some usage...
insights = smart_agent.get_usage_insights()
print("Usage insights:", json.dumps(insights, indent=2))
```

## 🚀 Upgrade Patterns

### Pattern 1: Modular Expansion

Build agents by adding focused modules:

```python
# Base math agent
agent = Agent()

# Math module
from src.tools import get_math_tools
agent.add_tools(get_math_tools())

# Statistics module  
def add_statistics_module(agent):
    @tool
    def descriptive_stats(data: str) -> str:
        """Calculate descriptive statistics."""
        # Implementation here
        pass
    
    @tool
    def hypothesis_test(sample1: str, sample2: str) -> str:
        """Perform statistical hypothesis test."""
        # Implementation here
        pass
    
    agent.add_tools([descriptive_stats, hypothesis_test])
    return agent

# Graphing module
def add_graphing_module(agent):
    @tool
    def create_plot(data: str, plot_type: str) -> str:
        """Create data visualization."""
        # Implementation here
        pass
    
    agent.add_tool(create_plot)
    return agent

# Upgrade incrementally
agent = add_statistics_module(agent)
agent = add_graphing_module(agent)
```

### Pattern 2: Capability Inheritance

Create specialized agent hierarchies:

```python
class BasicMathAgent(Agent):
    def __init__(self):
        super().__init__(system_prompt="Basic math assistant")
        from src.tools import advanced_calculator
        self.add_tool(advanced_calculator)

class AlgebraMathAgent(BasicMathAgent):
    def __init__(self):
        super().__init__()
        from src.tools import solve_quadratic
        self.add_tool(solve_quadratic)
        self.system_prompt = "Algebra specialist with equation solving"
        self._rebuild_agent()

class AdvancedMathAgent(AlgebraMathAgent):
    def __init__(self):
        super().__init__()
        from src.tools import matrix_operations
        self.add_tool(matrix_operations)
        self.system_prompt = "Advanced mathematics with matrices and equations"
        self._rebuild_agent()

# Use appropriate level
basic = BasicMathAgent()
algebra = AlgebraMathAgent() 
advanced = AdvancedMathAgent()
```

### Pattern 3: Plugin Architecture

Allow dynamic loading of capabilities:

```python
class PluginMathAgent(Agent):
    def __init__(self):
        super().__init__()
        self.plugins = {}
    
    def load_plugin(self, plugin_name: str, plugin_module):
        """Load a plugin module."""
        try:
            # Get tools from plugin
            tools = plugin_module.get_tools()
            commands = getattr(plugin_module, 'get_commands', lambda: [])()
            
            # Add to agent
            self.add_tools(tools)
            if commands:
                self.add_commands(commands)
            
            self.plugins[plugin_name] = plugin_module
            print(f"✅ Loaded plugin: {plugin_name}")
            
        except Exception as e:
            print(f"❌ Failed to load plugin {plugin_name}: {e}")
    
    def unload_plugin(self, plugin_name: str):
        """Remove a plugin."""
        if plugin_name in self.plugins:
            # This is simplified - in practice you'd need to track which tools belong to which plugin
            del self.plugins[plugin_name]
            print(f"Unloaded plugin: {plugin_name}")

# Plugin modules would look like:
# statistics_plugin.py
def get_tools():
    return [stats_tool1, stats_tool2]

def get_commands():
    return [stats_command1, stats_command2]
```

## 📊 Monitoring Agent Evolution

### Performance Metrics

```python
import time
from functools import wraps

def performance_monitor(func):
    """Decorator to monitor agent performance."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(self, *args, **kwargs)
            execution_time = time.time() - start_time
            
            # Log performance
            self._log_performance({
                "method": func.__name__,
                "execution_time": execution_time,
                "success": True,
                "timestamp": time.time()
            })
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self._log_performance({
                "method": func.__name__, 
                "execution_time": execution_time,
                "success": False,
                "error": str(e),
                "timestamp": time.time()
            })
            raise
    
    return wrapper

class MonitoredMathAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.performance_log = []
    
    @performance_monitor
    def chat(self, message: str, **kwargs):
        return super().chat(message, **kwargs)
    
    def _log_performance(self, metrics):
        self.performance_log.append(metrics)
    
    def get_performance_report(self):
        """Generate performance report."""
        if not self.performance_log:
            return "No performance data available"
        
        successful = [p for p in self.performance_log if p["success"]]
        avg_time = sum(p["execution_time"] for p in successful) / len(successful)
        error_rate = 1 - (len(successful) / len(self.performance_log))
        
        return f"""Performance Report:
- Average response time: {avg_time:.2f}s
- Success rate: {(1-error_rate)*100:.1f}%
- Total requests: {len(self.performance_log)}
"""
```

## 🔮 Planning Future Upgrades

### Roadmap Template

```python
# agent_roadmap.py
MATH_AGENT_ROADMAP = {
    "v1.0": {
        "features": ["Basic arithmetic", "Simple calculations"],
        "tools": ["advanced_calculator"],
        "status": "✅ Complete"
    },
    "v1.5": {
        "features": ["Equation solving", "Quadratic equations"],
        "tools": ["solve_quadratic"],
        "status": "✅ Complete"
    },
    "v2.0": {
        "features": ["Matrix operations", "Linear algebra"],
        "tools": ["matrix_operations"],
        "status": "✅ Complete"
    },
    "v2.5": {
        "features": ["Statistics", "Data analysis"],
        "tools": ["statistics_calculator", "hypothesis_testing"],
        "status": "🚧 In Development"
    },
    "v3.0": {
        "features": ["Calculus", "Derivatives and integrals"],
        "tools": ["derivative_calculator", "integral_solver"],
        "status": "📋 Planned"
    },
    "v3.5": {
        "features": ["Graphing", "Data visualization"],
        "tools": ["plot_generator", "graph_analyzer"],
        "status": "💭 Concept"
    }
}

def print_roadmap():
    """Display the development roadmap."""
    print("Math Agent Development Roadmap")
    print("=" * 40)
    
    for version, details in MATH_AGENT_ROADMAP.items():
        print(f"\n{version} - {details['status']}")
        print(f"Features: {', '.join(details['features'])}")
        print(f"Tools: {', '.join(details['tools'])}")
```

## 🎯 Best Practices

1. **Start Simple**: Begin with core functionality, add complexity gradually
2. **Version Everything**: Track changes and maintain backward compatibility
3. **Test Thoroughly**: Validate each upgrade before deployment
4. **Monitor Usage**: Use data to guide upgrade decisions
5. **Document Changes**: Keep clear records of what changed and why
6. **Plan Ahead**: Maintain a roadmap of future enhancements

## 🚀 Next Steps

1. **[Advanced Usage](advanced-usage.md)** - Multi-agent systems, RAG, HITL
2. **[Examples](examples.md)** - See real-world upgrade scenarios  
3. **[API Reference](api-reference.md)** - Complete technical documentation

The math agent provides an excellent template for systematic agent evolution. Start with basic functionality and expand based on user needs and usage patterns!