# Mathematical Discovery Agent

An advanced AI agent for discovering, analyzing, and cataloging new mathematical relationships including infinite series, products, patterns, and formulas.

## 🎯 Features

- **🔍 Mathematical Discovery**: Find new infinite series, products, and patterns
- **📐 Series Analysis**: Verify convergence and compute partial sums
- **📊 Pattern Recognition**: Discover patterns in number sequences
- **📝 LaTeX Support**: Ingest and parse LaTeX formulas as context
- **📚 Knowledge Base (RAG)**: Store and retrieve mathematical discoveries using Qdrant
- **🧠 Memory**: Maintain context across research sessions
- **🧰 Dynamic Toolbox**: Generate specialized tools on-the-fly
- **⚡ Commands**: Quick access to discovery functions

## 🚀 Quick Start

```python
from math_discovery_agent import create_math_discovery_agent

# Create agent
agent = create_math_discovery_agent(
    enable_memory=True,
    session_id="my_research_2024"
)

# Ingest a LaTeX formula as context
agent.ingest_latex_string(
    r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}",
    description="Basel problem"
)

# Discover related series
response = agent.chat(
    "Based on the Basel problem, can you find a similar series with 1/n^4?"
)

# Store your discovery
agent.store_discovery(
    "sum(1/n^4) = π^4/90 - related to Basel problem",
    category="series"
)
```

## 📋 Core Capabilities

### 1. Infinite Series Verification

```python
# Verify convergence and compute partial sum
response = agent.chat("Verify the series sum of 1/n^3 from n=1 to infinity")

# Direct tool usage
from math_discovery_agent import verify_infinite_series
result = verify_infinite_series.invoke({
    "expression": "1/n**3",
    "limit": 100
})
```

### 2. Infinite Product Analysis

```python
# Analyze infinite products
response = agent.chat(
    "Verify the Wallis product: product of 4n^2/(4n^2-1) for n=1 to infinity"
)

# Direct tool
from math_discovery_agent import verify_infinite_product
result = verify_infinite_product.invoke({
    "expression": "(4*n**2)/(4*n**2 - 1)",
    "limit": 100
})
```

### 3. Pattern Discovery

```python
# Discover patterns in sequences
response = agent.chat("Find the pattern in: 1, 1, 2, 3, 5, 8, 13, 21")

# Direct tool
from math_discovery_agent import discover_series_pattern
result = discover_series_pattern.invoke({
    "sequence": "1,4,9,16,25"
})
```

### 4. LaTeX Formula Ingestion

```python
# From string
agent.ingest_latex_string(
    r"\prod_{n=1}^{\infty} \left(1 - \frac{1}{(2n)^2}\right) = \frac{2}{\pi}",
    description="Wallis product formula"
)

# From file
agent.ingest_latex_file("formulas/euler_identities.tex")

# From directory
agent.load_knowledge_base("math_library/")
```

### 5. Knowledge Base Search

```python
# Search stored discoveries
results = agent.search_knowledge("infinite series involving pi", k=5)
print(results)

# Context-aware chat with RAG
response = agent.chat(
    "What infinite series formulas do we know that involve π?"
)
```

## 🛠️ Tools Reference

### Discovery Tools

- **`verify_infinite_series`**: Analyze series convergence and compute partial sums
- **`verify_infinite_product`**: Analyze product convergence and compute partial products
- **`discover_series_pattern`**: Find patterns in number sequences
- **`parse_latex_formula`**: Parse and extract components from LaTeX formulas

### Built-in Math Tools

- Calculator, quadratic solver, matrix operations
- Plus all tools from `get_math_tools()`

### Commands

- `/discover <sequence>`: Quick pattern discovery
- `/verify_series <expression>`: Quick series verification
- `/parse_latex <latex>`: Quick LaTeX parsing
- Plus all standard math commands

## 📚 Complete Examples

### Example 1: Discovering New Series

```python
# Start a research session
agent = create_math_discovery_agent(
    enable_memory=True,
    session_id="series_research"
)

# Ingest known formula
agent.ingest_latex_string(
    r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}",
    "Basel problem - Euler 1735"
)

# Ask agent to explore
response = agent.chat("""
Based on the Basel problem where sum of 1/n² equals π²/6,
can you:
1. Suggest a related series with 1/n⁴
2. Compute its partial sum
3. Try to determine its closed form
""")

# Verify the discovery
response = agent.chat("Let's verify sum of 1/n^4 numerically with 100 terms")

# Store the result
agent.store_discovery(
    "Series: Σ(1/n⁴) = π⁴/90 (Riemann ζ(4))",
    category="series"
)
```

### Example 2: Pattern Investigation

```python
# Given a sequence, discover its formula
sequence = "3, 7, 11, 15, 19, 23, 27"
response = agent.chat(f"What's the pattern in: {sequence}")

# Generate more terms
response = agent.chat("Using that pattern, what are the next 5 terms?")

# Find closed form
response = agent.chat("Give me a formula for the n-th term")
```

