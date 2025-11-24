"""
Unified RAG-Memory-AgentCard System Example
==========================================

Demonstrates the complete integration of:
- RAG document storage and search
- Conversation memory with summarization
- Agent card storage and discovery
- Unified Qdrant backend for scalability
"""

import asyncio
from datetime import datetime, timedelta
from src.storage import UnifiedQdrantStorage
from src.memory import ConversationMemoryManager
from src.protocol import register_agent, AgentStatus, get_agent_registry
from src.base import Agent, create_memory_enhanced_agent
from src.tools import get_math_tools
from src.toolbox import get_toolbox
from src.tool_generator import generate_tool


async def demonstrate_unified_system():
    """Comprehensive demonstration of the unified system."""
    
    print("🚀 Starting Unified RAG-Memory-AgentCard System Demo")
    print("=" * 60)
    
    # 1. Initialize unified storage
    print("\n1️⃣ Setting up unified Qdrant storage...")
    unified_storage = UnifiedQdrantStorage()
    
    # 2. Create and register specialized agents
    print("\n2️⃣ Creating and registering specialized agents...")
    
    @register_agent("unified_math", version="1.0.0", 
                    domain="mathematics", 
                    status=AgentStatus.PRODUCTION)
    class UnifiedMathAgent(Agent):
        """Math agent with memory and RAG capabilities."""
        def __init__(self):
            super().__init__(
                system_prompt="""I am a mathematical assistant with access to:
                - Conversation memory (can recall our previous discussions)
                - Document search (can find relevant mathematical resources)
                - Advanced mathematical tools and calculations
                
                I use memory to maintain context and can search documents for references.""",
                tools=get_math_tools(),
                enable_memory=True
            )
    
    # 3. Test agent card storage and search
    print("\n3️⃣ Testing agent card storage...")
    registry = get_agent_registry()
    agents = registry.list_agents()
    print(f"📋 Found {len(agents)} registered agents")
    for agent in agents[-3:]:  # Show last 3
        print(f"   - {agent.name} v{agent.version} ({agent.domain})")
    
    # 4. Create memory-enhanced agent
    print("\n4️⃣ Creating memory-enhanced agent...")
    memory_agent = create_memory_enhanced_agent()
    
    # 5. Test conversation memory
    print("\n5️⃣ Testing conversation memory...")
    session_id = "demo_session"
    
    # Simulate conversation
    conversations = [
        ("What's the quadratic formula?", "The quadratic formula is x = (-b ± √(b²-4ac)) / 2a"),
        ("Can you solve x² + 5x + 6 = 0?", "Using the quadratic formula: x = -2 or x = -3"),
        ("What about factoring methods?", "You can factor x² + 5x + 6 as (x+2)(x+3) = 0"),
        ("I'm working on a Python ML project", "Great! What type of machine learning problem are you solving?"),
        ("It's image classification with neural networks", "For image classification, consider using CNN architectures like ResNet or EfficientNet")
    ]
    
    memory_manager = ConversationMemoryManager(unified_storage)
    
    for message, response in conversations:
        await memory_manager.add_message(
            session_id=session_id,
            message=message,
            response=response,
            metadata={"demo": True, "topic": "math" if "quadratic" in message.lower() else "ml"}
        )
        print(f"💬 Stored: {message[:30]}...")
    
    # 6. Test memory search
    print("\n6️⃣ Testing memory search capabilities...")
    
    # Search by topic
    math_results = await memory_manager.search_memory(
        query="quadratic equation solving",
        session_id=session_id,
        limit=3
    )
    print(f"🔍 Math search found {len(math_results)} results:")
    for result in math_results:
        print(f"   📅 {result['timestamp'][:16]} - {result['message'][:40]}...")
    
    # Search by time range
    recent_time = datetime.now() - timedelta(minutes=5)
    recent_results = await memory_manager.search_memory(
        query="machine learning",
        session_id=session_id,
        time_range=(recent_time, datetime.now()),
        limit=2
    )
    print(f"🕐 Recent ML search found {len(recent_results)} results:")
    for result in recent_results:
        print(f"   📅 {result['timestamp'][:16]} - {result['message'][:40]}...")
    
    # 7. Test RAG document integration
    print("\n7️⃣ Testing RAG document storage...")
    rag_storage = unified_storage.get_rag_storage("math_docs")
    
    # Store some math documents
    math_documents = [
        {
            "content": "The quadratic formula is derived from completing the square method. It provides solutions to any quadratic equation ax² + bx + c = 0.",
            "metadata": {"topic": "algebra", "difficulty": "intermediate", "source": "textbook"}
        },
        {
            "content": "Linear algebra deals with vectors, matrices, and systems of linear equations. Matrix multiplication is a fundamental operation.",
            "metadata": {"topic": "linear_algebra", "difficulty": "advanced", "source": "reference"}
        },
        {
            "content": "Machine learning uses mathematical optimization to find patterns in data. Gradient descent is a key algorithm for training neural networks.",
            "metadata": {"topic": "machine_learning", "difficulty": "advanced", "source": "paper"}
        }
    ]
    
    doc_ids = await rag_storage.store_documents(math_documents)
    print(f"📚 Stored {len(doc_ids)} documents in RAG storage")
    
    # Search documents
    doc_results = await rag_storage.search_documents(
        query="quadratic formula algebra",
        filters={"topic": "algebra"},
        limit=2
    )
    print(f"🔍 Document search found {len(doc_results)} results:")
    for result in doc_results:
        print(f"   📖 Score: {result['score']:.3f} - {result['content'][:50]}...")
    
    # 8. Test unified search across all data types
    print("\n8️⃣ Testing unified search capabilities...")
    
    # Create memory-enhanced agent with access to all data
    unified_agent = create_memory_enhanced_agent(
        system_prompt="""I am an advanced assistant with access to:
        1. Conversation memory - our previous discussions
        2. Document library - mathematical and technical references  
        3. Agent registry - available specialized agents
        
        I can search across all these sources to provide comprehensive answers."""
    )
    
    # Test conversation with memory context
    print("🤖 Testing memory-enhanced conversation...")
    response1 = unified_agent.chat(
        "What did we discuss about quadratic equations earlier?",
        session_id=session_id
    )
    print(f"🔮 Agent response (with memory): {response1[:100]}...")
    
    response2 = unified_agent.chat(
        "Can you find information about machine learning in our conversation?",
        session_id=session_id
    )
    print(f"🔮 Agent response (with search): {response2[:100]}...")
    
    # 9. Demonstrate scaling features
    print("\n9️⃣ Demonstrating scaling features...")
    
    # Show storage statistics
    agent_storage = unified_storage.get_agent_storage()
    stats = agent_storage.get_storage_stats()
    print(f"📊 Storage Statistics:")
    print(f"   - Agent cards: {stats.get('agent_count', 0)}")
    print(f"   - Conversations: Available in unified storage")
    print(f"   - Documents: Available in unified storage")
    print(f"   - Total collections: {len(unified_storage.collections)}")
    
    # Test memory compression (simulate large conversation)
    print("\n🗜️  Testing memory compression...")
    
    # Add many messages to trigger summarization
    for i in range(10):
        await memory_manager.add_message(
            session_id="compression_test",
            message=f"This is message number {i+1} about various mathematical topics and formulas.",
            response=f"Thank you for message {i+1}. I understand you're asking about mathematical concepts.",
            metadata={"test": "compression", "message_number": i+1}
        )
    
    print("✅ Added messages for compression testing")
    
    # Search compressed session
    compressed_results = await memory_manager.search_memory(
        query="mathematical topics",
        session_id="compression_test",
        limit=5
    )
    print(f"📝 Found {len(compressed_results)} results in compressed session")
    
    # 10. Toolbox integration with unified system
    print("\n🔟 Demonstrating toolbox in unified system...")
    
    print("Generating specialized tool for math agent...")
    success, message, tool = generate_tool(
        "Calculate the area under a curve using numerical integration (trapezoidal rule)",
        category="math"
    )
    
    if success:
        print(f"✅ {message}")
        
        # Add to memory-enhanced agent
        unified_agent.add_tool(tool)
        print(f"Tool integrated with memory-enhanced agent")
        
        # Store tool usage in conversation
        await memory_manager.add_message(
            session_id=session_id,
            message="I generated a new integration tool",
            response=f"Created tool: {tool.name}",
            metadata={"event": "tool_generation", "category": "math"}
        )
    
    # Show toolbox contents
    toolbox = get_toolbox()
    all_tools = toolbox.list_tools()
    print(f"\n📦 Toolbox contains {len(all_tools)} tools across all categories")
    
    print("\n✅ Unified System Demo Complete!")
    print("\n🎯 Key Features Demonstrated:")
    print("   ✓ Unified Qdrant storage for all data types")
    print("   ✓ Agent card registration and discovery")
    print("   ✓ Conversation memory with temporal search")
    print("   ✓ RAG document storage and retrieval")
    print("   ✓ Cross-system search and integration")
    print("   ✓ Automatic memory compression")
    print("   ✓ Memory-enhanced agent interactions")
    print("   ✓ Dynamic toolbox integration with all systems")
    
    return {
        "unified_storage": unified_storage,
        "memory_manager": memory_manager,
        "agent_registry": registry,
        "memory_agent": unified_agent
    }


async def interactive_demo():
    """Interactive demo for testing the unified system."""
    
    print("\n🎮 Interactive Unified System Demo")
    print("=" * 40)
    
    # Setup
    components = await demonstrate_unified_system()
    memory_agent = components["memory_agent"]
    session_id = "interactive_session"
    
    print("\n💬 You can now chat with the memory-enhanced agent!")
    print("   - It remembers our conversation")
    print("   - It can search previous discussions") 
    print("   - It has access to document library")
    print("   - Type 'quit' to exit")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if user_input:
                print("🤖 Thinking...")
                response = memory_agent.chat(user_input, session_id=session_id)
                print(f"Agent: {response}")
                print()
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n👋 Thanks for testing the unified system!")


if __name__ == "__main__":
    print("🚀 LangChain Agent Base - Unified System Demo")
    
    # Run basic demonstration
    asyncio.run(demonstrate_unified_system())
    
    # Uncomment for interactive demo
    # asyncio.run(interactive_demo())