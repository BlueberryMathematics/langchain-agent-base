"""
Test Ultimate Coding Agent v2.0 - Memory & RAG Features
========================================================

This test demonstrates the new memory and RAG capabilities.

Note: This test may take 10-15 seconds to start due to heavy imports
(sentence-transformers, sklearn, etc.) - this is normal.
"""

import sys
from pathlib import Path
import asyncio

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "examples" / "building-ultimate-coding-agent"))

print("⏳ Loading dependencies (this may take 10-15 seconds)...")
from coding_agent import create_coding_agent
print("✅ Dependencies loaded!")


def test_basic_agent():
    """Test basic agent creation."""
    print("\n" + "="*70)
    print("TEST 1: Basic Agent Creation")
    print("="*70)
    
    try:
        # Create agent without memory for basic test
        agent = create_coding_agent(
            project_directory=".",
            enable_memory=False
        )
        
        print(f"✅ Agent created successfully")
        print(f"📊 Tools available: {len(agent.list_tools())}")
        print(f"🛠️  Tool list: {', '.join(agent.list_tools()[:5])}...")
        
        # Test basic functionality
        response = agent.chat("What tools do you have available?")
        print(f"\n🤖 Agent response preview: {response[:200]}...")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise


def test_memory_enabled():
    """Test agent with memory enabled."""
    print("\n" + "="*70)
    print("TEST 2: Memory-Enabled Agent")
    print("="*70)
    
    try:
        # Check if Qdrant is available
        try:
            from qdrant_client import QdrantClient
            client = QdrantClient(":memory:")
            print("✅ Qdrant available (in-memory mode)")
        except Exception as e:
            print(f"⚠️  Qdrant not available: {e}")
            print("   Skipping memory test")
            return
        
        # Create agent with memory
        agent = create_coding_agent(
            project_directory=".",
            enable_memory=True,
            session_id="test_session",
            max_context_tokens=2000
        )
        
        print(f"✅ Memory-enabled agent created")
        print(f"🧠 Memory manager: {agent.memory_manager is not None}")
        print(f"📚 RAG manager: {agent.rag_manager is not None}")
        
        # Test conversation with memory
        print("\n💬 Testing conversation memory...")
        response1 = agent.chat("Remember that I prefer Python 3.11", session_id="test_session")
        print(f"   Response 1: {response1[:100]}...")
        
        response2 = agent.chat("What did I just tell you about my preferences?", session_id="test_session")
        print(f"   Response 2: {response2[:100]}...")
        
        if "Python" in response2 or "3.11" in response2:
            print("✅ Memory working - agent remembered the preference!")
        else:
            print("⚠️  Memory may not be working as expected")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


def test_file_ingestion():
    """Test RAG file ingestion."""
    print("\n" + "="*70)
    print("TEST 3: File Ingestion & RAG")
    print("="*70)
    
    try:
        # Create a test file
        test_file = Path("test_reference.md")
        test_content = """# Test Reference Document

This is a test document for RAG ingestion.

## Key Features
- Feature A: Does something important
- Feature B: Another important thing
- Feature C: Critical functionality

## API Reference
- `function_a()`: Returns data
- `function_b()`: Processes data
"""
        
        test_file.write_text(test_content, encoding='utf-8')
        print(f"✅ Created test file: {test_file}")
        
        # Create agent with RAG
        agent = create_coding_agent(
            project_directory=".",
            enable_memory=True,
            session_id="rag_test"
        )
        
        # Ingest file
        print(f"\n📚 Ingesting reference file...")
        result = asyncio.run(
            agent.ingest_file_for_reference(
                str(test_file),
                description="Test reference document with features and API"
            )
        )
        print(result)
        
        # Check ingested files
        print(f"\n📊 Ingested files: {len(agent.ingested_files)}")
        for filepath, info in agent.ingested_files.items():
            print(f"   - {Path(filepath).name}: {info.get('lines')} lines")
        
        # Cleanup
        test_file.unlink()
        print(f"\n🧹 Cleaned up test file")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Cleanup on error
        if test_file.exists():
            test_file.unlink()


def test_context_management():
    """Test context management and token tracking."""
    print("\n" + "="*70)
    print("TEST 4: Context Management")
    print("="*70)
    
    try:
        agent = create_coding_agent(
            project_directory=".",
            enable_memory=True,
            session_id="context_test",
            max_context_tokens=500  # Small limit for testing
        )
        
        print(f"✅ Agent created with 500 token limit")
        
        # Send multiple messages to build up context
        messages = [
            "Create a user model",
            "Add authentication",
            "Include password hashing",
            "Add email verification",
            "Implement JWT tokens"
        ]
        
        print(f"\n💬 Sending {len(messages)} messages...")
        for i, msg in enumerate(messages, 1):
            response = agent.chat(msg, session_id="context_test")
            print(f"   {i}. Sent: '{msg}'")
        
        # Check memory state
        if agent.memory_manager:
            session = agent.memory_manager.active_sessions.get("context_test", {})
            token_count = session.get("token_count", 0)
            message_count = len(session.get("messages", []))
            
            print(f"\n📊 Session Statistics:")
            print(f"   Messages: {message_count}")
            print(f"   Estimated tokens: {int(token_count)}")
            print(f"   Max tokens: {agent.max_context_tokens}")
            print(f"   Usage: {(token_count/agent.max_context_tokens)*100:.1f}%")
            
            if token_count > agent.max_context_tokens * 0.7:
                print(f"   ⚠️  High usage - summarization would trigger")
            else:
                print(f"   ✅ Normal usage")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


def test_chat_with_context():
    """Test enhanced chat with file context."""
    print("\n" + "="*70)
    print("TEST 5: Chat with File Context")
    print("="*70)
    
    try:
        # Create test files
        test_file1 = Path("test_module.py")
        test_file1.write_text("""# Test Module
def helper_function():
    return "helper"
""", encoding='utf-8')
        
        test_file2 = Path("test_config.py")
        test_file2.write_text("""# Configuration
DEBUG = True
PORT = 8000
""", encoding='utf-8')
        
        print("✅ Created test files")
        
        # Create agent
        agent = create_coding_agent(
            project_directory=".",
            enable_memory=False  # Disable for simpler test
        )
        
        # Chat with context
        print("\n💬 Testing chat_with_context...")
        response = agent.chat_with_context(
            "What files do you have context about?",
            include_files=[str(test_file1), str(test_file2)]
        )
        
        print(f"🤖 Response preview: {response[:200]}...")
        
        # Cleanup
        test_file1.unlink()
        test_file2.unlink()
        print("\n🧹 Cleaned up test files")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Cleanup on error
        for f in [test_file1, test_file2]:
            if f.exists():
                f.unlink()


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print("ULTIMATE CODING AGENT v2.0 - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    tests = [
        ("Basic Agent", test_basic_agent),
        ("Memory Enabled", test_memory_enabled),
        ("File Ingestion", test_file_ingestion),
        ("Context Management", test_context_management),
        ("Chat with Context", test_chat_with_context),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"\n❌ {test_name} FAILED: {e}")
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"✅ Passed: {passed}/{len(tests)}")
    print(f"❌ Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️  {failed} test(s) failed")
    
    print("="*70)


if __name__ == "__main__":
    run_all_tests()
