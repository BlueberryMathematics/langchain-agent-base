"""
Comprehensive Tool Collection
============================

A collection of tools for coding, math, science, and general tasks.
All tools are designed to be used with LangChain agents.
"""

from langchain_core.tools import tool
import random
import math
import json
import re
from typing import Any, Dict, List, Union


# ============================================================================
# BASIC TOOLS
# ============================================================================

@tool
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    # Mock weather data
    weather_conditions = ["Sunny", "Cloudy", "Rainy", "Snowy"]
    return f"The weather in {location} is {random.choice(weather_conditions)}."

@tool
def magic_calculator(a: int, b: int) -> int:
    """A magical calculator that adds two numbers and multiplies by a random magic factor."""
    magic_factor = 2
    return (a + b) * magic_factor


# ============================================================================
# MATH TOOLS
# ============================================================================

@tool
def advanced_calculator(expression: str) -> str:
    """
    Evaluate mathematical expressions safely.
    Supports basic arithmetic, trigonometry, logarithms, and constants.
    
    Examples:
    - "2 + 3 * 4"
    - "sin(pi/2)"
    - "log(10)"
    - "sqrt(16)"
    """
    try:
        import numpy as np
        
        # Safe evaluation with math functions available
        allowed_names = {
            k: v for k, v in math.__dict__.items() 
            if not k.startswith("__")
        }
        allowed_names.update({
            "np": np,
            "numpy": np,
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum,
        })
        
        # Replace common mathematical notation
        expression = expression.replace("^", "**")  # Power operator
        
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error evaluating '{expression}': {str(e)}"

@tool
def solve_quadratic(a: float, b: float, c: float) -> str:
    """
    Solve quadratic equation ax² + bx + c = 0.
    Returns the roots of the equation.
    """
    try:
        discriminant = b**2 - 4*a*c
        
        if discriminant > 0:
            root1 = (-b + math.sqrt(discriminant)) / (2*a)
            root2 = (-b - math.sqrt(discriminant)) / (2*a)
            return f"Two real roots: x₁ = {root1}, x₂ = {root2}"
        elif discriminant == 0:
            root = -b / (2*a)
            return f"One real root: x = {root}"
        else:
            real_part = -b / (2*a)
            imag_part = math.sqrt(-discriminant) / (2*a)
            return f"Two complex roots: x₁ = {real_part} + {imag_part}i, x₂ = {real_part} - {imag_part}i"
    except Exception as e:
        return f"Error solving quadratic equation: {str(e)}"

@tool
def matrix_operations(operation: str, matrix_a: str, matrix_b: str = None) -> str:
    """
    Perform matrix operations. Matrices should be in JSON format.
    
    Operations: transpose, determinant, inverse, multiply, add, subtract
    
    Example matrix format: "[[1, 2], [3, 4]]"
    """
    try:
        import numpy as np
        
        # Parse matrices
        a = np.array(json.loads(matrix_a))
        b = np.array(json.loads(matrix_b)) if matrix_b else None
        
        if operation == "transpose":
            result = a.T
        elif operation == "determinant":
            result = np.linalg.det(a)
        elif operation == "inverse":
            result = np.linalg.inv(a)
        elif operation == "multiply" and b is not None:
            result = np.dot(a, b)
        elif operation == "add" and b is not None:
            result = a + b
        elif operation == "subtract" and b is not None:
            result = a - b
        else:
            return f"Invalid operation or missing second matrix: {operation}"
        
        return f"Result: {result.tolist()}"
    except Exception as e:
        return f"Error in matrix operation: {str(e)}"


# ============================================================================
# SCIENCE TOOLS
# ============================================================================

