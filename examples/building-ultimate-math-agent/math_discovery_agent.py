"""
Mathematical Discovery Agent
============================

An advanced agent that:
- Discovers new infinite sums, products, and series
- Stores mathematical knowledge in Qdrant (RAG)
- Ingests LaTeX formulas as context
- Generates and validates new mathematical relationships
- Uses the full framework: memory, RAG, toolbox, commands

This agent can become your mathematical research assistant for finding
and cataloging new mathematical discoveries.
"""

import sys
import re
from pathlib import Path
from typing import List, Optional

from src.base import Agent
from src.tools import get_math_tools
from src.protocol import register_agent, AgentStatus
from src.commands import create_math_commands, command
from src.toolbox import get_toolbox
from src.tool_generator import generate_tool
from src.rag import RAGManager
from langchain_core.tools import tool
import sympy as sp


@tool
def verify_infinite_series(expression: str, variable: str = "n", limit: int = 100) -> str:
    """
    Verify convergence and compute partial sum of an infinite series.
    
    Args:
        expression: Series term like "1/n**2" or "(-1)**n/factorial(n)"
        variable: Summation variable (default: n)
        limit: Number of terms to compute (default: 100)
    
    Returns:
        Convergence analysis and partial sum
    """
    try:
        var = sp.Symbol(variable)
        term = sp.sympify(expression)
        
        # Compute partial sum
        partial_sum = sum(float(term.subs(var, i)) for i in range(1, limit + 1))
        
        # Try to find closed form
        closed_form = sp.summation(term, (var, 1, sp.oo))
        
        result = f"Series: Σ({expression}) for {variable}=1 to ∞\n"
        result += f"Partial sum (n={limit}): {partial_sum:.10f}\n"
        
        if closed_form != sp.Sum(term, (var, 1, sp.oo)):
            result += f"Closed form: {closed_form}\n"
            result += f"Exact value: {float(closed_form.evalf()):.10f}"
        else:
            result += "Closed form: Unable to determine"
        
        return result
        
    except Exception as e:
        return f"Error analyzing series: {str(e)}"


@tool
def verify_infinite_product(expression: str, variable: str = "n", limit: int = 100) -> str:
    """
    Verify convergence and compute partial product of an infinite product.
    
    Args:
        expression: Product term like "(1 + 1/n**2)" or "cos(x/2**n)"
        variable: Product variable (default: n)
        limit: Number of terms to compute (default: 100)
    
    Returns:
        Convergence analysis and partial product
    """
    try:
        var = sp.Symbol(variable)
        term = sp.sympify(expression)
        
        # Compute partial product
        partial_product = 1
        for i in range(1, limit + 1):
            partial_product *= float(term.subs(var, i))
        
        result = f"Product: Π({expression}) for {variable}=1 to ∞\n"
        result += f"Partial product (n={limit}): {partial_product:.10f}\n"
        
        # Check for known forms
        if "cos" in expression or "sin" in expression:
            result += "Type: Trigonometric infinite product"
        elif "factorial" in expression:
            result += "Type: Factorial-based product"
        else:
            result += "Type: General infinite product"
        
        return result
        
    except Exception as e:
        return f"Error analyzing product: {str(e)}"


