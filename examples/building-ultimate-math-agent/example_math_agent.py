"""
Example: Ultimate Math Agent Implementation
============================================

This file shows the complete structure of your custom math agent.
This is what you'll build in your own project!
"""

from src.base import Agent
from src.tools import get_math_tools
from src.protocol import register_agent, AgentStatus
from src.commands import create_math_commands
from src.toolbox import get_toolbox
from src.tool_generator import generate_tool

# In your real project, you'd import from your custom_tools/ directory:
# from custom_tools.calculus import get_calculus_tools
# from custom_tools.statistics import get_statistics_tools
# from custom_tools.linear_algebra import get_linear_algebra_tools

# For this example, we'll use the built-in tools
from langchain_core.tools import tool


# Example: A few custom tools you might add
@tool
def polynomial_roots(coefficients: str) -> str:
    """
    Find roots of a polynomial given coefficients.
    
    Args:
        coefficients: Comma-separated coefficients from highest to lowest degree
                     e.g., "1,-5,6" for x² - 5x + 6
    
    Returns:
        The roots of the polynomial
    """
    try:
        import numpy as np
        coeffs = [float(c.strip()) for c in coefficients.split(',')]
        roots = np.roots(coeffs)
        
        real_roots = [r.real for r in roots if abs(r.imag) < 1e-10]
        complex_roots = [r for r in roots if abs(r.imag) >= 1e-10]
        
        result = []
        if real_roots:
            result.append(f"Real roots: {', '.join(f'{r:.4f}' for r in real_roots)}")
        if complex_roots:
            result.append(f"Complex roots: {', '.join(f'{r.real:.4f}+{r.imag:.4f}i' for r in complex_roots)}")
        
        return ' | '.join(result) if result else "No roots found"
    except Exception as e:
        return f"Error finding roots: {str(e)}"


@tool  
def gcd_lcm(numbers: str) -> str:
    """
    Calculate GCD (Greatest Common Divisor) and LCM (Least Common Multiple) of numbers.
    
    Args:
        numbers: Comma-separated integers, e.g., "12,18,24"
    
    Returns:
        The GCD and LCM of the numbers
    """
    try:
        import math
        from functools import reduce
        
        nums = [int(n.strip()) for n in numbers.split(',')]
        
        # Calculate GCD
        gcd_result = reduce(math.gcd, nums)
        
        # Calculate LCM
        def lcm(a, b):
            return abs(a * b) // math.gcd(a, b)
        lcm_result = reduce(lcm, nums)
        
        return f"Numbers: {nums} | GCD: {gcd_result} | LCM: {lcm_result}"
    except Exception as e:
        return f"Error calculating GCD/LCM: {str(e)}"


@tool
def prime_factorization(number: int) -> str:
    """
    Find the prime factorization of a number.
    
    Args:
        number: Integer to factorize
    
    Returns:
        Prime factorization in the form: number = p1^a1 * p2^a2 * ...
    """
    try:
        if number < 2:
            return f"{number} is not factorizable (must be >= 2)"
        
        n = abs(number)
        factors = {}
        d = 2
        
        while d * d <= n:
            while n % d == 0:
                factors[d] = factors.get(d, 0) + 1
                n //= d
            d += 1
        
        if n > 1:
            factors[n] = factors.get(n, 0) + 1
        
        # Format output
        factor_str = ' × '.join(
            f"{p}^{e}" if e > 1 else str(p)
            for p, e in sorted(factors.items())
        )
        
        return f"{abs(number)} = {factor_str}"
    except Exception as e:
        return f"Error factorizing: {str(e)}"


