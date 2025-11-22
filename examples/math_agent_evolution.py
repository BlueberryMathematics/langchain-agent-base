"""
Example: Ultimate Math Agent Implementation
==========================================

This example shows how to create a specialized math agent using the
LangChain Agent Base Protocol system with automatic versioning,
API generation, and metadata management.

This serves as the template for users building their own specialized agents.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from src.base import Agent
from src.protocol import register_agent, AgentStatus
from src.discovery import AutoRegisterMixin
from src.tools import get_math_tools, advanced_calculator, solve_quadratic, matrix_operations
from src.commands import create_math_commands
from langchain_core.tools import tool


# Custom math tools for the ultimate math agent
@tool
def symbolic_math(expression: str) -> str:
    """
    Perform symbolic mathematics including calculus, algebra, and more.
    
    Examples:
    - "diff(x^2 + 3*x + 2, x)" (derivative)
    - "integrate(2*x + 1, x)" (integral) 
    - "solve(x^2 + 3*x + 2 = 0, x)" (equation solving)
    - "factor(x^2 + 5*x + 6)" (factoring)
    """
    try:
        # This is a mock implementation - in reality you'd use SymPy
        expression = expression.lower()
        
        if 'diff(' in expression:
            return f"Derivative: d/dx[{expression.split('diff(')[1].split(',')[0]}] = computed derivative"
        elif 'integrate(' in expression:
            return f"Integral: ∫{expression.split('integrate(')[1].split(',')[0]} dx = computed integral"
        elif 'solve(' in expression:
            return f"Solution: {expression.split('solve(')[1].split(',')[0]} → computed solutions"
        elif 'factor(' in expression:
            return f"Factored form: {expression.split('factor(')[1].split(')')[0]} = computed factorization"
        else:
            # Fallback to advanced calculator
            return advanced_calculator.invoke({"expression": expression})
            
    except Exception as e:
        return f"Symbolic math error: {str(e)}"


@tool
def statistical_analysis(data: str, operation: str = "describe") -> str:
    """
    Perform statistical analysis on numerical data.
    
    Operations:
    - describe: Basic descriptive statistics
    - correlation: Correlation analysis (for paired data)
    - regression: Linear regression analysis
    - hypothesis_test: Basic hypothesis testing
    
    Data format: "1,2,3,4,5" or "1:10,2:15,3:20" (paired)
    """
    try:
        # Parse data
        if ':' in data:
            # Paired data
            pairs = [pair.split(':') for pair in data.split(',')]
            x_values = [float(pair[0]) for pair in pairs]
            y_values = [float(pair[1]) for pair in pairs]
        else:
            # Single dataset
            values = [float(x.strip()) for x in data.split(',')]
            
        if operation == "describe":
            if ':' in data:
                # Describe both x and y
                x_mean = sum(x_values) / len(x_values)
                y_mean = sum(y_values) / len(y_values)
                return f"X: mean={x_mean:.2f}, Y: mean={y_mean:.2f}"
            else:
                mean = sum(values) / len(values)
                variance = sum((x - mean)**2 for x in values) / len(values)
                std_dev = variance ** 0.5
                return f"Statistics: mean={mean:.2f}, std={std_dev:.2f}, var={variance:.2f}"
                
        elif operation == "correlation" and ':' in data:
            # Simple correlation coefficient calculation
            n = len(x_values)
            sum_x = sum(x_values)
            sum_y = sum(y_values)
            sum_xy = sum(x*y for x, y in zip(x_values, y_values))
            sum_x2 = sum(x**2 for x in x_values)
            sum_y2 = sum(y**2 for y in y_values)
            
            r = (n*sum_xy - sum_x*sum_y) / ((n*sum_x2 - sum_x**2) * (n*sum_y2 - sum_y**2))**0.5
            return f"Correlation coefficient: r = {r:.3f}"
            
        else:
            return f"Operation '{operation}' not implemented or requires different data format"
            
    except Exception as e:
        return f"Statistical analysis error: {str(e)}"


@tool
def number_theory(number: int, operation: str = "factors") -> str:
    """
    Number theory operations.
    
    Operations:
    - factors: Find all factors
    - prime_check: Check if number is prime
    - prime_factorization: Prime factorization
    - gcd: Greatest common divisor (provide two numbers: "12,18")
    - lcm: Least common multiple (provide two numbers: "12,18")
    """
    try:
        if operation == "factors":
            factors = [i for i in range(1, number + 1) if number % i == 0]
            return f"Factors of {number}: {factors}"
            
        elif operation == "prime_check":
            if number < 2:
                return f"{number} is not prime"
            for i in range(2, int(number**0.5) + 1):
                if number % i == 0:
                    return f"{number} is not prime (divisible by {i})"
            return f"{number} is prime"
            
        elif operation == "prime_factorization":
            factors = []
            d = 2
            while d * d <= number:
                while number % d == 0:
                    factors.append(d)
                    number //= d
                d += 1
            if number > 1:
                factors.append(number)
            return f"Prime factorization: {' × '.join(map(str, factors))}"
            
        else:
            return f"Operation '{operation}' not implemented"
            
    except Exception as e:
        return f"Number theory error: {str(e)}"


# Math Agent v1.0 - Basic Implementation
@register_agent(
    name="math",
    version="1.0.0",
    domain="math",
    category="specialist",
    description="Basic mathematical assistant with core calculation capabilities",
    author="LangChain Agent Base",
    status=AgentStatus.PRODUCTION
)
class MathAgent(Agent, AutoRegisterMixin):
    """
    Basic math agent with essential mathematical tools.
    Serves as the foundation for more advanced versions.
    """
    
    def __init__(self, **kwargs):
        # Core math tools only
        tools = [advanced_calculator, solve_quadratic]
        
        super().__init__(
            system_prompt="""You are a mathematical assistant specializing in calculations and basic equation solving.
            
