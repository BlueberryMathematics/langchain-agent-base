## Ultimate Coding Agent v2.0

A specialized AI agent for software development with memory, RAG, safety controls, and intelligent context management.

## ✨ What's New in v2.0

- **🧠 Conversation Memory**: Persistent memory across sessions with automatic summarization
- **📚 RAG Knowledge Base**: Upload reference files and search across project documentation
- **📊 Context Management**: Optimized for 2000 token windows with smart compression
- **📁 File Upload**: Add reference files to enhance agent's understanding
- **🎯 Session Tracking**: Organize work by feature/task with session IDs

## 🎯 Features

### Core Capabilities
- **🔒 Project Locking**: Agent is locked to a specific directory, cannot access files outside
- **👥 User Approval**: All file operations (create/edit/delete) require explicit user approval
- **📂 File Navigation**: Smart file tree that excludes noise (__pycache__, .venv, etc.)
- **✏️ Intelligent Editing**: Agent responds with only the code changes needed
- **💻 Terminal Access**: Execute safe terminal commands within project
- **🔍 Code Search**: Find patterns across your codebase
- **📝 Code Parsing**: Automatically extracts code blocks from markdown responses

### Memory & RAG (v2.0)
- **🧠 Persistent Memory**: Conversation history stored in Qdrant vector database
- **📚 Reference Files**: Upload and search project documentation
- **🎯 Smart Context**: Automatic summarization when approaching token limits
- **🔎 Semantic Search**: Find relevant past conversations and code references
- **📊 Token Management**: Visual monitoring of context usage

## 🚀 Quick Start

### Interactive CLI Mode (Recommended)

```bash
# With memory enabled (default)
python examples/building-ultimate-coding-agent/cli.py /path/to/your/project

# Without memory
python examples/building-ultimate-coding-agent/cli.py /path/to/your/project --no-memory

# Custom session ID
python examples/building-ultimate-coding-agent/cli.py ./project --session my_feature
```

#### CLI Commands

```bash
tree              # Show file structure
upload <file>     # Upload reference file to knowledge base
references        # List all uploaded reference files
summary           # Show conversation statistics
context           # View context usage and limits
quit/exit         # Exit the CLI
```

### Programmatic Usage

```python
from examples.building_ultimate_coding_agent.coding_agent import create_coding_agent

# Create agent with memory and RAG
agent = create_coding_agent(
    project_directory="./my_project",
    enable_memory=True,
    session_id="my_session",
    max_context_tokens=2000
)

# Basic usage
response = agent.chat("Show me the file tree")
print(response)

# Upload reference file
import asyncio
result = asyncio.run(
    agent.ingest_file_for_reference(
        "./docs/architecture.md",
        description="System architecture documentation"
    )
)

# Chat with file context
response = agent.chat_with_context(
    "Create a new service following the architecture",
    include_files=["./docs/architecture.md", "./src/base_service.py"]
)
print(response)
```

## 📚 Documentation

- **[MEMORY_AND_RAG_GUIDE.md](MEMORY_AND_RAG_GUIDE.md)** - Complete guide to memory and RAG features
- **[QUICKSTART.md](QUICKSTART.md)** - Quick reference and examples

## 🛡️ Safety Features

### Directory Locking
- Agent is locked to the specified project directory
- Cannot use `cd` to change directories
- Cannot access files outside the project root

### Command Restrictions
- Dangerous commands blocked (rm -rf, format, shutdown, etc.)
- No directory traversal (../)
- 30-second timeout on all commands

### User Approval Workflow
1. Agent proposes a file operation
2. System shows exactly what will change
3. User approves or declines
4. If approved, change is applied
5. If declined, agent moves to next suggestion

## 📋 Available Tools

### Navigation & Reading
- `get_file_tree()` - View project structure (excludes __pycache__, .venv, etc.)
- `read_file(filepath)` - Read file contents
- `list_directory(dirpath)` - List directory contents
- `search_in_files(pattern, extension)` - Search for patterns in code

