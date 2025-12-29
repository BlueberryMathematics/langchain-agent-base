"""Test the new is_prime tool"""
import sys
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Fix the import paths
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "examples" / "building-ultimate-math-agent"))

from math_discovery_agent import create_math_discovery_agent

print(" Testing Prime Checker Tool")
print("=" * 70)

# Create agent without memory (simpler for testing)
print("\n Creating agent...")
agent = create_math_discovery_agent(enable_memory=False)
print(" Agent created!\n")

# Test the prime checker
print("Test 1: Checking if 17 is prime...")
response = agent.chat("Is 17 prime?")
print(f" Agent: {response}\n")

print("Test 2: Checking if 24 is prime...")
response = agent.chat("Is 24 prime?")
print(f" Agent: {response}\n")

print("Test 3: Checking if 97 is prime...")
response = agent.chat("Check if 97 is prime")
print(f" Agent: {response}\n")

print("Test 4: Checking if 2 is prime...")
response = agent.chat("Is 2 prime?")
print(f" Agent: {response}\n")

print("=" * 70)
print(" Prime checker tool test complete!")