Your capabilities:
- Advanced mathematical calculations (trigonometry, logarithms, etc.)
- Quadratic equation solving
- Step-by-step explanations

Always show your work and explain your reasoning clearly.""",
            tools=tools,
            enable_commands=True,
            **kwargs
        )
        
        # Add math commands
        self.add_commands(create_math_commands())


# Math Agent v2.0 - Enhanced with Linear Algebra
@register_agent(
    name="math",
    version="2.0.0", 
    domain="math",
    category="specialist",
    description="Enhanced mathematical assistant with linear algebra capabilities",
    author="LangChain Agent Base",
    status=AgentStatus.PRODUCTION
)
class EnhancedMathAgent(Agent, AutoRegisterMixin):
    """
    Enhanced math agent with linear algebra and matrix operations.
    Builds upon v1.0 with additional matrix capabilities.
    """
    
    def __init__(self, **kwargs):
        # All core math tools + matrix operations
        tools = get_math_tools()  # Includes calculator, quadratic, matrix_operations
        
        super().__init__(
            system_prompt="""You are an advanced mathematical assistant specializing in algebra and linear algebra.
            
Your capabilities:
- Advanced mathematical calculations (trigonometry, logarithms, etc.)  
- Quadratic and polynomial equation solving
- Matrix operations (multiplication, transpose, determinant, inverse)
- Linear algebra problem solving
- Step-by-step explanations with mathematical notation

Always show your work, use proper mathematical notation, and explain concepts clearly.""",
            tools=tools,
            enable_commands=True,
            **kwargs
        )
        
        # Add math commands
        self.add_commands(create_math_commands())


# Math Agent v3.0 - Ultimate Math Agent
@register_agent(
    name="math", 
    version="3.0.0",
    domain="math", 
    category="specialist",
    description="Ultimate mathematical assistant with symbolic math, statistics, and number theory",
    author="LangChain Agent Base",
    status=AgentStatus.TESTING
)
class UltimateMathAgent(Agent, AutoRegisterMixin):
    """
    Ultimate math agent with comprehensive mathematical capabilities.
    The most advanced version with symbolic math, statistics, and number theory.
    """
    
    def __init__(self, **kwargs):
        # All math tools + advanced capabilities
        tools = get_math_tools() + [
            symbolic_math,
            statistical_analysis,
            number_theory
        ]
        
        super().__init__(
            system_prompt="""You are the ultimate mathematical assistant with comprehensive capabilities across all areas of mathematics.
            
