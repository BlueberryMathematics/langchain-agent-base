# API Reference

Complete reference for all classes, methods, and functions in the LangChain Agent Base.

## Core Classes

### Agent

The main agent class that can be configured with any tools and capabilities.

```python
from src.base import Agent
```

### AgentCard

Metadata container for agent registration and versioning.

```python
from src.protocol import AgentCard, AgentStatus
```

#### Properties
- `name`: Agent identifier
- `version`: Semantic version (e.g., "1.2.0")
- `domain`: Domain category (math, science, finance, etc.)
- `category`: Agent type (specialist, generalist, etc.)
- `description`: Human-readable description
- `system_prompt`: LLM system prompt
- `tools`: List of available tool names
- `commands`: List of available command names
- `status`: AgentStatus enum value
- `created_at`/`updated_at`: Timestamps
- `author`: Agent creator
- `tags`: Searchable keywords

### AgentRegistry

Central registry for managing agent versions and metadata.

```python
from src.protocol import get_agent_registry
registry = get_agent_registry()
```

#### Methods

##### `register_agent_class(agent_class, **metadata) -> AgentCard`
Register an agent class with metadata.

##### `get_agent_card(name: str, version: str = None) -> AgentCard`
Retrieve agent metadata card.

##### `list_agents(domain: str = None, status: AgentStatus = None) -> List[AgentCard]`
List registered agents with optional filtering.

#### Constructor

```python
Agent(
    model_name: str = "openai/gpt-oss-120b",
    temperature: float = 0,
    system_prompt: str = "You are a helpful AI assistant...",
    tools: List[Callable] = None,
    enable_commands: bool = False,
    **model_kwargs
)
```

**Parameters:**
- `model_name`: Groq model name (default: "openai/gpt-oss-120b")
- `temperature`: Model temperature 0-1 (default: 0 for deterministic)
- `system_prompt`: System prompt for the agent
- `tools`: List of tool functions to add initially
- `enable_commands`: Whether to enable command system
- `**model_kwargs`: Additional arguments passed to ChatGroq

#### Methods

##### `chat(message: str, **kwargs) -> str`
Send a message to the agent and get a response.

```python
response = agent.chat("What's 2 + 2?")
```

##### `add_tool(tool_func: Callable)`
Add a single tool to the agent.

```python
from langchain_core.tools import tool

@tool
def my_tool() -> str:
    return "Hello from my tool!"

agent.add_tool(my_tool)
```

##### `add_tools(tools: List[Callable])`
Add multiple tools to the agent.

```python
from src.tools import get_math_tools
agent.add_tools(get_math_tools())
```

##### `remove_tool(tool_name: str)`
Remove a tool by name.

```python
agent.remove_tool("calculator")
```

##### `list_tools() -> List[str]`
Get list of available tool names.

```python
tools = agent.list_tools()
# ['get_weather', 'magic_calculator']
```

##### `enable_commands()`
Enable the command system for direct tool execution.

```python
agent.enable_commands()
```

##### `execute_command(command: str, **kwargs) -> str`
Execute a command directly without LLM inference.

```python
result = agent.execute_command("/calc", expression="2 + 2")
```

##### `list_commands() -> List[str]`
Get list of available commands.

```python
commands = agent.list_commands()
# ['/help', '/list', '/calc', '/solve']
```

### HITLAgent

Human-in-the-Loop agent that requires approval for sensitive operations.

```python
from src.base import HITLAgent
```

#### Constructor

```python
HITLAgent(
    interrupt_tools: List[str] = None,
    approval_timeout: int = 300,
    **kwargs  # Same as Agent constructor
)
```

**Parameters:**
- `interrupt_tools`: List of tool names requiring approval
- `approval_timeout`: Timeout in seconds for approval requests
- `**kwargs`: All Agent constructor parameters

#### Methods

##### `chat_with_approval(message: str, thread_id: str) -> Dict`
Chat with approval workflow for sensitive operations.

```python
result = hitl_agent.chat_with_approval(
    "Delete old files", 
    thread_id="session_123"
)
```

##### `approve_and_continue(thread_id: str, interrupt_id: str) -> str`
Approve a pending operation and continue execution.

```python
final_result = hitl_agent.approve_and_continue(thread_id, interrupt_id)
```

## Factory Functions

### create_simple_agent(**kwargs) -> Agent
Create a basic agent with default settings.

```python
from src.base import create_simple_agent
agent = create_simple_agent()
```