### File Operations (Require Approval)
- `propose_file_create(filepath, content)` - Create new file
- `propose_file_edit(filepath, changes)` - Edit existing file
- `propose_file_delete(filepath)` - Delete file

### Development Tools
- `run_terminal_command(command)` - Execute terminal commands (restricted)
- `get_python_info()` - View Python environment details

## 💡 Usage Examples

### Example 1: Create a New Module

```python
agent.chat("""
Create a new file called validators.py with these functions:
- validate_email(email: str) -> bool
- validate_phone(phone: str) -> bool
- validate_url(url: str) -> bool

Use regex patterns and add docstrings.
""")
```

The agent will respond with only the code in markdown blocks:

```python
import re
from typing import Pattern

def validate_email(email: str) -> bool:
    """Validate email address format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

### Example 2: Refactor Existing Code

```python
agent.chat("""
Read the main.py file and refactor the database connection code 
into a separate DatabaseManager class. Put it in a new db.py file.
""")
```

### Example 3: Add Error Handling

```python
agent.chat("""
Read api.py and add try-except blocks around all API calls.
Add proper logging for errors.
""")
```

## 🎯 Agent Response Format

The agent is trained to respond with **only the code changes** in markdown blocks:

```python
# Only the specific function to add
def new_function(param: str) -> int:
    """New function docstring."""
    return len(param)
```

NOT like this:
```python
# ... existing code ...
def new_function(...):  # ❌ Don't include comments like this
# ... rest of file ...   # ❌ Or placeholders
```

## 🧪 Testing

Run the comprehensive test that demonstrates building a full project:

```bash
python tests/test_building_ultimate_coding_agent.py
```

This test creates a modular Task Manager CLI application with:
- OOP design with multiple classes
- Proper project structure
- Type hints and docstrings
- JSON persistence
- Modular architecture

## 📝 System Prompt

The agent uses a specialized system prompt that instructs it to:
1. Respond with only code changes in markdown blocks
2. List files to edit clearly: "FILES: file1.py, file2.py"
3. Always check file tree before proposing changes
4. Follow project's existing code style
5. Add docstrings and type hints
6. Handle errors gracefully

## 🔧 Advanced Configuration

### Custom Project Setup

```python
agent = create_coding_agent(
    project_directory="./my_project",
    enable_memory=False,  # Disable memory for security
)
```

### With Approval System

```python
from examples.building_ultimate_coding_agent.cli import FileOperations, ApprovalSystem

# Manual approval workflow
file_ops = FileOperations(project_root)
approval = ApprovalSystem()

# Create file with approval
if approval.ask_approval("CREATE", "Creating new file..."):
    file_ops.create_file("new_file.py", code_content)
```

## 🎓 How It Works

1. **User Request**: User describes what they want to code
2. **Agent Analysis**: Agent reads necessary files, checks structure
3. **Code Generation**: Agent generates only the specific code changes
4. **Markdown Response**: Agent responds with code in markdown blocks
5. **Parsing**: System extracts code blocks from response
6. **Approval**: User approves or declines each change
7. **Application**: Approved changes are written to files

## 🚨 Limitations

- Agent cannot access files outside project directory
- Cannot use `cd` command
- Cannot execute dangerous terminal commands
- All file operations require user approval
- Commands timeout after 30 seconds

## 📚 Related Documentation

- [Building Agents Guide](../../docs/building-agents.md)
- [Adding Tools Guide](../../docs/adding-tools.md)
- [Agent Protocol System](../../docs/api-reference.md)

## 🤝 Contributing

This agent can be extended with additional tools:
- Git operations (commit, push, pull)
- Package management (pip install)
- Testing tools (pytest runner)
- Linting and formatting (black, flake8)
- Documentation generation

Add new tools by creating `@tool` decorated functions in `coding_agent.py`.