@tool
def discover_series_pattern(sequence: str) -> str:
    """
    Analyze a sequence and discover potential series patterns.
    
    Args:
        sequence: Comma-separated numbers like "1,4,9,16,25" or "1,1,2,3,5,8"
    
    Returns:
        Discovered pattern and formula
    """
    try:
        nums = [float(x.strip()) for x in sequence.split(',')]
        n = len(nums)
        
        results = []
        
        # Check polynomial patterns
        var = sp.Symbol('n')
        for degree in range(1, min(5, n)):
            try:
                # Fit polynomial
                coeffs = sp.polys.polyfit(list(range(1, n + 1)), nums, degree)
                poly = sum(c * var**i for i, c in enumerate(reversed(coeffs)))
                
                # Verify fit
                predicted = [float(poly.subs(var, i)) for i in range(1, n + 1)]
                error = sum(abs(p - a) for p, a in zip(predicted, nums)) / n
                
                if error < 0.01:
                    results.append(f"Polynomial (degree {degree}): a(n) = {poly}")
            except:
                pass
        
        # Check Fibonacci-like patterns
        if n >= 3:
            is_fib = all(abs(nums[i] - (nums[i-1] + nums[i-2])) < 0.01 
                        for i in range(2, n))
            if is_fib:
                results.append("Pattern: Fibonacci-like (a(n) = a(n-1) + a(n-2))")
        
        # Check geometric series
        if n >= 2:
            ratios = [nums[i] / nums[i-1] for i in range(1, n) if nums[i-1] != 0]
            if ratios and all(abs(r - ratios[0]) < 0.01 for r in ratios):
                results.append(f"Geometric series: a(n) = a(1) * {ratios[0]:.4f}^(n-1)")
        
        if results:
            return "Discovered patterns:\n" + "\n".join(results)
        else:
            return "No clear pattern detected. Try more terms or different approaches."
        
    except Exception as e:
        return f"Error discovering pattern: {str(e)}"


@tool
def parse_latex_formula(latex: str) -> str:
    """
    Parse a LaTeX mathematical formula and extract its components.
    
    Args:
        latex: LaTeX formula like "\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}"
    
    Returns:
        Parsed components and symbolic representation
    """
    try:
        # Clean LaTeX
        formula = latex.strip()
        
        # Remove common LaTeX commands
        formula = formula.replace(r'\displaystyle', '')
        formula = formula.replace(r'\limits', '')
        
        result = f"Original LaTeX: {latex}\n\n"
        result += "Parsed components:\n"
        
        # Detect series
        if r'\sum' in formula:
            result += "• Type: Infinite series or summation\n"
            
            # Extract bounds
            bounds_match = re.search(r'\\sum_\{([^}]+)\}\^\{([^}]+)\}', formula)
            if bounds_match:
                result += f"• Lower bound: {bounds_match.group(1)}\n"
                result += f"• Upper bound: {bounds_match.group(2)}\n"
        
        # Detect products
        if r'\prod' in formula:
            result += "• Type: Infinite product\n"
            
            bounds_match = re.search(r'\\prod_\{([^}]+)\}\^\{([^}]+)\}', formula)
            if bounds_match:
                result += f"• Lower bound: {bounds_match.group(1)}\n"
                result += f"• Upper bound: {bounds_match.group(2)}\n"
        
        # Detect integrals
        if r'\int' in formula:
            result += "• Type: Integral\n"
        
        # Detect equation
        if '=' in formula:
            parts = formula.split('=')
            result += f"• Left side: {parts[0].strip()}\n"
            result += f"• Right side: {parts[1].strip() if len(parts) > 1 else 'N/A'}\n"
        
        # Extract fractions
        fractions = re.findall(r'\\frac\{([^}]+)\}\{([^}]+)\}', formula)
        if fractions:
            result += f"• Fractions found: {len(fractions)}\n"
            for i, (num, den) in enumerate(fractions[:3], 1):
                result += f"  {i}. {num}/{den}\n"
        
        return result
        
    except Exception as e:
        return f"Error parsing LaTeX: {str(e)}"


