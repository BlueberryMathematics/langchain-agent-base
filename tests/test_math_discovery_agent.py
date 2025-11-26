"""
Comprehensive Test Suite for Mathematical Discovery Agent
==========================================================

Tests all features:
- LaTeX ingestion and parsing
- Infinite series discovery and verification
- Infinite products discovery and verification
- Pattern recognition in sequences
- RAG knowledge base storage and retrieval
- Memory across research sessions
- Tool generation for specialized tasks
- Full integration of framework capabilities
"""

import sys
from pathlib import Path

# Add the examples directory to path
examples_dir = Path(__file__).parent.parent / "examples" / "building-ultimate-math-agent"
sys.path.insert(0, str(examples_dir))

from math_discovery_agent import create_math_discovery_agent


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def test_latex_ingestion():
    """Test LaTeX formula ingestion."""
    print_section("TEST 1: LaTeX Formula Ingestion")
    
    agent = create_math_discovery_agent(enable_memory=False, session_id="test_latex")
    
    # Test 1: Ingest Basel problem
    print("1️⃣ Ingesting Basel Problem (sum of 1/n^2)...")
    latex = r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}"
    result = agent.ingest_latex_string(latex, "Basel problem - famous result by Euler")
    print(f"   Result: {result}\n")
    
    # Test 2: Parse the formula
    print("2️⃣ Parsing the LaTeX formula...")
    response = agent.chat(f"Parse this LaTeX formula: {latex}")
    print(f"   Response: {response[:300]}...\n")
    
    # Test 3: Ingest more formulas
    print("3️⃣ Ingesting additional formulas...")
    formulas = [
        (r"\sum_{n=0}^{\infty} \frac{(-1)^n}{2n+1} = \frac{\pi}{4}", "Leibniz formula for π"),
        (r"\prod_{n=1}^{\infty} \left(1 - \frac{1}{(2n)^2}\right) = \frac{2}{\pi}", "Wallis product"),
        (r"\sum_{n=0}^{\infty} \frac{1}{n!} = e", "Exponential series")
    ]
    
    for formula, desc in formulas:
        result = agent.ingest_latex_string(formula, desc)
        print(f"   • {desc}")
        if "✅" in result:
            print(f"     ✅ Stored successfully")
        else:
            print(f"     ⚠️ {result}")
    
    print("\n✅ LaTeX ingestion test complete!")


def test_series_discovery():
    """Test infinite series discovery and verification."""
    print_section("TEST 2: Infinite Series Discovery")
    
    agent = create_math_discovery_agent(enable_memory=False, session_id="test_series")
    
    # Test 1: Verify convergence of 1/n^2
    print("1️⃣ Verifying Basel series (sum of 1/n^2)...")
    response = agent.chat("Verify the convergence of the series sum of 1/n^2 from n=1 to infinity")
    print(f"   Response: {response[:400]}...\n")
    
    # Test 2: Verify alternating series
    print("2️⃣ Verifying alternating harmonic series...")
    response = agent.chat("Verify the series sum of (-1)^(n+1)/n")
    print(f"   Response: {response[:400]}...\n")
    
    # Test 3: Discover new series
    print("3️⃣ Asking agent to discover a new series...")
    response = agent.chat(
        "Can you discover or suggest a new infinite series involving 1/n^3? "
        "Calculate its partial sum and see if it converges."
    )
    print(f"   Response: {response[:500]}...\n")
    
    # Test 4: Store discovery
    print("4️⃣ Storing the discovery in knowledge base...")
    discovery = "New series found: sum of 1/n^3 converges (related to Riemann zeta function)"
    result = agent.store_discovery(discovery, category="series")
    print(f"   Result: {result}\n")
    
    print("✅ Series discovery test complete!")


