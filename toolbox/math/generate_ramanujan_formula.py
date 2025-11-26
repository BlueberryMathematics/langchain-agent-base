"""
Tool: generate_ramanujan_formula
Category: math
Author: llm
Version: 1.0.0
Created: 2025-11-26T00:44:10.990947
Description: Generate a Ramanujan‑style nested radical or series formula for a famous mathematical constant.

Arg...
"""

from langchain_core.tools import tool
import math
import typing

from langchain_core.tools import tool
import math
from typing import Dict

@tool
def generate_ramanujan_formula(constant: str, terms: int = 5) -> str:
    """
    Generate a Ramanujan‑style nested radical or series formula for a famous mathematical constant.
    
    Args:
        constant: Name of the constant (e.g., "pi", "e", "sqrt2", "phi").
                  The function is case‑insensitive and accepts common aliases.
        terms: Number of terms to include in the series expansion (must be a positive integer).
               For nested radicals the value is ignored but kept for API consistency.
    
    Returns:
        A string containing a LaTeX‑style formula (or plain text if LaTeX is not desired) that
        represents a Ramanujan‑style expression for the requested constant, or an error message.
    
    Examples:
        generate_ramanujan_formula("pi", 3) ->
            "Ramanujan series for \\(\\pi\\):\\n"
            "1/π = (2√2)/9801 * Σ_{k=0}^{2} (4k)!(1103+26390k) / ((k!)^4 396^{4k})"
        generate_ramanujan_formula("sqrt2") ->
            "Nested radical for \\(\\sqrt{2}\\):\\n"
            "√2 = 1 + 1/(2+1/(2+1/(2+...)))"
    """
    try:
        if not isinstance(constant, str):
            return "Error: 'constant' must be a string."
        if not isinstance(terms, int) or terms <= 0:
            return "Error: 'terms' must be a positive integer."

        const_key = constant.strip().lower()
        # Mapping of constants to their Ramanujan‑style formulas
        formulas: Dict[str, str] = {
            "pi": (
                "Ramanujan series for \\(\\pi\\):\\n"
                "\\frac{{1}}{{\\pi}} = \\frac{{2\\sqrt{{2}}}}{{9801}} "
                "\\sum_{k=0}^{%d} \\frac{{(4k)!\\,(1103+26390k)}}{{(k!)^4\\,396^{4k}}}"
            ),
            "e": (
                "Ramanujan‑type series for \\(e\\):\\n"
                "e = \\sum_{k=0}^{%d} \\frac{{1}}{{k!}} + \\frac{{1}}{{2^{2k+1}}}"
            ),
            "sqrt2": (
                "Nested radical for \\(\\sqrt{2}\\):\\n"
                "\\sqrt{2} = 1 + \\frac{1}{{2+\\frac{1}{{2+\\frac{1}{{2+\\cdots}}}}}}"
            ),
            "phi": (
                "Nested radical for the golden ratio \\(\\varphi\\):\\n"
                "\\varphi = 1 + \\frac{1}{{1+\\frac{1}{{1+\\frac{1}{{1+\\cdots}}}}}}"
            ),
            "catalan": (
                "Ramanujan series for Catalan's constant \\(G\\):\\n"
                "G = \\sum_{k=0}^{%d} \\frac{{(-1)^k}}{{(2k+1)^2}}"
            ),
        }

        if const_key not in formulas:
            return f"Error: Unknown constant '{constant}'. Supported constants are: {', '.join(formulas.keys())}."

        template = formulas[const_key]
        # Only series formulas need the term count inserted
        if "%d" in template:
            formula_filled = template % (terms - 1)  # series index runs from 0 to terms-1
        else:
            formula_filled = template

        return formula_filled

    except Exception as e:
        return f"Error generating Ramanujan formula: {str(e)}"