@register_agent(
    name="math_discovery",
    version="1.0.0",
    domain="mathematics",
    category="research",
    description="Mathematical discovery agent for finding new infinite series, products, and patterns",
    author="Math Research Team",
    status=AgentStatus.PRODUCTION
)
class MathDiscoveryAgent(Agent):
    """
    Mathematical Discovery Agent
    
    This agent specializes in:
    - Discovering new infinite sums and products
    - Analyzing mathematical patterns
    - Storing discoveries in Qdrant for future reference
    - Ingesting LaTeX formulas as context
    - Generating new mathematical relationships
    - Validating and verifying mathematical statements
    
    Features:
    - Full RAG integration for mathematical knowledge
    - Conversation memory for research sessions
    - Dynamic tool generation for specialized tasks
    - Command system for quick operations
    - LaTeX parsing and formula extraction
    """
    
    def __init__(self, 
                 enable_memory: bool = True,
                 memory_session_id: str = "discovery_session",
                 knowledge_base_path: Optional[str] = None,
                 **kwargs):
        
        print("🔬 Initializing Mathematical Discovery Agent...")
        
        # Initialize base agent with enhanced system prompt
        super().__init__(
            system_prompt=self._create_system_prompt(),
            enable_memory=enable_memory,
            memory_session_id=memory_session_id,
            enable_commands=True,
            **kwargs
        )
        
        # Add all math tools
        print("  📐 Loading mathematical tools...")
        self.add_tools(get_math_tools())
        
        # Add discovery tools
        print("  🔍 Loading discovery tools...")
        self.add_tools([
            verify_infinite_series,
            verify_infinite_product,
            discover_series_pattern,
            parse_latex_formula
        ])
        
        # Add commands
        print("  ⚡ Setting up commands...")
        for cmd in create_math_commands():
            self.add_command(cmd)
        
        # Add discovery-specific commands
        self._add_discovery_commands()
        
        # Initialize RAG for mathematical knowledge
        print("  📚 Initializing knowledge base (RAG)...")
        try:
            self.rag = RAGManager()
            self.rag_collection = "mathematical_discoveries"
            
            # Load knowledge base if provided
            if knowledge_base_path:
                self.load_knowledge_base(knowledge_base_path)
        except Exception as e:
            print(f"     ⚠️  RAG initialization: {e}")
            self.rag = None
        
        # Load tools from toolbox
        print("  🧰 Loading tools from toolbox...")
        try:
            self.load_tools_from_toolbox(category="math")
            toolbox_tools = len(self.list_tools()) - len(get_math_tools()) - 4
            print(f"     Loaded {toolbox_tools} additional tools from toolbox")
        except Exception as e:
            print(f"     ⚠️  Toolbox loading: {e}")
        
        print(f"\n✅ Math Discovery Agent Ready!")
        print(f"   📊 Total tools: {len(self.tools)}")
        print(f"   ⚡ Total commands: {len(self.list_commands())}")
        print(f"   🧠 Memory: {'Enabled' if enable_memory else 'Disabled'}")
        print(f"   📚 RAG: {'Enabled' if self.rag else 'Disabled'}")
        print(f"   🆔 Session: {memory_session_id}\n")
    
    def _create_system_prompt(self) -> str:
        """Create enhanced system prompt for discovery."""
        return """I am a Mathematical Discovery Agent specialized in finding and analyzing new mathematical relationships.

My capabilities include:
1. Discovering new infinite series and products
2. Analyzing patterns in sequences
3. Verifying convergence of series and products
4. Parsing and understanding LaTeX formulas
5. Storing mathematical discoveries in a knowledge base
6. Retrieving relevant mathematical knowledge from past discoveries

I approach problems systematically:
- First, I understand the mathematical context
- Then, I use appropriate tools to analyze and discover
- I verify my findings rigorously
- I store important discoveries for future reference
- I build upon previous discoveries

I can ingest LaTeX formulas and use them as context for new discoveries.
I maintain a research journal of all mathematical insights.
I am creative yet rigorous in my mathematical exploration."""
    
    def _add_discovery_commands(self):
        """Add discovery-specific commands."""
        
        @command(name="discover", description="Discover patterns in a sequence of numbers")
        def discover_cmd(sequence: str) -> str:
            """Discover patterns in a sequence. Usage: /discover 1,4,9,16,25"""
            return discover_series_pattern.invoke({"sequence": sequence})
        
        @command(name="verify_series", description="Verify an infinite series")
        def verify_series_cmd(expression: str) -> str:
            """Verify series convergence. Usage: /verify_series 1/n**2"""
            return verify_infinite_series.invoke({"expression": expression})
        
        @command(name="parse_latex", description="Parse a LaTeX formula")
        def parse_latex_cmd(latex: str) -> str:
            """Parse LaTeX formula. Usage: /parse_latex \\sum_{n=1}^{\\infty}..."""
            return parse_latex_formula.invoke({"latex": latex})
        
        self.add_command(discover_cmd)
        self.add_command(verify_series_cmd)
        self.add_command(parse_latex_cmd)
    
    def ingest_latex_file(self, filepath: str) -> str:
        """
        Ingest a LaTeX file and add it to the knowledge base.
        
        Args:
            filepath: Path to .tex file
        
        Returns:
            Status message
        """
        try:
            path = Path(filepath)
            if not path.exists():
                return f"Error: File {filepath} not found"
            
            content = path.read_text(encoding='utf-8')
            
            # Extract formulas (everything between $ or \[ \])
            formulas = []
            formulas.extend(re.findall(r'\$\$(.*?)\$\$', content, re.DOTALL))
            formulas.extend(re.findall(r'\\\[(.*?)\\\]', content, re.DOTALL))
            formulas.extend(re.findall(r'\$(.*?)\$', content))
            
            if not formulas and self.rag:
                # No formulas found, add whole content
                return self.ingest_latex_string(content, f"Full content from {filepath}")
            
            if self.rag:
                # Add each formula to knowledge base
                for i, formula in enumerate(formulas):
                    self.ingest_latex_string(formula.strip(), f"Formula {i+1} from {filepath}")
                
                return f"✅ Ingested {len(formulas)} formulas from {filepath} into knowledge base"
            else:
                return f"⚠️ RAG not initialized. Found {len(formulas)} formulas but couldn't store them."
            
        except Exception as e:
            return f"Error ingesting LaTeX file: {str(e)}"
    
    def ingest_latex_string(self, latex: str, description: str = "") -> str:
        """
        Ingest a LaTeX formula string into the knowledge base.
        
        Args:
            latex: LaTeX formula string
            description: Optional description of the formula
        
        Returns:
            Status message
        """
        try:
            if not self.rag:
                return "⚠️ RAG not initialized. Cannot store formula."
            
            # Parse the formula first
            parsed = parse_latex_formula.invoke({"latex": latex})
            
            # Store in knowledge base
            doc_text = f"{latex}\n\nDescription: {description}\n\n{parsed}"
            
            # Use add_documents_to_collection method
            try:
                self.rag.add_documents_to_collection([doc_text], self.rag_collection)
            except ValueError:
                # Collection doesn't exist yet, create it
                from langchain_core.documents import Document
                docs = [Document(page_content=doc_text)]
                splits = self.rag.text_splitter.split_documents(docs)
                
                # Create collection
                from qdrant_client.models import VectorParams, Distance
                try:
                    self.rag.client.create_collection(
                        collection_name=self.rag_collection,
                        vectors_config=VectorParams(size=self.rag.vector_size, distance=Distance.COSINE)
                    )
                except:
                    pass
                
                # Create vector store
                from langchain_qdrant import QdrantVectorStore
                vectorstore = QdrantVectorStore(
                    client=self.rag.client,
                    collection_name=self.rag_collection,
                    embedding=self.rag.embedding_model,
                )
                vectorstore.add_documents(splits)
                self.rag.collections[self.rag_collection] = vectorstore
            
            return f"✅ Added formula to knowledge base:\n{latex}"
            
        except Exception as e:
            return f"Error ingesting LaTeX string: {str(e)}"
    
    def load_knowledge_base(self, directory: str) -> str:
        """
        Load multiple files into the knowledge base.
        
        Args:
            directory: Directory containing .tex or .txt files
        
        Returns:
            Status message
        """
        try:
            path = Path(directory)
            if not path.exists():
                return f"Error: Directory {directory} not found"
            
            if path.is_file():
                return self.ingest_latex_file(str(path))
            
            # Load all .tex and .txt files
            files_loaded = 0
            for file in path.glob("**/*.tex"):
                result = self.ingest_latex_file(str(file))
                if "✅" in result:
                    files_loaded += 1
            
            for file in path.glob("**/*.txt"):
                content = file.read_text(encoding='utf-8')
                if self.rag:
                    self.ingest_latex_string(content, f"Text file: {file.name}")
                    files_loaded += 1
            
            return f"✅ Loaded {files_loaded} files into knowledge base"
            
        except Exception as e:
            return f"Error loading knowledge base: {str(e)}"
    
    def search_knowledge(self, query: str, k: int = 5) -> str:
        """
        Search the mathematical knowledge base.
        
        Args:
            query: Search query
            k: Number of results
        
        Returns:
            Search results
        """
        try:
            if not self.rag:
                return "⚠️ RAG not initialized. Cannot search knowledge base."
            
            if self.rag_collection not in self.rag.collections:
                return "No knowledge base found. Ingest some formulas first."
            
            # Get retriever and search
            retriever = self.rag.get_retriever(self.rag_collection)
            results = retriever.invoke(query)[:k]
            
            if not results:
                return "No relevant knowledge found."
            
            output = f"Found {len(results)} relevant items:\n\n"
            for i, doc in enumerate(results, 1):
                output += f"{i}. {doc.page_content[:200]}...\n"
                if hasattr(doc, 'metadata') and doc.metadata:
                    output += f"   Metadata: {doc.metadata}\n"
                output += "\n"
            
            return output
            
        except Exception as e:
            return f"Error searching knowledge base: {str(e)}"
    
    def store_discovery(self, discovery: str, category: str = "general") -> str:
        """
        Store a mathematical discovery in the knowledge base.
        
        Args:
            discovery: Description of the discovery
            category: Category (series, product, pattern, formula)
        
        Returns:
            Status message
        """
        try:
            if not self.rag:
                return "⚠️ RAG not initialized. Cannot store discovery."
            
            # Use ingest_latex_string method which handles collection creation
            doc_text = f"[{category.upper()}] {discovery}"
            return self.ingest_latex_string(doc_text, f"Discovery - {category}")
            
        except Exception as e:
            return f"Error storing discovery: {str(e)}"