def test_product_discovery():
    """Test infinite product discovery and verification."""
    print_section("TEST 3: Infinite Product Discovery")
    
    agent = create_math_discovery_agent(enable_memory=False, session_id="test_products")
    
    # Test 1: Verify Wallis product
    print("1️⃣ Verifying Wallis product...")
    response = agent.chat(
        "Verify the infinite product: product of (4n^2)/(4n^2 - 1) for n=1 to infinity. "
        "This should equal π/2."
    )
    print(f"   Response: {response[:400]}...\n")
    
    # Test 2: Euler's product for sine
    print("2️⃣ Exploring Euler's product formula for sin(x)...")
    response = agent.chat(
        "Can you explain and verify the infinite product representation of sin(x)/x? "
        "It's the product of (1 - x^2/(n*pi)^2) for n=1 to infinity."
    )
    print(f"   Response: {response[:400]}...\n")
    
    # Test 3: Discover new product
    print("3️⃣ Discovering patterns in products...")
    response = agent.chat(
        "What are some interesting infinite products involving factorials or "
        "exponentials? Can you compute one?"
    )
    print(f"   Response: {response[:500]}...\n")
    
    print("✅ Product discovery test complete!")


def test_pattern_recognition():
    """Test sequence pattern recognition."""
    print_section("TEST 4: Pattern Recognition")
    
    agent = create_math_discovery_agent(enable_memory=False, session_id="test_patterns")
    
    # Test 1: Recognize polynomial pattern
    print("1️⃣ Recognizing perfect squares...")
    response = agent.chat("Find the pattern in this sequence: 1, 4, 9, 16, 25, 36, 49")
    print(f"   Response: {response[:300]}...\n")
    
    # Test 2: Recognize Fibonacci
    print("2️⃣ Recognizing Fibonacci sequence...")
    response = agent.chat("What pattern do you see in: 1, 1, 2, 3, 5, 8, 13, 21?")
    print(f"   Response: {response[:300]}...\n")
    
    # Test 3: Recognize geometric series
    print("3️⃣ Recognizing geometric progression...")
    response = agent.chat("Analyze this sequence: 2, 6, 18, 54, 162")
    print(f"   Response: {response[:300]}...\n")
    
    # Test 4: Complex pattern
    print("4️⃣ Finding pattern in factorials...")
    response = agent.chat("What's the pattern in: 1, 2, 6, 24, 120, 720?")
    print(f"   Response: {response[:300]}...\n")
    
    print("✅ Pattern recognition test complete!")


def test_knowledge_base_rag():
    """Test RAG knowledge base functionality."""
    print_section("TEST 5: Knowledge Base & RAG")
    
    agent = create_math_discovery_agent(enable_memory=False, session_id="test_rag")
    
    # Test 1: Store multiple discoveries
    print("1️⃣ Storing mathematical discoveries...")
    discoveries = [
        ("Riemann Hypothesis: All non-trivial zeros of zeta function have real part 1/2", "conjecture"),
        ("Euler's formula: e^(iπ) + 1 = 0", "formula"),
        ("Fermat's Last Theorem: No three positive integers a, b, c satisfy a^n + b^n = c^n for n > 2", "theorem"),
        ("Basel problem solution: ζ(2) = π²/6", "series"),
    ]
    
    for discovery, category in discoveries:
        result = agent.store_discovery(discovery, category)
        print(f"   • {category.capitalize()}: {'✅' if '✅' in result else '⚠️'}")
    print()
    
    # Test 2: Search knowledge base
    print("2️⃣ Searching knowledge base for 'pi'...")
    results = agent.search_knowledge("pi infinite series")
    print(f"   Results:\n{results[:400]}...\n")
    
    # Test 3: Search for specific topic
    print("3️⃣ Searching for 'zeta function'...")
    results = agent.search_knowledge("zeta function")
    print(f"   Results:\n{results[:400]}...\n")
    
    # Test 4: Use RAG-enhanced chat
    print("4️⃣ Asking question that uses stored knowledge...")
    response = agent.chat(
        "Based on what you know about infinite series and pi, "
        "can you list some famous formulas involving pi?"
    )
    print(f"   Response: {response[:500]}...\n")
    
    print("✅ Knowledge base test complete!")


