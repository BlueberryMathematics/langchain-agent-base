#!/usr/bin/env python3
"""
Quick Start Script - Building Your Ultimate Math Agent
=======================================================

This script helps you quickly set up a new project using the LangChain Agent Base.

Usage:
    python quick_start.py my-math-agent
    
This will:
1. Create a new project directory
2. Copy the framework files
3. Set up the project structure
4. Create template files for your custom tools and agent
5. Initialize git repository
"""

import os
import sys
import shutil
from pathlib import Path

def create_project(project_name: str, base_path: Path = None):
    """Create a new agent project from the framework."""
    
    print(f"🚀 Creating project: {project_name}")
    print("=" * 70)
    
    # Determine paths
    if base_path is None:
        base_path = Path.cwd()
    
    project_path = base_path / project_name
    framework_path = Path(__file__).parent.parent.parent  # Go up to langchain-agent-base root
    
    if project_path.exists():
        print(f"❌ Error: Directory {project_path} already exists!")
        return False
    
    try:
        # Step 1: Create directory structure
        print("\n1️⃣ Creating directory structure...")
        project_path.mkdir(parents=True)
        (project_path / "custom_tools").mkdir()
        (project_path / "agents").mkdir()
        (project_path / "tests").mkdir()
        (project_path / "docs").mkdir()
        print("   ✅ Directories created")
        
        # Step 2: Copy framework
        print("\n2️⃣ Copying framework files...")
        src_source = framework_path / "src"
        src_dest = project_path / "src"
        
        if src_source.exists():
            shutil.copytree(src_source, src_dest)
            print("   ✅ Framework copied to src/")
        else:
            print(f"   ⚠️  Warning: Could not find src/ at {src_source}")
        
        # Step 3: Copy reference files
        print("\n3️⃣ Copying reference files...")
        files_to_copy = [
            ("pyproject.toml", "pyproject.toml"),
            (".gitignore", ".gitignore"),
            ("main.py", "main.py"),
        ]
        
        for source_file, dest_file in files_to_copy:
            source = framework_path / source_file
            dest = project_path / dest_file
            if source.exists():
                shutil.copy2(source, dest)
                print(f"   ✅ Copied {source_file}")
        
        # Step 4: Create template files
        print("\n4️⃣ Creating template files...")
        
        # custom_tools/__init__.py
        (project_path / "custom_tools" / "__init__.py").write_text('''"""
Custom Tools for Your Agent
"""

# Import your custom tools here as you create them
# from custom_tools.calculus import get_calculus_tools
# from custom_tools.statistics import get_statistics_tools

def get_all_custom_tools():
    """Get all custom tools."""
    return [
        # Add your tools here
    ]
''')
        
        # agents/__init__.py
        (project_path / "agents" / "__init__.py").write_text('''"""
Your Custom Agents
"""

from agents.math_agent import create_ultimate_math_agent

__all__ = ['create_ultimate_math_agent']
''')
        
        # agents/math_agent.py
        (project_path / "agents" / "math_agent.py").write_text('''"""
Your Ultimate Math Agent
"""

from src.base import Agent
from src.tools import get_math_tools
from src.protocol import register_agent, AgentStatus
from src.commands import create_math_commands
from custom_tools import get_all_custom_tools

@register_agent(
    name="ultimate_math",
    version="1.0.0",
    domain="mathematics",
    status=AgentStatus.PRODUCTION
)
class UltimateMathAgent(Agent):
    """Your custom math agent."""
    
    def __init__(self, enable_memory: bool = True, **kwargs):
        super().__init__(
            system_prompt="I am your ultimate math assistant.",
            enable_memory=enable_memory,
            enable_commands=True,
            **kwargs
        )
        
        # Add tools
        self.add_tools(get_math_tools())
        self.add_tools(get_all_custom_tools())
        
        # Add commands
        for cmd in create_math_commands():
            self.add_command(cmd)

def create_ultimate_math_agent(**kwargs):
    """Factory function for your agent."""
    return UltimateMathAgent(**kwargs)
''')
        
        # .env.example
        (project_path / ".env.example").write_text('''# Get your API key from https://console.groq.com/
GROQ_API_KEY=your_groq_api_key_here

# Optional: LangSmith for debugging
# LANGSMITH_API_KEY=your_langsmith_key
# LANGSMITH_TRACING=true
''')
        
        # README.md
        (project_path / "README.md").write_text(f'''# {project_name.replace("-", " ").title()}

Ultimate mathematical AI agent built with LangChain Agent Base.

## Quick Start

```bash
# Set up environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# Install dependencies
pip install -e .

# Configure API key
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Run the agent
python main.py chat
```

## Project Structure

- `src/` - LangChain Agent Base framework
- `custom_tools/` - Your custom mathematical tools
- `agents/` - Your agent definitions
- `tests/` - Test files
- `docs/` - Documentation

## Adding Custom Tools

1. Create a new file in `custom_tools/` (e.g., `calculus.py`)
2. Write your tool using `@tool` decorator
3. Import and export in `custom_tools/__init__.py`
4. Tools automatically available to your agent!

## Development

```bash
# Interactive chat
python main.py chat --memory

# Start API server
python main.py server

# Run tests
pytest tests/
```

## Documentation

See the [building-ultimate-math-agent guide](https://github.com/BlueberryMathematician/langchain-agent-base/tree/main/examples/building-ultimate-math-agent) for detailed instructions.

## License

Apache 2.0
''')
        
        print("   ✅ Template files created")
        
        # Step 5: Initialize git
        print("\n5️⃣ Initializing git repository...")
        os.chdir(project_path)
        os.system("git init")
        os.system("git add .")
        os.system('git commit -m "Initial commit: Project structure from LangChain Agent Base"')
        print("   ✅ Git repository initialized")
        
        # Step 6: Success message
        print("\n" + "=" * 70)
        print(f"✅ Project '{project_name}' created successfully!")
        print("\n📋 Next steps:")
        print(f"\n   cd {project_name}")
        print("   python -m venv .venv")
        print("   source .venv/bin/activate  # Windows: .venv\\Scripts\\activate")
        print("   pip install -e .")
        print("   cp .env.example .env")
        print("   # Edit .env and add your GROQ_API_KEY")
        print("   python main.py chat")
        print("\n💡 See README.md for full documentation")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error creating project: {e}")
        # Clean up on error
        if project_path.exists():
            shutil.rmtree(project_path)
        return False


def main():
    """Main CLI entry point."""
    
    if len(sys.argv) < 2:
        print("Usage: python quick_start.py <project-name>")
        print("\nExample:")
        print("  python quick_start.py my-ultimate-math-agent")
        sys.exit(1)
    
    project_name = sys.argv[1]
    
    # Validate project name
    if not project_name.replace("-", "").replace("_", "").isalnum():
        print("❌ Error: Project name should only contain letters, numbers, hyphens, and underscores")
        sys.exit(1)
    
    success = create_project(project_name)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