Your extensive capabilities include:

🔢 ARITHMETIC & ALGEBRA:
- Advanced calculations (trigonometry, logarithms, exponentials)
- Polynomial and quadratic equation solving
- Symbolic mathematics (derivatives, integrals, factoring)

📐 LINEAR ALGEBRA:  
- Matrix operations (multiplication, transpose, determinant, inverse)
- Vector operations and transformations
- System of equations solving

📊 STATISTICS:
- Descriptive statistics (mean, median, mode, standard deviation)
- Correlation and regression analysis  
- Hypothesis testing and probability

🔍 NUMBER THEORY:
- Prime number analysis and factorization
- Greatest common divisor (GCD) and least common multiple (LCM)
- Modular arithmetic and number properties

💡 PROBLEM SOLVING:
- Step-by-step explanations with proper mathematical notation
- Multiple solution approaches when applicable
- Educational insights and concept explanations
- Real-world application examples

Always provide clear, detailed explanations and show your mathematical reasoning.""",
            tools=tools,
            enable_commands=True,
            **kwargs
        )
        
        # Add math commands
        self.add_commands(create_math_commands())
        
        # Add custom commands for advanced features
        self.add_command(self._create_symbolic_command())
        self.add_command(self._create_stats_command())
    
    def _create_symbolic_command(self):
        """Create symbolic math command."""
        from src.commands import command
        
        @command("symbolic", "Symbolic mathematics", "/symbolic <expression>")
        def symbolic_command(expression: str) -> str:
            return symbolic_math.invoke({"expression": expression})
        
        return symbolic_command
    
    def _create_stats_command(self):
        """Create statistics command."""
        from src.commands import command
        
        @command("stats", "Statistical analysis", "/stats <data> [operation]")
        def stats_command(data: str, operation: str = "describe") -> str:
            return statistical_analysis.invoke({"data": data, "operation": operation})
        
        return stats_command


# Development/Testing Agent - Experimental Features
@register_agent(
    name="math",
    version="4.0.0-beta", 
    domain="math",
    category="specialist", 
    description="Experimental math agent with AI-powered theorem proving (BETA)",
    author="LangChain Agent Base",
    status=AgentStatus.DEVELOPMENT
)
class ExperimentalMathAgent(UltimateMathAgent):
    """
    Experimental math agent with cutting-edge features.
    Inherits all capabilities from Ultimate Math Agent plus experimental features.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Add experimental tools
        self.add_tool(self._create_theorem_prover())
        
        # Update system prompt for experimental features
        self.system_prompt += """

🧪 EXPERIMENTAL FEATURES:
- AI-powered theorem proving and verification
- Advanced symbolic manipulation
- Research-level mathematical analysis

Note: Experimental features are under development and may produce unexpected results.
Always verify important mathematical conclusions independently."""
        
        self._rebuild_agent()
    
    def _create_theorem_prover(self):
        """Create experimental theorem proving tool."""
        
        @tool
        def theorem_prover(statement: str, context: str = "") -> str:
            """
            Experimental AI-powered theorem proving and verification.
            
            Args:
                statement: Mathematical statement to prove or verify
                context: Additional context or assumptions
            """
            return f"""Theorem Analysis: {statement}

Context: {context or 'General mathematical context'}

AI Analysis: This is an experimental feature. The statement requires formal mathematical proof techniques that are beyond current automated capabilities.

Suggested approach:
1. Define all terms and assumptions clearly
2. Identify the proof strategy (direct, contradiction, induction, etc.)
3. Break down into logical steps
4. Verify each step rigorously

Recommendation: Consult mathematical literature or formal proof systems for rigorous verification."""
        
        return theorem_prover