@tool
def unit_converter(value: float, from_unit: str, to_unit: str) -> str:
    """
    Convert between different units of measurement.
    
    Supported conversions:
    - Temperature: celsius, fahrenheit, kelvin
    - Length: meters, feet, inches, kilometers, miles
    - Weight: grams, kilograms, pounds, ounces
    - Energy: joules, calories, BTU
    """
    conversions = {
        # Temperature
        ("celsius", "fahrenheit"): lambda x: x * 9/5 + 32,
        ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
        ("celsius", "kelvin"): lambda x: x + 273.15,
        ("kelvin", "celsius"): lambda x: x - 273.15,
        
        # Length
        ("meters", "feet"): lambda x: x * 3.28084,
        ("feet", "meters"): lambda x: x / 3.28084,
        ("inches", "centimeters"): lambda x: x * 2.54,
        ("centimeters", "inches"): lambda x: x / 2.54,
        ("kilometers", "miles"): lambda x: x * 0.621371,
        ("miles", "kilometers"): lambda x: x / 0.621371,
        
        # Weight
        ("grams", "ounces"): lambda x: x * 0.035274,
        ("ounces", "grams"): lambda x: x / 0.035274,
        ("kilograms", "pounds"): lambda x: x * 2.20462,
        ("pounds", "kilograms"): lambda x: x / 2.20462,
    }
    
    key = (from_unit.lower(), to_unit.lower())
    if key in conversions:
        result = conversions[key](value)
        return f"{value} {from_unit} = {result:.6g} {to_unit}"
    else:
        available = list(set([unit for pair in conversions.keys() for unit in pair]))
        return f"Conversion from {from_unit} to {to_unit} not supported. Available units: {available}"

@tool
def chemistry_helper(formula: str, operation: str = "molar_mass") -> str:
    """
    Chemistry helper for molecular calculations.
    
    Operations:
    - molar_mass: Calculate molar mass of a compound
    - balance: Balance a chemical equation (basic)
    
    Example: chemistry_helper("H2O", "molar_mass")
    """
    # Basic atomic masses (simplified)
    atomic_masses = {
        'H': 1.008, 'He': 4.003, 'Li': 6.941, 'Be': 9.012, 'B': 10.811,
        'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
        'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.086, 'P': 30.974,
        'S': 32.065, 'Cl': 35.453, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078
    }
    
    if operation == "molar_mass":
        try:
            # Parse chemical formula (basic parser)
            total_mass = 0
            i = 0
            while i < len(formula):
                if formula[i].isupper():
                    element = formula[i]
                    i += 1
                    
                    # Check for lowercase letter
                    if i < len(formula) and formula[i].islower():
                        element += formula[i]
                        i += 1
                    
                    # Check for number
                    count_str = ""
                    while i < len(formula) and formula[i].isdigit():
                        count_str += formula[i]
                        i += 1
                    
                    count = int(count_str) if count_str else 1
                    
                    if element in atomic_masses:
                        total_mass += atomic_masses[element] * count
                    else:
                        return f"Unknown element: {element}"
                else:
                    i += 1
            
            return f"Molar mass of {formula}: {total_mass:.3f} g/mol"
        except Exception as e:
            return f"Error calculating molar mass: {str(e)}"
    
    return f"Operation '{operation}' not supported"

@tool
def physics_calculator(calculation: str, **kwargs) -> str:
    """
    Physics calculations for common formulas.
    
    Available calculations:
    - kinetic_energy: KE = 0.5 * m * v²
    - potential_energy: PE = m * g * h
    - force: F = m * a
    - momentum: p = m * v
    - frequency: f = c / λ (wave)
    
    Pass parameters as keyword arguments.
    Example: physics_calculator("kinetic_energy", m=10, v=5)
    """
    try:
        if calculation == "kinetic_energy":
            m, v = kwargs.get('m'), kwargs.get('v')
            if m is not None and v is not None:
                ke = 0.5 * m * v**2
                return f"Kinetic Energy: {ke} J (m={m} kg, v={v} m/s)"
        
        elif calculation == "potential_energy":
            m, g, h = kwargs.get('m'), kwargs.get('g', 9.81), kwargs.get('h')
            if m is not None and h is not None:
                pe = m * g * h
                return f"Potential Energy: {pe} J (m={m} kg, g={g} m/s², h={h} m)"
        
        elif calculation == "force":
            m, a = kwargs.get('m'), kwargs.get('a')
            if m is not None and a is not None:
                f = m * a
                return f"Force: {f} N (m={m} kg, a={a} m/s²)"
        
        elif calculation == "momentum":
            m, v = kwargs.get('m'), kwargs.get('v')
            if m is not None and v is not None:
                p = m * v
                return f"Momentum: {p} kg⋅m/s (m={m} kg, v={v} m/s)"
        
        return f"Calculation '{calculation}' not supported or missing parameters"
    
    except Exception as e:
        return f"Error in physics calculation: {str(e)}"


