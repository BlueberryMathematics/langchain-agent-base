"""
Tool: generate_ramanujan_formulas
Category: math
Author: llm
Version: 1.0.0
Created: 2025-11-26T00:50:41.603465
Description: Generate Ramanujan‑style nested radical and series formulas for a given famous mathematical constant...
"""

from langchain_core.tools import tool
import typing

from langchain_core.tools import tool
from typing import Dict, List


@tool
def generate_ramanujan_formulas(constant: str) -> str:
    """
    Generate Ramanujan‑style nested radical and series formulas for a given famous mathematical constant.

    Args:
        constant: Name of the constant for which to retrieve formulas. Supported values (case‑insensitive):
            - "pi"
            - "e"
            - "sqrt2"
            - "phi" (golden ratio)
            - "apery" (Apéry's constant ζ(3))

    Returns:
        A formatted string containing one or more Ramanujan‑style formulas for the requested constant.
        If the constant is not recognized, an error message is returned.

    Examples:
        generate_ramanujan_formulas("pi") ->
        "Ramanujan nested radical for π:\\n"
        "    \\(\\frac{1}{\\pi}=\\frac{2\\sqrt{2}}{9801}\\sum_{k=0}^{\\infty}\\frac{(4k)!(1103+26390k)}{(k!)^4 396^{4k}}\\)\\n"
        "Ramanujan series for π:\\n"
        "    \\(\\frac{1}{\\pi}=\\frac{2\\sqrt{2}}{9801}\\sum_{k=0}^{\\infty}\\frac{(4k)!(1103+26390k)}{(k!)^4 396^{4k}}\\)"
    """
    try:
        # Normalise the constant name
        key = constant.strip().lower()

        formulas: Dict[str, List[str]] = {
            "pi": [
                "Ramanujan series for \\(\\pi\\):\\n"
                "    \\(\\frac{1}{\\pi}=\\frac{2\\sqrt{2}}{9801}"
                "\\sum_{k=0}^{\\infty}\\frac{(4k)!(1103+26390k)}{(k!)^4 396^{4k}}\\)",
                "Ramanujan nested radical for \\(\\pi\\):\\n"
                "    \\(\\pi = \\frac{2}{\\sqrt{2+\\sqrt{2+\\sqrt{2+\\cdots}}}}\\)"
            ],
            "e": [
                "Ramanujan‑type series for \\(e\\):\\n"
                "    \\(e = \\sum_{n=0}^{\\infty}\\frac{1}{n!}\\)",
                "Ramanujan nested radical for \\(e\\):\\n"
                "    \\(e = 2+\\frac{1}{1+\\frac{1}{2+\\frac{1}{3+\\frac{1}{4+\\cdots}}}}\\)"
            ],
            "sqrt2": [
                "Ramanujan nested radical for \\(\\sqrt{2}\\):\\n"
                "    \\(\\sqrt{2}=\\sqrt{2+\\sqrt{2+\\sqrt{2+\\cdots}}}\\)",
                "Ramanujan series for \\(\\sqrt{2}\\):\\n"
                "    \\(\\sqrt{2}=\\sum_{n=0}^{\\infty}\\binom{1/2}{n}(-1)^n\\)"
            ],
            "phi": [
                "Ramanujan nested radical for the golden ratio \\(\\phi\\):\\n"
                "    \\(\\phi=1+\\frac{1}{1+\\frac{1}{1+\\frac{1}{1+\\cdots}}}\\)",
                "Ramanujan series for \\(\\phi\\):\\n"
                "    \\(\\phi=\\sum_{n=0}^{\\infty}\\frac{1}{F_{2n+1}}\\)  (where \\(F_n\\) are Fibonacci numbers)"
            ],
            "apery": [
                "Ramanujan‑type series for Apéry's constant \\(\\zeta(3)\\):\\n"
                "    \\(\\zeta(3)=\\frac{5}{2}\\sum_{n=1}^{\\infty}\\frac{(-1)^{n-1}}{n^3\\binom{2n}{n}}\\)",
                "Ramanujan nested radical for \\(\\zeta(3)\\) (due to Ramanujan):\\n"
                "    \\(\\zeta(3)=\\frac{\\pi^2}{7}\\left(\\sqrt[3]{\\frac{1}{2}}+\\sqrt[3]{\\frac{3}{2}}+\\sqrt[3]{\\frac{5}{2}}+\\cdots\\right)\\)"
            ],
        }

        if key not in formulas:
            return f"Error: Unsupported constant '{constant}'. Supported constants are: pi, e, sqrt2, phi, apery."

        # Join multiple formulas with a blank line for readability
        result = "\n\n".join(formulas[key])
        return result

    except Exception as e:
        return f"Error generating Ramanujan formulas: {str(e)}"