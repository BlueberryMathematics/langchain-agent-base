"""Test the toolbox functionality of the math agent."""
import sys
sys.path.insert(0, r"M:\_tools\langchain-agent-base")
sys.path.insert(0, r"M:\_tools\langchain-agent-base\examples\building-ultimate-math-agent")

from example_math_agent import create_ultimate_math_agent

print("\n🧰 Testing Toolbox Integration")
print("=" * 70)

# Create agent
agent = create_ultimate_math_agent(enable_memory=False)

print("\n1️⃣ Current tool count:")
print(f"   📊 Agent has {len(agent.list_tools())} tools")

print("\n2️⃣ Attempting to generate a Fibonacci tool...")
print("   Description: 'Calculate the Fibonacci sequence up to n terms'")

try:
    success = agent.generate_and_add_tool(
        "Calculate the Fibonacci sequence up to n terms and return as a list",
        category="math"
    )
    
    if success:
        print("   ✅ Tool generated successfully!")
        print(f"   📊 Agent now has {len(agent.list_tools())} tools")
        
        # Test the new tool
        print("\n3️⃣ Testing the generated Fibonacci tool...")
        response = agent.chat("Generate the first 10 Fibonacci numbers")
        print(f"   🤖 Response: {response[:200]}...")
    else:
        print("   ⚠️  Tool generation failed")
        print("   Note: This requires an API key with tool generation capabilities")
        
except Exception as e:
    print(f"   ⚠️  Error: {str(e)}")
    print("   Note: Toolbox features require proper API configuration")

print("\n" + "=" * 70)
print("✅ Toolbox test completed!")
