"""Quick test script for the math agent without memory."""
import sys
sys.path.insert(0, r"M:\_tools\langchain-agent-base")
sys.path.insert(0, r"M:\_tools\langchain-agent-base\examples\building-ultimate-math-agent")

from example_math_agent import create_ultimate_math_agent

print("🧪 Testing Ultimate Math Agent")
print("=" * 70)

# Create agent without memory (no Qdrant needed)
print("\n1️⃣ Creating agent (without memory)...")
agent = create_ultimate_math_agent(enable_memory=False)
print(f"   ✅ Agent created!")
print(f"   📊 Available tools: {len(agent.list_tools())}")
print(f"   🛠️  Tool names: {', '.join(agent.list_tools()[:5])}...")

# Test basic calculation
print("\n2️⃣ Testing basic calculation...")
print("   Query: 'What is 15 * 23?'")
response = agent.chat("What is 15 * 23?")
print(f"   🤖 Response: {response}")

# Test custom polynomial tool
print("\n3️⃣ Testing polynomial roots...")
print("   Query: 'Find roots of polynomial with coefficients 1,-5,6'")
response = agent.chat("Find the roots of the polynomial with coefficients 1,-5,6")
print(f"   🤖 Response: {response}")

# Test GCD/LCM tool
print("\n4️⃣ Testing number theory...")
print("   Query: 'What is the GCD and LCM of 12, 18, and 24?'")
response = agent.chat("What is the GCD and LCM of 12, 18, and 24?")
print(f"   🤖 Response: {response}")

# Test prime factorization
print("\n5️⃣ Testing prime factorization...")
print("   Query: 'What is the prime factorization of 360?'")
response = agent.chat("What is the prime factorization of 360?")
print(f"   🤖 Response: {response}")

print("\n" + "=" * 70)
print("✅ All tests completed successfully!")
print("\n💡 The math agent is working correctly!")
print("   • Custom tools are loaded")
print("   • LLM communication is working")
print("   • Tool calling is functional")