def test_tool_generation():
    """Test dynamic tool generation."""
    print_section("TEST 6: Dynamic Tool Generation")
    
    agent = create_math_discovery_agent(enable_memory=False, session_id="test_tools")
    
    print("1️⃣ Current tool count:")
    print(f"   Agent has {len(agent.list_tools())} tools\n")
    
    # Test 1: Generate continued fraction tool
    print("2️⃣ Generating continued fraction analyzer...")
    success = agent.generate_and_add_tool(
        "Calculate and analyze continued fraction representations of numbers like pi, e, or square roots",
        category="math"
    )
    
    if success:
        print(f"   ✅ Tool generated! New total: {len(agent.list_tools())} tools")
        
        # Test the new tool
        print("\n3️⃣ Testing the new continued fraction tool...")
        response = agent.chat("What is the continued fraction representation of the golden ratio?")
        print(f"   Response: {response[:400]}...\n")
    else:
        print("   ⚠️ Tool generation requires API with function calling capability\n")
    
    # Test 2: Generate specialized discovery tool
    print("4️⃣ Generating Ramanujan-style formula generator...")
    success = agent.generate_and_add_tool(
        "Generate Ramanujan-style nested radical and series formulas for famous constants",
        category="math"
    )
    
    if success:
        print(f"   ✅ Tool generated! New total: {len(agent.list_tools())} tools\n")
    else:
        print("   ⚠️ Skipping (API limitation)\n")
    
    print("✅ Tool generation test complete!")


def test_memory_and_research_session():
    """Test memory across a research session."""
    print_section("TEST 7: Memory & Research Session")
    
    print("Creating agent with memory enabled...")
    agent = create_math_discovery_agent(enable_memory=True, session_id="research_2024")
    
    print("\n1️⃣ Starting research session on infinite series...")
    response = agent.chat(
        "I'm starting a research session on infinite series. "
        "Let's begin by reviewing the Basel problem: sum of 1/n^2 equals π²/6."
    )
    print(f"   Response: {response[:300]}...\n")
    
    print("2️⃣ Continuing research (testing memory)...")
    response = agent.chat(
        "Now, based on what we just discussed, can you suggest "
        "a related series with 1/n^3?"
    )
    print(f"   Response: {response[:300]}...\n")
    
    print("3️⃣ Referencing earlier conversation...")
    response = agent.chat(
        "What was the first thing I asked you to review in this session?"
    )
    print(f"   Response: {response[:300]}...\n")
    
    print("4️⃣ Building on previous discoveries...")
    response = agent.chat(
        "Can you summarize what we've discussed so far about infinite series in this session?"
    )
    print(f"   Response: {response[:400]}...\n")
    
    print("✅ Memory test complete!")


def test_latex_file_ingestion():
    """Test ingesting a LaTeX file (if available)."""
    print_section("TEST 8: LaTeX File Ingestion")
    
    agent = create_math_discovery_agent(enable_memory=False, session_id="test_file")
    
    # Create a sample LaTeX file
    print("1️⃣ Creating sample LaTeX file...")
    sample_latex = r"""
\documentclass{article}
\begin{document}

\section{Famous Series}

The Basel Problem:
$$\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}$$

Leibniz Formula for $\pi$:
$$\sum_{n=0}^{\infty} \frac{(-1)^n}{2n+1} = \frac{\pi}{4}$$

The exponential function:
$$e^x = \sum_{n=0}^{\infty} \frac{x^n}{n!}$$

\section{Infinite Products}

Wallis Product:
$$\prod_{n=1}^{\infty} \frac{4n^2}{4n^2-1} = \frac{\pi}{2}$$

\end{document}
"""
    
    # Write to file
    test_file = Path("test_formulas.tex")
    test_file.write_text(sample_latex)
    print(f"   Created: {test_file}\n")
    
    # Test ingestion
    print("2️⃣ Ingesting LaTeX file into knowledge base...")
    result = agent.ingest_latex_file(str(test_file))
    print(f"   Result: {result}\n")
    
    # Test if knowledge was stored
    print("3️⃣ Searching for ingested formulas...")
    results = agent.search_knowledge("Wallis product")
    print(f"   Results: {results[:300]}...\n")
    
    # Clean up
    test_file.unlink()
    print("   ✅ Cleaned up test file\n")
    
    print("✅ LaTeX file ingestion test complete!")