# Factory functions for easy agent creation
def create_basic_math_agent(**kwargs) -> MathAgent:
    """Create basic math agent (v1.0)."""
    return MathAgent(**kwargs)


def create_enhanced_math_agent(**kwargs) -> EnhancedMathAgent:
    """Create enhanced math agent with linear algebra (v2.0)."""
    return EnhancedMathAgent(**kwargs)


def create_ultimate_math_agent(**kwargs) -> UltimateMathAgent:
    """Create ultimate math agent with all features (v3.0).""" 
    return UltimateMathAgent(**kwargs)


def create_experimental_math_agent(**kwargs) -> ExperimentalMathAgent:
    """Create experimental math agent (v4.0-beta)."""
    return ExperimentalMathAgent(**kwargs)


# Demonstration function
def demonstrate_math_agent_evolution():
    """Demonstrate the evolution of math agents from basic to ultimate."""
    
    print("🧮 Math Agent Evolution Demonstration")
    print("=" * 50)
    
    test_queries = [
        "What is sin(π/2) + log(10)?",
        "Solve x² + 5x + 6 = 0",
        "Multiply matrices [[1,2],[3,4]] and [[5,6],[7,8]]",
        "Find the correlation between data points 1:2,2:4,3:6,4:8",
        "Is 97 a prime number?"
    ]
    
    # Test each version
    agents = [
        ("Basic Math Agent v1.0", MathAgent),
        ("Enhanced Math Agent v2.0", EnhancedMathAgent), 
        ("Ultimate Math Agent v3.0", UltimateMathAgent)
    ]
    
    for agent_name, agent_class in agents:
        print(f"\n🤖 Testing {agent_name}")
        print("-" * 30)
        
        try:
            agent = agent_class()
            
            for i, query in enumerate(test_queries, 1):
                try:
                    response = agent.chat(query)
                    print(f"{i}. Query: {query}")
                    print(f"   Response: {response[:100]}..." if len(response) > 100 else f"   Response: {response}")
                except Exception as e:
                    print(f"{i}. Query: {query}")
                    print(f"   Error: {str(e)}")
                    
        except Exception as e:
            print(f"   Failed to create {agent_name}: {e}")


# Usage examples for the protocol
def usage_examples():
    """Show various ways to use the math agents."""
    
    print("\n📖 Math Agent Usage Examples")
    print("=" * 40)
    
    # Method 1: Direct instantiation
    print("\n1. Direct Instantiation:")
    agent = UltimateMathAgent()
    response = agent.chat("Calculate the derivative of x² + 3x + 2")
    print(f"   Response: {response}")
    
    # Method 2: Using factory functions
    print("\n2. Factory Functions:")
    agent = create_ultimate_math_agent()
    response = agent.execute_command("/calc", expression="2^10")
    print(f"   Command result: {response}")
    
    # Method 3: Using the registry (would work with protocol server)
    print("\n3. Registry Access:")
    from src.protocol import get_agent_registry
    registry = get_agent_registry()
    
    try:
        # This would work after agents are properly registered
        card = registry.get_agent_card("math", "3.0.0")
        if card:
            print(f"   Agent info: {card.name} v{card.version} - {card.description}")
        else:
            print("   Agent not found in registry (run with protocol server)")
    except Exception as e:
        print(f"   Registry access: {e}")


if __name__ == "__main__":
    """
    Run demonstrations when executed directly.
    """
    print("🚀 Ultimate Math Agent - Example Implementation")
    print("=" * 60)
    
    # Run demonstrations
    demonstrate_math_agent_evolution()
    usage_examples()
    
    print(f"\n✅ Demonstration complete!")
    print(f"\n🌐 To run with full protocol server:")
    print(f"   python -m src.server")
    print(f"\n📚 API Documentation will be available at:")
    print(f"   http://localhost:8000/docs")