# Register your agent with the protocol system
@register_agent(
    name="ultimate_math",
    version="1.0.0",
    domain="mathematics",
    category="specialist",
    description="Ultimate mathematical assistant with calculus, algebra, number theory, and statistics",
    author="Your Name Here",
    status=AgentStatus.PRODUCTION,
    tags=["math", "calculus", "algebra", "statistics", "number-theory"]
)
class UltimateMathAgent(Agent):
    """
    Your Ultimate Math Agent - A Specialized Mathematical Assistant
    
    This agent combines:
    - Built-in math tools from the framework (calculator, quadratic solver, matrices)
    - Custom calculus tools (derivatives, integrals, limits)
    - Custom algebra tools (polynomial roots, factorization)
    - Custom number theory tools (GCD, LCM, prime factorization)
    - Conversation memory for contextual assistance
    - Command system for fast operations
    
    Features:
    - Step-by-step solutions
    - Clear explanations of mathematical concepts
    - Remembers conversation history
    - Fast command execution for common operations
    """
    
    def __init__(self, 
                 enable_memory: bool = True,
                 memory_session_id: str = "math_session",
                 **kwargs):
        """
        Initialize the Ultimate Math Agent.
        
        Args:
            enable_memory: Enable conversation memory (default: True)
            memory_session_id: Session ID for memory persistence
            **kwargs: Additional arguments passed to base Agent
        """
        
        # Initialize with enhanced system prompt
        super().__init__(
            system_prompt="""I am the Ultimate Math Agent, your specialized mathematical assistant.

I excel at:
• Calculus: derivatives, integrals, limits, series expansions
• Algebra: equations, polynomials, factorization, simplification
• Linear Algebra: matrices, vectors, eigenvalues, transformations
• Statistics: descriptive stats, probability, distributions
• Number Theory: GCD, LCM, prime factorization, modular arithmetic
• Symbolic Mathematics: exact solutions and symbolic manipulation

My Approach:
1. I show step-by-step solutions with clear explanations
2. I verify my work and check for edge cases
3. I explain mathematical concepts when helpful
4. I remember our conversation history for contextual assistance
5. I can handle both numerical and symbolic mathematics

I use precise mathematical notation and provide accurate, verified results.""",
            enable_memory=enable_memory,
            memory_session_id=memory_session_id,
            enable_commands=True,
            **kwargs
        )
        
        print("🔧 Initializing Ultimate Math Agent...")
        
        # Add built-in math tools from the framework
        print("  📦 Adding framework math tools...")
        self.add_tools(get_math_tools())
        
        # Add your custom tools
        print("  🎯 Adding custom tools...")
        custom_tools = [
            polynomial_roots,
            gcd_lcm,
            prime_factorization,
            # In your real project, you'd add:
            # *get_calculus_tools(),
            # *get_statistics_tools(),
            # *get_linear_algebra_tools(),
        ]
        self.add_tools(custom_tools)
        
        # Add math commands for fast operations
        print("  ⚡ Adding command shortcuts...")
        for cmd in create_math_commands():
            self.add_command(cmd)
        
        # Load any additional tools from toolbox
        print("  🧰 Loading tools from toolbox...")
        try:
            self.load_tools_from_toolbox(category="math")
            print(f"     Loaded {len(self.list_tools()) - len(custom_tools) - len(get_math_tools())} additional tools from toolbox")
        except Exception as e:
            print(f"     Toolbox loading skipped: {e}")
        
        print(f"\n✅ Ultimate Math Agent Ready!")
        print(f"   📊 Total tools: {len(self.tools)}")
        print(f"   🛠️  Available tools: {', '.join(self.list_tools()[:5])}...")
        print(f"   ⚡ Available commands: {', '.join(self.list_commands()[:5])}...")
        print(f"   🧠 Memory: {'Enabled' if enable_memory else 'Disabled'}")
        print(f"   🆔 Session: {memory_session_id}\n")


def create_ultimate_math_agent(
    enable_memory: bool = True,
    session_id: str = "default",
    **kwargs
) -> UltimateMathAgent:
    """
    Factory function to create an Ultimate Math Agent.
    
    This is the recommended way to create your agent as it provides
    a clean API and allows for future enhancements.
    
    Args:
        enable_memory: Enable conversation memory
        session_id: Session ID for persistent memory
        **kwargs: Additional arguments for agent configuration
    
    Returns:
        Configured UltimateMathAgent instance
    
    Example:
        >>> agent = create_ultimate_math_agent()
        >>> response = agent.chat("Calculate the derivative of x^3")
        >>> print(response)
    """
    return UltimateMathAgent(
        enable_memory=enable_memory,
        memory_session_id=session_id,
        **kwargs
    )


# Example usage and demonstrations
def demonstrate_agent():
    """Demonstrate the capabilities of the Ultimate Math Agent."""
    
    print("🧪 Ultimate Math Agent Demonstration")
    print("=" * 70)
    
    # Create agent
    agent = create_ultimate_math_agent(session_id="demo_session")
    
    # Test queries covering different capabilities
    test_queries = [
        # Basic arithmetic
        ("Calculate 15 * 23 + 47", "Basic Arithmetic"),
        
        # Quadratic equations (built-in tool)
        ("Solve the quadratic equation x² - 5x + 6 = 0", "Quadratic Solver"),
        
        # Matrix operations (built-in tool)
        ("Calculate the determinant of the matrix [[1,2],[3,4]]", "Linear Algebra"),
        
        # Polynomial roots (custom tool)
        ("Find the roots of the polynomial with coefficients 1,-5,6", "Polynomial Roots"),
        
        # Number theory (custom tool)
        ("What's the GCD and LCM of 12, 18, and 24?", "Number Theory - GCD/LCM"),
        
        # Prime factorization (custom tool)
        ("Give me the prime factorization of 360", "Prime Factorization"),
        
        # Memory test - reference previous conversation
        ("What was the first calculation we did?", "Memory Test"),
    ]
    
    for query, category in test_queries:
        print(f"\n{'='*70}")
        print(f"📝 Category: {category}")
        print(f"❓ Query: {query}")
        print(f"{'-'*70}")
        
        try:
            response = agent.chat(query)
            print(f"🤖 Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'='*70}")
    print("✅ Demonstration complete!")
    print("\n💡 Key Features Demonstrated:")
    print("   • Basic calculations with built-in tools")
    print("   • Equation solving (quadratic, systems)")
    print("   • Matrix operations and linear algebra")
    print("   • Custom polynomial root finding")
    print("   • Number theory (GCD, LCM, primes)")
    print("   • Conversation memory across queries")