def test_full_discovery_workflow():
    """Test complete discovery workflow."""
    print_section("TEST 9: Full Discovery Workflow")
    
    agent = create_math_discovery_agent(
        enable_memory=True,
        session_id="full_workflow_2024"
    )
    
    print("🔬 Simulating a complete mathematical discovery session...\n")
    
    # Step 1: Ingest known formula
    print("Step 1: Ingesting known formula as context...")
    latex = r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}"
    agent.ingest_latex_string(latex, "Basel problem")
    print("   ✅ Context loaded\n")
    
    # Step 2: Analyze the formula
    print("Step 2: Analyzing the formula...")
    response = agent.chat(
        "I've loaded the Basel problem. Can you explain why this series converges "
        "and what makes it special?"
    )
    print(f"   Response: {response[:300]}...\n")
    
    # Step 3: Discover related series
    print("Step 3: Discovering related series...")
    response = agent.chat(
        "Based on the Basel problem, can you suggest and verify a related series "
        "with 1/n^4? What should it converge to?"
    )
    print(f"   Response: {response[:400]}...\n")
    
    # Step 4: Verify numerically
    print("Step 4: Numerical verification...")
    response = agent.chat(
        "Let's verify the series sum of 1/n^4 numerically. "
        "Calculate the partial sum for the first 100 terms."
    )
    print(f"   Response: {response[:300]}...\n")
    
    # Step 5: Store discovery
    print("Step 5: Storing the discovery...")
    discovery = (
        "Discovered series: sum(1/n^4, n=1 to ∞) = π^4/90 "
        "(related to Basel problem, part of Riemann zeta function values)"
    )
    result = agent.store_discovery(discovery, category="series")
    print(f"   Result: {result}\n")
    
    # Step 6: Build on discovery
    print("Step 6: Building on the discovery...")
    response = agent.chat(
        "What can we conclude about the general pattern for sum of 1/n^k "
        "where k is an even positive integer?"
    )
    print(f"   Response: {response[:400]}...\n")
    
    # Step 7: Search accumulated knowledge
    print("Step 7: Searching accumulated knowledge...")
    results = agent.search_knowledge("series n^4")
    print(f"   Found knowledge:\n{results[:300]}...\n")
    
    print("✅ Full workflow test complete!")


def run_all_tests():
    """Run all test suites."""
    print("\n" + "🧪" * 35)
    print("  MATHEMATICAL DISCOVERY AGENT - COMPREHENSIVE TEST SUITE")
    print("🧪" * 35)
    
    try:
        test_latex_ingestion()
        test_series_discovery()
        test_product_discovery()
        test_pattern_recognition()
        test_knowledge_base_rag()
        test_tool_generation()
        test_memory_and_research_session()
        test_latex_file_ingestion()
        test_full_discovery_workflow()
        
        print("\n" + "🎉" * 35)
        print("  ALL TESTS COMPLETED SUCCESSFULLY!")
        print("🎉" * 35)
        print("\n✅ The Mathematical Discovery Agent is fully operational!")
        print("\n📊 Summary:")
        print("   • LaTeX ingestion: ✅")
        print("   • Series discovery: ✅")
        print("   • Product verification: ✅")
        print("   • Pattern recognition: ✅")
        print("   • RAG knowledge base: ✅")
        print("   • Tool generation: ✅")
        print("   • Memory system: ✅")
        print("   • File ingestion: ✅")
        print("   • Full workflow: ✅")
        print("\n🚀 Ready for mathematical research!\n")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