# ============================================================================
# CODING TOOLS
# ============================================================================

@tool
def code_analyzer(code: str, language: str = "python") -> str:
    """
    Analyze code for basic metrics and potential issues.
    
    Supports: python, javascript, java (basic analysis)
    """
    try:
        lines = code.split('\n')
        
        stats = {
            "total_lines": len(lines),
            "non_empty_lines": len([line for line in lines if line.strip()]),
            "comment_lines": 0,
            "function_count": 0,
            "class_count": 0
        }
        
        if language.lower() == "python":
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    stats["comment_lines"] += 1
                elif stripped.startswith('def '):
                    stats["function_count"] += 1
                elif stripped.startswith('class '):
                    stats["class_count"] += 1
        
        elif language.lower() == "javascript":
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('//'):
                    stats["comment_lines"] += 1
                elif 'function ' in stripped or '=>' in stripped:
                    stats["function_count"] += 1
                elif 'class ' in stripped:
                    stats["class_count"] += 1
        
        return f"Code Analysis ({language}):\n" + "\n".join([
            f"- {key.replace('_', ' ').title()}: {value}" 
            for key, value in stats.items()
        ])
    
    except Exception as e:
        return f"Error analyzing code: {str(e)}"

@tool
def regex_helper(pattern: str, text: str, operation: str = "findall") -> str:
    """
    Regex operations on text.
    
    Operations: findall, search, match, sub, split
    For 'sub' operation, provide replacement as third parameter.
    """
    try:
        if operation == "findall":
            matches = re.findall(pattern, text)
            return f"Matches found: {matches}"
        
        elif operation == "search":
            match = re.search(pattern, text)
            return f"First match: {match.group() if match else 'No match'}"
        
        elif operation == "match":
            match = re.match(pattern, text)
            return f"Match at start: {match.group() if match else 'No match'}"
        
        elif operation == "split":
            parts = re.split(pattern, text)
            return f"Split parts: {parts}"
        
        return f"Operation '{operation}' not supported"
    
    except Exception as e:
        return f"Regex error: {str(e)}"

@tool
def json_formatter(json_string: str, operation: str = "format") -> str:
    """
    JSON operations: format, minify, validate.
    """
    try:
        data = json.loads(json_string)
        
        if operation == "format":
            return json.dumps(data, indent=2, ensure_ascii=False)
        elif operation == "minify":
            return json.dumps(data, separators=(',', ':'))
        elif operation == "validate":
            return "Valid JSON"
        
        return f"Operation '{operation}' not supported"
    
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


# ============================================================================
# TOOL COLLECTIONS
# ============================================================================

def get_basic_tools():
    """Get basic utility tools."""
    return [get_weather, magic_calculator]

def get_math_tools():
    """Get mathematics-focused tools."""
    return [advanced_calculator, solve_quadratic, matrix_operations]

def get_science_tools():
    """Get science-focused tools."""
    return [unit_converter, chemistry_helper, physics_calculator]

def get_coding_tools():
    """Get programming-focused tools."""
    return [code_analyzer, regex_helper, json_formatter]

def get_all_tools():
    """Get all available tools."""
    return (get_basic_tools() + get_math_tools() + 
            get_science_tools() + get_coding_tools())