def demonstrate_commands():
    """Demonstrate the command system for fast operations."""
    
    print("\n⚡ Command System Demonstration")
    print("=" * 70)
    
    agent = create_ultimate_math_agent()
    
    print("\n💬 Using chat (slower - goes through LLM):")
    print("   Query: 'Calculate 15 * 23'")
    print("   → Agent reasons about the query, selects tool, executes")
    
    print("\n⚡ Using command (faster - direct execution):")
    print("   Command: agent.execute_command('/calc', expression='15 * 23')")
    try:
        result = agent.execute_command("/calc", expression="15 * 23")
        print(f"   → {result}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n📋 Available commands:")
    for cmd in agent.list_commands():
        print(f"   • {cmd}")
    
    print("\n💡 Use commands for:")
    print("   • High-frequency operations")
    print("   • Batch processing")
    print("   • API integrations")
    print("   • When you know exactly which tool to use")


def demonstrate_toolbox():
    """Demonstrate dynamic tool generation with the toolbox system."""
    
    print("\n🧰 Toolbox System Demonstration")
    print("=" * 70)
    
    agent = create_ultimate_math_agent()
    
    print("\n1️⃣ Generating a new tool dynamically...")
    print("   Description: 'Calculate the Fibonacci sequence up to n terms'")
    
    try:
        success = agent.generate_and_add_tool(
            "Calculate the Fibonacci sequence up to n terms and return as a list",
            category="math"
        )
        
        if success:
            print("   ✅ Tool generated and added!")
            print(f"   📊 Agent now has {len(agent.list_tools())} tools")
            
            # Test the new tool
            print("\n2️⃣ Testing the generated tool...")
            response = agent.chat("Generate the first 10 Fibonacci numbers")
            print(f"   🤖 Response: {response[:200]}...")
        else:
            print("   ⚠️  Tool generation failed (API key may be needed)")
    except Exception as e:
        print(f"   ⚠️  Toolbox feature: {e}")
    
    print("\n3️⃣ Loading tools from toolbox...")
    try:
        toolbox = get_toolbox()
        tools = toolbox.list_tools(category="math")
        print(f"   📦 Toolbox contains {len(tools)} math tools:")
        for tool_info in tools[:5]:
            print(f"      • {tool_info['name']} - {tool_info['description'][:50]}...")
    except Exception as e:
        print(f"   ⚠️  Toolbox access: {e}")
    
    print("\n💡 Toolbox benefits:")
    print("   • Generate tools from natural language")
    print("   • Persist tools across sessions")
    print("   • Share tools between agents")
    print("   • Validate and test tools automatically")
    print("   • Build your tool library over time")


# Main execution
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        # Run demonstrations
        demonstrate_agent()
        demonstrate_commands()
        demonstrate_toolbox()
    else:
        # Interactive mode
        print("🤖 Ultimate Math Agent - Interactive Mode")
        print("=" * 70)
        print("Type your math questions, or:")
        print("  • 'demo' - Run demonstration")
        print("  • 'help' - Show available tools")
        print("  • 'commands' - Show available commands")
        print("  • 'toolbox' - Show toolbox system")
        print("  • 'generate <description>' - Generate a new tool")
        print("  • 'exit' or 'quit' - End session")
        print("=" * 70)
        
        agent = create_ultimate_math_agent(session_id="interactive")
        
        while True:
            try:
                user_input = input("\n📝 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit']:
                    print("\n👋 Thanks for using Ultimate Math Agent! Goodbye!")
                    break
                
                if user_input.lower() == 'demo':
                    demonstrate_agent()
                    continue
                
                if user_input.lower() == 'help':
                    print(f"\n🛠️  Available tools: {', '.join(agent.list_tools())}")
                    continue
                
                if user_input.lower() == 'commands':
                    print(f"\n⚡ Available commands: {', '.join(agent.list_commands())}")
                    continue
                
                if user_input.lower() == 'toolbox':
                    demonstrate_toolbox()
                    continue
                
                if user_input.lower().startswith('generate '):
                    description = user_input[9:].strip()
                    if description:
                        print(f"\n🤖 Generating tool: {description}")
                        success = agent.generate_and_add_tool(description, category="math")
                        if success:
                            print(f"✅ Tool generated! Total tools: {len(agent.list_tools())}")
                        else:
                            print("⚠️  Tool generation failed")
                    else:
                        print("⚠️  Please provide a description: generate <description>")
                    continue
                
                # Process query
                response = agent.chat(user_input)
                print(f"\n🤖 Agent: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again with a different query.")