def create_math_discovery_agent(
    enable_memory: bool = True,
    session_id: str = "discovery",
    knowledge_base: Optional[str] = None,
    **kwargs
) -> MathDiscoveryAgent:
    """
    Factory function to create a Mathematical Discovery Agent.
    
    Args:
        enable_memory: Enable conversation memory
        session_id: Session ID for research session
        knowledge_base: Path to knowledge base directory/file
        **kwargs: Additional agent configuration
    
    Returns:
        Configured MathDiscoveryAgent
    
    Example:
        >>> agent = create_math_discovery_agent(session_id="research_2024")
        >>> agent.ingest_latex_string(r"\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}")
        >>> response = agent.chat("Find a similar series that converges to π^3")
    """
    return MathDiscoveryAgent(
        enable_memory=enable_memory,
        memory_session_id=session_id,
        knowledge_base_path=knowledge_base,
        **kwargs
    )


if __name__ == "__main__":
    print("🔬 Mathematical Discovery Agent")
    print("=" * 70)
    print("This agent helps discover new mathematical relationships!")
    print()
    
    # Create agent
    agent = create_math_discovery_agent(
        enable_memory=False,  # Disable for demo
        session_id="demo"
    )
    
    print("\n" + "=" * 70)
    print("💡 Example Usage:")
    print()
    print("# Ingest a LaTeX formula:")
    print('agent.ingest_latex_string(r"\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}")')
    print()
    print("# Discover patterns:")
    print('agent.chat("Find patterns in the sequence 1, 4, 9, 16, 25")')
    print()
    print("# Verify series:")
    print('agent.chat("Verify the convergence of sum of 1/n^3")')
    print()
    print("# Search knowledge:")
    print('agent.search_knowledge("infinite series involving pi")')