### Example 3: LaTeX Research Database

```python
# Build a research database from LaTeX files
agent = create_math_discovery_agent(session_id="research_db")

# Ingest multiple sources
agent.load_knowledge_base("papers/ramanujan/")
agent.ingest_latex_file("notes/infinite_products.tex")
agent.ingest_latex_file("textbooks/series_analysis.tex")

# Now search across all sources
results = agent.search_knowledge("nested radicals ramanujan")

# Ask questions that use the knowledge
response = agent.chat("""
Based on the formulas in my knowledge base, are there any
infinite series or products that involve both π and e?
""")
```

### Example 4: Discovering Wallis Product

```python
# Start fresh
agent = create_math_discovery_agent(enable_memory=False)

# Give a hint
response = agent.chat("""
Consider the infinite product of (4n²)/(4n² - 1) for n = 1 to ∞.
Can you:
1. Compute the first 10 terms
2. Compute the partial product
3. What famous constant does it approach?
""")

# Verify with tool
result = verify_infinite_product.invoke({
    "expression": "(4*n**2)/(4*n**2 - 1)",
    "limit": 50
})

# Store discovery
agent.store_discovery(
    "Wallis Product: Π(4n²/(4n²-1)) = π/2",
    category="product"
)
```

## 🔬 Research Workflow

### Typical Discovery Session

```python
# 1. Create agent with memory
agent = create_math_discovery_agent(
    enable_memory=True,
    session_id="discovery_session_20241125"
)

# 2. Ingest context (known formulas)
agent.ingest_latex_string(
    r"\sum_{n=0}^{\infty} \frac{x^n}{n!} = e^x",
    "Exponential series expansion"
)

# 3. Explore and discover
agent.chat("Based on the exponential series, what about sin(x)?")

# 4. Verify discoveries
agent.chat("Can you verify the sin(x) series numerically at x=π/4?")

# 5. Store findings
agent.store_discovery(
    "sin(x) = Σ((-1)^n * x^(2n+1)/(2n+1)!)",
    category="series"
)

# 6. Search accumulated knowledge
agent.search_knowledge("trigonometric series")

# 7. Continue building on discoveries
agent.chat("What about cos(x) series? Can we derive it from sin(x)?")
```

## 🎓 Advanced Features

### Dynamic Tool Generation

```python
# Generate specialized tools on-the-fly
agent.generate_and_add_tool(
    "Calculate continued fraction representations of algebraic and transcendental numbers",
    category="math"
)

# Use the new tool
response = agent.chat("What's the continued fraction of the golden ratio?")
```

### Memory-Enhanced Research

```python
# Agent remembers entire research session
agent.chat("I'm investigating series related to π")
agent.chat("Let's start with the Basel problem")
agent.chat("Now what about 1/n^3?")
agent.chat("What was my original research topic?")  # Remembers: series related to π
```

### Multi-File LaTeX Ingestion

```python
# Ingest entire research directories
agent.load_knowledge_base("research_papers/")

# Agent now has access to all formulas from those papers
agent.chat("Summarize all the infinite products we have in the knowledge base")
```

## 📊 Example Output

### Series Verification

```
Series: Σ(1/n**2) for n=1 to ∞
Partial sum (n=100): 1.6349839002
Closed form: pi**2/6
Exact value: 1.6449340668
```

### Pattern Discovery

```
Discovered patterns:
Polynomial (degree 2): a(n) = n**2
```

### LaTeX Parsing

```
Original LaTeX: \sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}

Parsed components:
• Type: Infinite series or summation
• Lower bound: n=1
• Upper bound: \infty
• Left side: \sum_{n=1}^{\infty} \frac{1}{n^2}
• Right side: \frac{\pi^2}{6}
• Fractions found: 2
```

## 🧪 Testing

Run the test suite:

```bash
# Quick test (no Qdrant required)
python tests/test_discovery_quick.py

# Comprehensive test (requires Qdrant)
python tests/test_math_discovery_agent.py
```

## 📝 Notes

- **Memory**: Requires functional memory system (can be disabled for quick tests)
- **RAG**: Requires Qdrant running for full knowledge base features
- **API**: Requires GROQ_API_KEY for LLM functionality
- **Tool Generation**: Requires API with function calling for dynamic tools

## 🎯 Use Cases

1. **Mathematical Research**: Discover new formulas and relationships
2. **Series Analysis**: Verify convergence of infinite series
3. **Pattern Recognition**: Find formulas from sequences
4. **Knowledge Management**: Build a searchable math formula database
5. **Education**: Explore mathematical concepts interactively
6. **Paper Analysis**: Extract and catalog formulas from LaTeX papers

## 🤝 Integration

Can be combined with:
- Standard math agent for general calculations
- Toolbox system for persistent tool storage
- Memory system for long-term research sessions
- RAG for large mathematical knowledge bases

## 📄 License

Apache 2.0 - Part of LangChain Agent Base framework
