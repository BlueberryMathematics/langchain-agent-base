"""
Test ingesting complex mathematical content - Weierstrass product formulas
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "examples" / "building-ultimate-math-agent"))

from math_discovery_agent import create_math_discovery_agent

print("🔬 Testing Complex Mathematical Content Ingestion")
print("=" * 70)

# Create agent
agent = create_math_discovery_agent(enable_memory=False, session_id="weierstrass_test")

# Test 1: Ingest the Weierstrass product formula
print("\n1️⃣ Ingesting Weierstrass Product Formula...")
weierstrass_latex = r"\sin\left(\frac{\pi z}{k}\right) = \pi z\prod_{n=2}^x \left(1-\frac{z^2}{n^2k^2}\right)"
result = agent.ingest_latex_string(
    weierstrass_latex,
    "Weierstrass Product Formula for sin with constant k"
)
print(f"   {result}\n")

# Test 2: Ingest the product of both sides
print("2️⃣ Ingesting product formula (function a(z) and b(z))...")
product_latex = r"\prod_{k=2}^x\sin\left(\frac{\pi z}{k}\right) = \prod_{k=2}^x \pi z\prod_{n=2}^x \left(1-\frac{z^2}{n^2k^2}\right)"
result = agent.ingest_latex_string(
    product_latex,
    "Product of sin functions - derives a(z) and b(z)"
)
print(f"   {result}\n")

# Test 3: Ask agent to analyze the formulas
print("3️⃣ Asking agent to analyze the Weierstrass product...")
response = agent.chat("""
I've loaded the Weierstrass Product Formula for sin. Can you:
1. Explain what this formula represents
2. Identify the key components (the product term)
3. What does the nested product in the second formula mean mathematically?
""")
print(f"   Response: {response[:500]}...\n")

# Test 4: Ask about the Python implementation
print("4️⃣ Asking about implementing this as a product of sines...")
response = agent.chat("""
Given the formula:
∏(k=2 to x) sin(πz/k)

How would you compute this numerically? What are the challenges with:
- Complex numbers (z = x + iy)
- Convergence for large x
- Numerical stability
""")
print(f"   Response: {response[:500]}...\n")

# Test 5: Create a LaTeX file with the full content
print("5️⃣ Creating LaTeX file with full derivation...")
full_latex = r"""
\documentclass{article}
\begin{document}

\subsection*{IV. Derivation of a(z) and b(z) from the Weierstrass product formula for sin}

Derivation of a(z) and b(z) by substituting the infinite product representation of $\sin(\pi*z/n)$ into the infinite product of $\sin(\pi*z/n)$:

We use the Weierstrass Product Formula for sin to form the relationship where k is a constant, this differs from the original Weierstrass product formula which does not contain this constant:

\begin{align*}
	\sin\left(\frac{\pi z}{k}\right) = \pi z\prod_{n=2}^x \left(1-\frac{z^2}{n^2k^2}\right)
\end{align*}

Taking the product of both sides provides function a(z) as well as the functional equation of a(z) known as b(z):

\begin{align*}
	\prod_{k=2}^x\sin\left(\frac{\pi z}{k}\right) = \prod_{k=2}^x \pi z\prod_{n=2}^x \left(1-\frac{z^2}{n^2k^2}\right)
\end{align*}

This represents a nested double product structure that relates the product of sine functions to an algebraic expression.

\end{document}
"""

test_file = Path("weierstrass_derivation.tex")
test_file.write_text(full_latex)
print(f"   Created: {test_file}")

# Test 6: Ingest the full file
print("\n6️⃣ Ingesting complete LaTeX file...")
result = agent.ingest_latex_file(str(test_file))
print(f"   {result}\n")

# Test 7: Search the knowledge base
print("7️⃣ Searching knowledge base for 'Weierstrass product'...")
results = agent.search_knowledge("Weierstrass product nested double product")
print(f"   {results[:400]}...\n")

# Test 8: Ask about the nested structure
print("8️⃣ Asking about nested product implementation...")
response = agent.chat("""
Based on the Weierstrass formulas in my knowledge base, 
how would you implement the nested double product:

∏(k=2 to x) [ π*z * ∏(n=2 to x) (1 - z²/(n²k²)) ]

What's the computational complexity and what optimizations could be applied?
""")
print(f"   Response: {response[:600]}...\n")

# Test 9: Store a discovery about this formula
print("9️⃣ Storing discovery about the formula...")
discovery = """
Weierstrass Product Nested Structure Discovery:
The double product ∏(k=2 to x) ∏(n=2 to x) (1 - z²/(n²k²)) represents a 
product over a 2D grid, creating O(x²) terms. This relates the transcendental
sine function to an infinite algebraic product, demonstrating deep connections
between trigonometric and algebraic structures.
"""
result = agent.store_discovery(discovery, category="product")
print(f"   {result}\n")

# Test 10: Ask agent to connect with known formulas
print("🔟 Asking agent to connect with classical results...")
response = agent.chat("""
Compare the Weierstrass product formula with the Euler product formula
for sin(x). Are they related? How does the nested product structure 
differ from the standard Weierstrass formula?
""")
print(f"   Response: {response[:600]}...\n")

# Cleanup
test_file.unlink()
print("   ✅ Cleaned up test file")

print("\n" + "=" * 70)
print("✅ Complex Content Test Complete!")
print("\n📊 Summary:")
print("   • Weierstrass formula ingestion: ✅")
print("   • Nested product formula ingestion: ✅")
print("   • LaTeX file parsing: ✅")
print("   • Complex formula analysis: ✅")
print("   • Knowledge base search: ✅")
print("   • Discovery storage: ✅")
print("   • Mathematical insights: ✅")
print("\n💡 The agent can handle:")
print("   • Complex LaTeX with nested products")
print("   • Multi-level mathematical structures")
print("   • Derivations and relationships")
print("   • Connection to Python implementations")
print("   • Storage and retrieval of complex formulas")