### create_math_agent(enable_commands: bool = True, **kwargs) -> Agent
Create an agent pre-configured with math tools and commands.

```python
from src.base import create_math_agent
math_agent = create_math_agent()
```

**Tools included:**
- Advanced calculator
- Quadratic equation solver
- Matrix operations

### create_science_agent(enable_commands: bool = True, **kwargs) -> Agent
Create an agent pre-configured with science tools and commands.

```python
from src.base import create_science_agent
science_agent = create_science_agent()
```

**Tools included:**
- Unit converter
- Chemistry helper
- Physics calculator

### create_coding_agent(enable_commands: bool = True, **kwargs) -> Agent
Create an agent pre-configured with coding tools and commands.

```python
from src.base import create_coding_agent
coding_agent = create_coding_agent()
```

**Tools included:**
- Code analyzer
- Regex helper
- JSON formatter

### create_rag_agent(urls: List[str] = None, documents: List[str] = None, **kwargs) -> Agent
Create an agent with document search capabilities.

```python
from src.base import create_rag_agent

# From URLs
rag_agent = await create_rag_agent(urls=["https://example.com"])

# From documents
rag_agent = await create_rag_agent(documents=["doc1", "doc2"])
```

### create_multi_agent_supervisor(**kwargs) -> Agent
Create a supervisor agent that coordinates multiple specialists.

```python
from src.base import create_multi_agent_supervisor
supervisor = await create_multi_agent_supervisor()
```

## Tool Collections

### Basic Tools

```python
from src.tools import get_basic_tools
tools = get_basic_tools()
# [get_weather, magic_calculator]
```

### Math Tools

```python
from src.tools import get_math_tools
tools = get_math_tools()
# [advanced_calculator, solve_quadratic, matrix_operations]
```

### Science Tools

```python
from src.tools import get_science_tools
tools = get_science_tools()
# [unit_converter, chemistry_helper, physics_calculator]
```

### Coding Tools

```python
from src.tools import get_coding_tools
tools = get_coding_tools()
# [code_analyzer, regex_helper, json_formatter]
```

### All Tools

```python
from src.tools import get_all_tools
tools = get_all_tools()
# Returns all available tools
```

## RAG System

### RAGManager

Manages document indexing and retrieval for RAG applications.

```python
from src.rag import RAGManager
```

#### Constructor

```python
RAGManager(
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    vector_size: int = 384
)
```

#### Methods

##### `setup_from_urls(urls: List[str], collection_name: str = "web_docs") -> List`
Setup RAG from web URLs.

```python
rag_manager = RAGManager()
rag_tools = await rag_manager.setup_from_urls(["https://example.com"])
```

##### `setup_from_documents(documents: List[str], collection_name: str = "text_docs") -> List`
Setup RAG from text documents.

```python
rag_tools = await rag_manager.setup_from_documents(["doc1", "doc2"])
```

## Command System

### CommandRegistry

Manages agent commands for direct tool execution.

```python
from src.commands import CommandRegistry
```

#### Methods

##### `execute_command(command_str: str, **kwargs) -> str`
Execute a command directly.

```python
registry = CommandRegistry()
result = registry.execute_command("/help")
```

### @command Decorator

Decorator to register functions as commands.

```python
from src.commands import command

@command("greet", "Say hello", "/greet <name>")
def greet_command(name: str) -> str:
    return f"Hello, {name}!"
```

**Parameters:**
- `name`: Command name (without /)
- `description`: Command description
- `usage`: Usage example

## Environment Variables

### Required
- `GROQ_API_KEY`: Your Groq API key for model access

### Optional
- `LANGSMITH_API_KEY`: LangSmith key for tracing (optional)
- `LANGSMITH_TRACING`: Set to "true" to enable tracing
- `LANGSMITH_PROJECT`: Project name for LangSmith

## Error Handling

All methods include appropriate error handling. Common exceptions:

- `ValueError`: Invalid parameters or configuration
- `ImportError`: Missing dependencies
- `RuntimeError`: Agent execution errors
- `TimeoutError`: Approval timeout in HITL agents

```python
try:
    response = agent.chat("Hello")
except Exception as e:
    print(f"Agent error: {e}")
```

## Type Hints

All functions include complete type hints for better IDE support:

```python
from typing import List, Optional, Dict, Any, Callable

def my_function(agents: List[Agent]) -> Optional[str]:
    # Function implementation
    pass
```