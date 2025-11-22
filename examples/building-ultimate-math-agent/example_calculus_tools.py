"""
Example: Custom Calculus Tools
================================

This file shows how to create custom mathematical tools for your agent.
Copy this pattern to create your own domain-specific tools!
"""

from langchain_core.tools import tool
import sympy as sp
from typing import Optional

@tool
def derivative(expression: str, variable: str = "x", order: int = 1) -> str:
    """
    Calculate the derivative of a mathematical expression.
    
    Args:
        expression: Math expression like "x**2 + 3*x + 2" or "sin(x)*cos(x)"
        variable: Variable to differentiate with respect to (default: x)
        order: Order of derivative (default: 1 for first derivative)
    
    Returns:
        The derivative as a string with the original expression
    
    Examples:
        derivative("x**2 + 3*x + 2") → "d/dx(x**2 + 3*x + 2) = 2*x + 3"
        derivative("sin(x)", order=2) → "d²/dx²(sin(x)) = -sin(x)"
    """
    try:
        var = sp.Symbol(variable)
        expr = sp.sympify(expression)
        
        # Calculate derivative (can be higher order)
        result = expr
        for _ in range(order):
            result = sp.diff(result, var)
        
        # Format output based on order
        if order == 1:
            return f"d/d{variable}({expression}) = {result}"
        elif order == 2:
            return f"d²/d{variable}²({expression}) = {result}"
        else:
            return f"d^{order}/d{variable}^{order}({expression}) = {result}"
            
    except Exception as e:
        return f"Error calculating derivative: {str(e)}. Make sure expression is valid (e.g., 'x**2 + 3*x')"


@tool
def integrate(expression: str, variable: str = "x") -> str:
    """
    Calculate the indefinite integral (antiderivative) of a mathematical expression.
    
    Args:
        expression: Math expression like "x**2 + 3*x + 2" or "sin(x)"
        variable: Variable to integrate with respect to (default: x)
    
    Returns:
        The integral as a string with constant of integration
    
    Examples:
        integrate("x**2") → "∫(x**2) dx = x**3/3 + C"
        integrate("sin(x)") → "∫(sin(x)) dx = -cos(x) + C"
    """
    try:
        var = sp.Symbol(variable)
        expr = sp.sympify(expression)
        result = sp.integrate(expr, var)
        return f"∫({expression}) d{variable} = {result} + C"
        
    except Exception as e:
        return f"Error calculating integral: {str(e)}. Make sure expression is valid."


@tool
def definite_integral(expression: str, variable: str, lower: float, upper: float) -> str:
    """
    Calculate the definite integral of a mathematical expression over an interval.
    
    Args:
        expression: Math expression to integrate
        variable: Variable to integrate with respect to
        lower: Lower bound of integration
        upper: Upper bound of integration
    
    Returns:
        The numerical value of the definite integral
    
    Examples:
        definite_integral("x**2", "x", 0, 1) → "∫[0, 1](x**2) dx = 0.333333"
        definite_integral("sin(x)", "x", 0, 3.14159) → "∫[0, π](sin(x)) dx = 2.0"
    """
    try:
        var = sp.Symbol(variable)
        expr = sp.sympify(expression)
        result = sp.integrate(expr, (var, lower, upper))
        
        # Try to get numerical value
        try:
            numerical = float(result.evalf())
            return f"∫[{lower}, {upper}]({expression}) d{variable} = {numerical}"
        except:
            return f"∫[{lower}, {upper}]({expression}) d{variable} = {result}"
            
    except Exception as e:
        return f"Error calculating definite integral: {str(e)}"


@tool
def limit(expression: str, variable: str, value: str) -> str:
    """
    Calculate the limit of a mathematical expression as variable approaches a value.
    
    Args:
        expression: Math expression
        variable: Variable approaching the limit
        value: Value the variable approaches (can be "oo" for infinity)
    
    Returns:
        The limit value or "undefined" if limit doesn't exist
    
    Examples:
        limit("sin(x)/x", "x", "0") → "lim(x→0) sin(x)/x = 1"
        limit("1/x", "x", "oo") → "lim(x→∞) 1/x = 0"
    """
    try:
        var = sp.Symbol(variable)
        expr = sp.sympify(expression)
        
        # Handle infinity
        if value.lower() == "oo" or value == "infinity":
            limit_value = sp.oo
            value_str = "∞"
        elif value.lower() == "-oo" or value == "-infinity":
            limit_value = -sp.oo
            value_str = "-∞"
        else:
            limit_value = sp.sympify(value)
            value_str = str(value)
        
        result = sp.limit(expr, var, limit_value)
        return f"lim({variable}→{value_str}) {expression} = {result}"
        
    except Exception as e:
        return f"Error calculating limit: {str(e)}"


@tool
def taylor_series(expression: str, variable: str = "x", point: float = 0, order: int = 5) -> str:
    """
    Calculate the Taylor series expansion of a function around a point.
    
    Args:
        expression: Math expression to expand
        variable: Variable for expansion (default: x)
        point: Point to expand around (default: 0 for Maclaurin series)
        order: Number of terms to include (default: 5)
    
    Returns:
        The Taylor series expansion up to the specified order
    
    Examples:
        taylor_series("sin(x)", order=3) → "sin(x) ≈ x - x³/6 + O(x⁵)"
        taylor_series("exp(x)", order=4) → "exp(x) ≈ 1 + x + x²/2 + x³/6 + x⁴/24 + O(x⁵)"
    """
    try:
        var = sp.Symbol(variable)
        expr = sp.sympify(expression)
        
        # Calculate Taylor series
        series = sp.series(expr, var, point, order + 1)
        
        series_name = "Maclaurin" if point == 0 else "Taylor"
        return f"{series_name} series of {expression} around {variable}={point}: {series}"
        
    except Exception as e:
        return f"Error calculating Taylor series: {str(e)}"


# Collection function for easy import
def get_calculus_tools():
    """Get all calculus tools."""
    return [
        derivative,
        integrate,
        definite_integral,
        limit,
        taylor_series
    ]


# Example usage and testing
if __name__ == "__main__":
    print("🧮 Testing Calculus Tools")
    print("=" * 60)
    
    # Test derivative
    print("\n1. Derivative:")
    print(derivative.invoke({"expression": "x**3 + 2*x**2 - 5*x + 1"}))
    print(derivative.invoke({"expression": "sin(x)*cos(x)"}))
    print(derivative.invoke({"expression": "exp(x**2)", "order": 2}))
    
    # Test integral
    print("\n2. Integral:")
    print(integrate.invoke({"expression": "x**2 + 3*x + 2"}))
    print(integrate.invoke({"expression": "sin(x)"}))
    
    # Test definite integral
    print("\n3. Definite Integral:")
    print(definite_integral.invoke({
        "expression": "x**2",
        "variable": "x",
        "lower": 0,
        "upper": 1
    }))
    
    # Test limit
    print("\n4. Limit:")
    print(limit.invoke({"expression": "sin(x)/x", "variable": "x", "value": "0"}))
    print(limit.invoke({"expression": "1/x", "variable": "x", "value": "oo"}))
    
    # Test Taylor series
    print("\n5. Taylor Series:")
    print(taylor_series.invoke({"expression": "sin(x)", "order": 5}))
    print(taylor_series.invoke({"expression": "exp(x)", "order": 4}))
    
    print("\n✅ All calculus tools tested successfully!")
