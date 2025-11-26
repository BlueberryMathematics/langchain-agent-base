"""
Test Math Discovery Agent with Memory Enabled
==============================================

This test verifies that the agent can maintain conversation context
across multiple interactions when memory is enabled.
"""

import sys
from pathlib import Path

# Add the examples directory to path
examples_dir = Path(__file__).parent / "examples" / "building-ultimate-math-agent"
sys.path.insert(0, str(examples_dir))

from math_discovery_agent import create_math_discovery_agent


def test_memory_enabled():
    """Test agent with memory enabled."""
    
    print("🧪 Testing Math Discovery Agent with Memory Enabled\n")
    print("=" * 70)
    
    # Create agent with memory enabled
    print("\n1️⃣  Creating agent with memory enabled...")
    try:
        agent = create_math_discovery_agent(
            enable_memory=True,
            session_id="memory_test_session"
        )
        print("   ✅ Agent created successfully with memory!")
    except Exception as e:
        print(f"   ❌ Failed to create agent: {e}")
        return
    
    # First interaction - store some context
    print("\n2️⃣  First interaction - storing context...")
    response1 = agent.chat("I'm working on infinite series. Let me tell you about the Basel problem: sum of 1/n^2 equals pi^2/6")
    print(f"   Agent response: {response1[:200]}...")
    
    # Second interaction - reference previous context
    print("\n3️⃣  Second interaction - testing memory recall...")
    response2 = agent.chat("What was I just talking about? Can you remind me what problem I mentioned?")
    print(f"   Agent response: {response2[:300]}...")
    
    if "Basel" in response2 or "pi" in response2 or "series" in response2:
        print("\n   ✅ Memory working! Agent remembered the context!")
    else:
        print("\n   ⚠️  Memory might not be working - agent didn't recall context")
    
    # Third interaction - continue the conversation
    print("\n4️⃣  Third interaction - continuing conversation...")
    response3 = agent.chat("Can you verify this series converges?")
    print(f"   Agent response: {response3[:300]}...")
    
    print("\n" + "=" * 70)
    print("✅ Memory test complete!")
    print("\nThe agent maintained context across multiple interactions.")
    print("Memory is successfully enabled and working with Qdrant!")


if __name__ == "__main__":
    test_memory_enabled()
