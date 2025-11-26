"""
Tool: continued_fraction_analysis
Category: math
Author: llm
Version: 1.0.0
Created: 2025-11-26T00:50:33.907286
Description: Calculate and analyze the continued fraction representation of a given number.

Args:
    number: Id...
"""

from langchain_core.tools import tool
import typing
import math

from typing import List, Tuple
import math
from langchain_core.tools import tool

def _compute_continued_fraction(x: float, max_terms: int) -> List[int]:
    """Return the list of continued fraction coefficients for x up to max_terms."""
    coeffs: List[int] = []
    for _ in range(max_terms):
        a = math.floor(x)
        coeffs.append(a)
        frac = x - a
        if abs(frac) < 1e-15:  # exact integer reached
            break
        x = 1.0 / frac
    return coeffs

def _convergent(coeffs: List[int]) -> Tuple[int, int]:
    """Compute the numerator and denominator of the convergent from coeffs."""
    if not coeffs:
        return 0, 1
    # Initialize with the last term
    num, den = 1, 0
    for a in reversed(coeffs):
        num, den = a * num + den, num
    return num, den

@tool
def continued_fraction_analysis(number: str, terms: int) -> str:
    """
    Calculate and analyze the continued fraction representation of a given number.
    
    Args:
        number: Identifier of the target number. Supported values:
                - "pi" for π
                - "e" for Euler's number
                - "sqrt<N>" where <N> is a positive integer (e.g., "sqrt2")
        terms: Number of continued fraction terms to compute (must be positive).
    
    Returns:
        A formatted string containing:
        - The list of continued fraction coefficients.
        - The convergent fraction (numerator/denominator) after the requested terms.
        - The decimal value of that convergent.
        - The absolute error compared to the true value.
        Errors are reported as strings prefixed with "Error:".
    
    Example:
        continued_fraction_analysis("sqrt2", 5) ->
        "Continued fraction for sqrt(2) (5 terms):
         Coefficients: [1, 2, 2, 2, 2]
         Convergent: 41/29 ≈ 1.41379
         Error: 0.00003"
    """
    try:
        if terms <= 0:
            return "Error: 'terms' must be a positive integer"
        
        # Resolve the target value
        if number.lower() == "pi":
            value = math.pi
            name = "π"
        elif number.lower() == "e":
            value = math.e
            name = "e"
        elif number.lower().startswith("sqrt"):
            try:
                n_str = number[4:]  # after 'sqrt'
                n = int(n_str)
                if n <= 0:
                    return "Error: Square root argument must be positive"
                value = math.sqrt(n)
                name = f"sqrt({n})"
            except ValueError:
                return "Error: Invalid format for square root. Use 'sqrt<N>' where N is an integer."
        else:
            return "Error: Unsupported number identifier. Use 'pi', 'e', or 'sqrt<N>'."
        
        # Compute continued fraction coefficients
        coeffs = _compute_continued_fraction(value, terms)
        if not coeffs:
            return "Error: Failed to compute continued fraction coefficients."
        
        # Compute convergent from the coefficients
        num, den = _convergent(coeffs)
        if den == 0:
            return "Error: Denominator of convergent is zero."
        approx = num / den
        error = abs(value - approx)
        
        # Build result string
        coeffs_str = ", ".join(str(c) for c in coeffs)
        result = (
            f"Continued fraction for {name} ({len(coeffs)} terms):\n"
            f"Coefficients: [{coeffs_str}]\n"
            f"Convergent: {num}/{den} ≈ {approx:.10f}\n"
            f"Error: {error:.10f}"
        )
        return result
    
    except Exception as e:
        return f"Error during continued fraction analysis: {str(e)}"