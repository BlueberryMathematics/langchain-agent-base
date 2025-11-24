"""
Toolbox System Demonstration
=============================

Complete example showing how to use the toolbox system for dynamic tool management.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.toolbox import ToolboxManager, get_toolbox
from src.tool_generator import ToolGenerator, ToolAssistant, generate_tool
from src.base import Agent


def demo_basic_toolbox():
    """Demonstrate basic toolbox functionality."""
    print("\n" + "=" * 70)
    print("📦 DEMO 1: Basic Toolbox Operations")
    print("=" * 70)
    
    # Initialize toolbox
    toolbox = ToolboxManager(toolbox_dir="demo_toolbox")
    
    # Add a tool from code
    print("\n1️⃣ Adding tool from code...")
    tool_code = '''
@tool
def calculate_fibonacci(n: int) -> str:
    """
    Calculate the nth Fibonacci number.
    
    Args:
        n: Position in Fibonacci sequence (must be >= 0)
    
    Returns:
        String with the nth Fibonacci number
    """
    try:
        if n < 0:
            return "Error: n must be non-negative"
        
        if n <= 1:
            return f"fibonacci({n}) = {n}"
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        
        return f"fibonacci({n}) = {b}"
    
    except Exception as e:
        return f"Error: {str(e)}"
'''
    
    success, message, tool = toolbox.add_tool_from_code(
        tool_code,
        category="math",
        author="demo",
        tags=["fibonacci", "sequence", "math"]
    )
    
    print(f"   Result: {message}")
    
    if success and tool:
        # Test the tool
        print(f"\n   Testing fibonacci tool:")
        print(f"   • {tool.invoke({'n': 10})}")
        print(f"   • {tool.invoke({'n': 0})}")
        print(f"   • {tool.invoke({'n': -1})}")
    
    # List all tools
    print("\n2️⃣ Listing all tools in toolbox...")
    tools = toolbox.list_tools()
    for t in tools:
        print(f"   • {t['name']} ({t['category']}) - {t['description'][:60]}...")
    
    # Get tools by category
    print("\n3️⃣ Getting math tools...")
    math_tools = toolbox.get_tools_by_category("math")
    print(f"   Found {len(math_tools)} math tools")
    
    # Test a tool
    print("\n4️⃣ Testing tool with test cases...")
    test_results = toolbox.test_tool("calculate_fibonacci", [
        {'input': {'n': 5}, 'expected': '5'},
        {'input': {'n': 10}, 'expected': '55'},
        {'input': {'n': 0}, 'expected': '0'}
    ])
    print(f"   Tests: {test_results['passed']}/{test_results['total_tests']} passed")


def demo_llm_tool_generation():
    """Demonstrate LLM-based tool generation."""
    print("\n" + "=" * 70)
    print("🤖 DEMO 2: LLM-Assisted Tool Generation")
    print("=" * 70)
    
    generator = ToolGenerator()
    
    # Generate a statistics tool
    print("\n1️⃣ Generating a statistics tool...")
    success, message, tool = generator.generate_tool(
        description="Calculate the median of a list of numbers",
        category="math",
        examples=[
            "median([1, 2, 3, 4, 5]) should return 3",
            "median([1, 2, 3, 4]) should return 2.5"
        ]
    )
    
    print(f"   Result: {message}")
    
    if success and tool:
        print(f"\n   Testing generated tool:")
        print(f"   • {tool.invoke({'numbers': '1,2,3,4,5'})}")
    
    # Generate a custom domain tool
    print("\n2️⃣ Generating a custom tool...")
    success, message, tool = generator.generate_tool(
        description="Convert temperature between Celsius, Fahrenheit, and Kelvin",
        category="science"
    )
    
    print(f"   Result: {message}")
    
    # Generate a collection of tools
    print("\n3️⃣ Generating a collection of geometry tools...")
    success, message, tools = generator.generate_tool_collection(
        domain="geometry",
        num_tools=3
    )
    
    print(f"   Result: {message}")
    if tools:
        for t in tools:
            print(f"   • {t.name}: {t.description[:60]}...")


def demo_agent_integration():
    """Demonstrate toolbox integration with agents."""
    print("\n" + "=" * 70)
    print("🤝 DEMO 3: Agent Integration with Toolbox")
    print("=" * 70)
    
    # Create agent
    print("\n1️⃣ Creating agent with toolbox integration...")
    agent = Agent(
        system_prompt="I am a mathematical assistant with dynamically loaded tools."
    )
    
    # Load tools from toolbox
    print("\n2️⃣ Loading math tools from toolbox...")
    agent.load_tools_from_toolbox(category="math")
    
    print(f"\n   Agent now has {len(agent.list_tools())} tools:")
    for tool_name in agent.list_tools():
        print(f"   • {tool_name}")
    
    # Use loaded tools
    print("\n3️⃣ Using loaded tools...")
    if agent.list_tools():
        response = agent.chat("Calculate fibonacci number for n=8")
        print(f"   Response: {response}")
    
    # Generate and add a tool on-the-fly
    print("\n4️⃣ Generating a new tool on-the-fly...")
    success = agent.generate_and_add_tool(
        description="Calculate the greatest common divisor (GCD) of two numbers",
        category="math"
    )
    
    if success:
        print(f"\n   Agent now has {len(agent.list_tools())} tools (added GCD)")
        response = agent.chat("What's the GCD of 48 and 18?")
        print(f"   Response: {response}")


def demo_tool_validation():
    """Demonstrate tool validation and safety checks."""
    print("\n" + "=" * 70)
    print("🛡️ DEMO 4: Tool Validation & Safety")
    print("=" * 70)
    
    toolbox = ToolboxManager(toolbox_dir="demo_toolbox")
    
    # Try to add a safe tool
    print("\n1️⃣ Adding a safe tool...")
    safe_code = '''
@tool
def safe_calculator(expression: str) -> str:
    """Safely evaluate a mathematical expression."""
    import math
    try:
        result = eval(expression, {"__builtins__": {}}, {"math": math})
        return f"{expression} = {result}"
    except:
        return "Error evaluating expression"
'''
    
    success, message, _ = toolbox.add_tool_from_code(safe_code, category="math")
    print(f"   Result: {message}")
    
    # Try to add a dangerous tool
    print("\n2️⃣ Trying to add a dangerous tool (should fail)...")
    dangerous_code = '''
@tool
def dangerous_tool(command: str) -> str:
    """This tool tries to use subprocess."""
    import subprocess
    result = subprocess.run(command, shell=True)
    return str(result)
'''
    
    success, message, _ = toolbox.add_tool_from_code(dangerous_code, category="custom")
    print(f"   Result: {message}")
    print(f"   Success: {success} (should be False)")
    
    # Try tool without @tool decorator
    print("\n3️⃣ Trying to add tool without @tool decorator (should fail)...")
    no_decorator_code = '''
def not_a_tool(x: int) -> str:
    """This is not decorated with @tool."""
    return str(x * 2)
'''
    
    success, message, _ = toolbox.add_tool_from_code(no_decorator_code, category="custom")
    print(f"   Result: {message}")
    print(f"   Success: {success} (should be False)")


def demo_tool_management():
    """Demonstrate advanced tool management features."""
    print("\n" + "=" * 70)
    print("⚙️ DEMO 5: Advanced Tool Management")
    print("=" * 70)
    
    toolbox = ToolboxManager(toolbox_dir="demo_toolbox")
    assistant = ToolAssistant(toolbox=toolbox)
    
    # Suggest tools for a task
    print("\n1️⃣ Suggesting tools for a task...")
    task = "I need to calculate statistical measures of a dataset"
    suggestions = assistant.suggest_tools_for_task(task)
    
    print(f"   Task: {task}")
    print(f"   Suggested tools ({len(suggestions)}):")
    for sugg in suggestions:
        print(f"   • {sugg['name']}: {sugg['description'][:50]}... (relevance: {sugg['relevance']})")
    
    # Batch create tools
    print("\n2️⃣ Batch creating tools...")
    descriptions = [
        "Calculate the mode (most frequent value) of a list",
        "Calculate the range (max - min) of a list",
        "Calculate percentiles of a dataset"
    ]
    
    results = assistant.batch_create_tools(descriptions, category="math")
    print(f"   Created {results['success']}/{results['total']} tools")
    for tool_info in results['tools']:
        print(f"   • {tool_info['message']}")
    
    # Export tools
    print("\n3️⃣ Exporting math tools to file...")
    export_msg = toolbox.export_tools("exported_math_tools.py", category="math")
    print(f"   {export_msg}")


def demo_complete_workflow():
    """Demonstrate complete workflow: generate -> test -> use."""
    print("\n" + "=" * 70)
    print("🔄 DEMO 6: Complete Workflow")
    print("=" * 70)
    
    # Step 1: Generate tool
    print("\n1️⃣ Step 1: Generate a prime number checker tool...")
    success, message, tool = generate_tool(
        description="Check if a number is prime and return detailed explanation",
        category="math"
    )
    print(f"   {message}")
    
    if not success or not tool:
        print("   ⚠️  Tool generation failed")
        return
    
    # Step 2: Test the tool
    print("\n2️⃣ Step 2: Test the generated tool...")
    toolbox = get_toolbox()
    test_results = toolbox.test_tool(tool.name, [
        {'input': {'number': 7}, 'expected': 'prime'},
        {'input': {'number': 10}, 'expected': 'not prime'},
        {'input': {'number': 2}, 'expected': 'prime'}
    ])
    
    print(f"   Tests: {test_results['passed']}/{test_results['total_tests']} passed")
    for result in test_results['test_results']:
        status = "✅" if result['passed'] else "❌"
        print(f"   {status} Test {result['test_number']}: {result['input']}")
    
    # Step 3: Use in agent
    print("\n3️⃣ Step 3: Use tool in agent...")
    agent = Agent()
    agent.add_tool(tool)
    
    response = agent.chat("Is 17 a prime number?")
    print(f"   Agent response: {response}")
    
    # Step 4: Improve tool if needed
    print("\n4️⃣ Step 4: Improve the tool...")
    generator = ToolGenerator()
    success, message, improved_tool = generator.improve_tool(
        tool.name,
        improvements="Add support for checking multiple numbers at once"
    )
    print(f"   {message}")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("🧰 TOOLBOX SYSTEM DEMONSTRATION")
    print("=" * 70)
    print("\nThis demonstration shows how to:")
    print("  • Create and manage tools dynamically")
    print("  • Generate tools using LLM assistance")
    print("  • Integrate tools with agents")
    print("  • Validate and test tools")
    print("  • Export and share tools")
    
    try:
        demo_basic_toolbox()
        demo_llm_tool_generation()
        demo_agent_integration()
        demo_tool_validation()
        demo_tool_management()
        demo_complete_workflow()
        
        print("\n" + "=" * 70)
        print("✅ ALL DEMONSTRATIONS COMPLETED!")
        print("=" * 70)
        
        print("\n💡 Next steps:")
        print("  • Create your own tools with toolbox.add_tool_from_code()")
        print("  • Generate tools with generate_tool(description)")
        print("  • Load tools into agents with agent.load_tools_from_toolbox()")
        print("  • Export tools with toolbox.export_tools()")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
