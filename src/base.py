"""
LangChain Agent Base Classes
============================

A flexible, class-based system for building LangChain agents with Groq's gpt-oss-120b model.
Designed for coding, math, and science applications with easy tool and RAG integration.

Usage:
    from src.base import Agent
    from src.tools import get_math_tools, get_coding_tools
    from src.rag import setup_rag_tools
    
    # Create a simple agent
    agent = Agent()
    agent.add_tools(get_math_tools())
    response = agent.chat("What's 2 + 2?")
    
    # Add RAG capabilities
    rag_tools = await setup_rag_tools()
    agent.add_tools(rag_tools)
    response = agent.chat("Search the documents for X")
    
    # Load tools from toolbox
    agent.load_tools_from_toolbox(category="math")
    
    # Generate tools dynamically
    agent.generate_and_add_tool(
        "Calculate prime factors of a number",
        category="math"
    )
"""

import os
import asyncio
from typing import List, Optional, Dict, Any, Callable

from langchain_groq import ChatGroq
try:
    from langchain_ollama import ChatOllama
except ImportError:
    ChatOllama = None

from langchain.agents import create_agent
from langchain_core.tools import tool, Tool
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

try:
    from langchain.agents.middleware import HumanInTheLoopMiddleware
except ImportError:
    HumanInTheLoopMiddleware = None

from src.tools import get_basic_tools, get_math_tools, get_science_tools, get_coding_tools
from src.rag import setup_rag_tools
from src.commands import CommandRegistry, create_math_commands, create_science_commands, create_coding_commands, create_agent_commands

try:
    from src.toolbox import get_toolbox, ToolboxManager
    from src.tool_generator import ToolGenerator, ToolAssistant
    TOOLBOX_AVAILABLE = True
except ImportError:
    TOOLBOX_AVAILABLE = False

try:
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False


class Agent:
    """
    A flexible agent class that can be configured with any tools and capabilities.
    This follows the original simple design pattern from agent.py.
    """
    
    def __init__(self, 
                 model_name: str = "openai/gpt-oss-120b",
                 provider: str = "groq",
                 temperature: float = 0,
                 system_prompt: str = "You are a helpful AI assistant specialized in coding, math, and science.",
                 tools: List[Callable] = None,
                 enable_commands: bool = False,
                 enable_memory: bool = False,
                 memory_session_id: str = "default",
                 **model_kwargs):
        """
        Initialize the agent.
        
        Args:
            model_name: The model to use
            provider: The LLM provider ("groq" or "ollama")
            temperature: Model temperature (0-2)
            system_prompt: System prompt for the agent
            tools: Initial list of tools to add
            enable_commands: Whether to enable command system
            **model_kwargs: Additional model parameters
        """
        self.model_name = model_name
        self.provider = provider
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.model_kwargs = model_kwargs
        self.tools = []
        self.agent = None
        
        # Initialize command system if requested
        self.commands = CommandRegistry() if enable_commands else None
        
        # Memory system integration
        self.enable_memory = enable_memory
        self.memory_session_id = memory_session_id
        self.memory_manager = None
        
        if enable_memory and MEMORY_AVAILABLE:
            try:
                from src.memory import get_memory_manager
                self.memory_manager = get_memory_manager()
            except ImportError:
                print("⚠️ Memory system not available")
                self.memory_manager = None
        
        # Setup model
        if self.provider == "ollama":
            if ChatOllama is None:
                raise ImportError("langchain-ollama is not installed. Please install it with: pip install langchain-ollama")
            
            self.model = ChatOllama(
                model=self.model_name,
                temperature=self.temperature,
                **self.model_kwargs
            )
        else:
            # Default to Groq
            self.model = ChatGroq(
                model=self.model_name,
                temperature=self.temperature,
                **self.model_kwargs
            )
        
        # Add initial tools
        if tools:
            self.add_tools(tools)
        else:
            # Add basic tools by default
            self.add_tools(get_basic_tools())
    
    def add_tool(self, tool_func: Callable):
        """
        Add a tool to the agent.
        
        Args:
            tool_func: A function decorated with @tool or a Tool object
        """
        self.tools.append(tool_func)
        self._rebuild_agent()
    
    def add_tools(self, tools: List[Callable]):
        """Add multiple tools at once."""
        self.tools.extend(tools)
        self._rebuild_agent()
    
    def remove_tool(self, tool_name: str):
        """Remove a tool by name."""
        self.tools = [t for t in self.tools if getattr(t, 'name', str(t)) != tool_name]
        self._rebuild_agent()
    
    def list_tools(self) -> List[str]:
        """List all available tool names."""
        return [getattr(tool, 'name', str(tool)) for tool in self.tools]
    
    def load_tools_from_toolbox(self, category: str = None, tags: List[str] = None):
        """
        Load tools from the toolbox system.
        
        Args:
            category: Load tools from specific category
            tags: Load tools matching specific tags
        """
        if not TOOLBOX_AVAILABLE:
            print("⚠️  Toolbox system not available")
            return
        
        toolbox = get_toolbox()
        
        if category:
            tools = toolbox.get_tools_by_category(category)
        elif tags:
            tools = toolbox.get_tools_by_tags(tags)
        else:
            tools = toolbox.get_all_tools()
        
        self.add_tools(tools)
        print(f"✅ Loaded {len(tools)} tools from toolbox")
    
    def generate_and_add_tool(self, description: str, category: str = "custom") -> bool:
        """
        Generate a new tool using LLM and add it to the agent.
        
        Args:
            description: What the tool should do
            category: Tool category
        
        Returns:
            True if successful
        """
        if not TOOLBOX_AVAILABLE:
            print("⚠️  Tool generator not available")
            return False
        
        assistant = ToolAssistant()
        success, message, tool_func = assistant.create_tool_for_agent(
            self,
            tool_description=description,
            category=category,
            add_to_agent=True
        )
        
        print(message)
        return success
    
    def _rebuild_agent(self):
        """Rebuild the agent with current tools and configuration."""
        self.agent = create_agent(
            model=self.model,
            tools=self.tools,
            system_prompt=self.system_prompt
        )
    
    def chat(self, message: str, session_id: str = None, **kwargs) -> str:
        """
        Send a message to the agent and get a response.
        
        Args:
            message: The user message
            session_id: Optional session ID for memory (overrides default)
            **kwargs: Additional parameters for the agent
        
        Returns:
            The agent's response as a string
        """
        if not self.agent:
            self._rebuild_agent()
        
        # Handle memory integration
        if self.enable_memory and self.memory_manager:
            actual_session_id = session_id or self.memory_session_id
            
            # Get conversation context
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                context = loop.run_until_complete(
                    self.memory_manager.get_context_for_session(actual_session_id)
                )
                
                # Enhance message with context
                if context:
                    enhanced_message = f"""Previous conversation context:
{context}

Current message: {message}"""
                else:
                    enhanced_message = message
                
                # Get response
                response = self.agent.invoke({
                    "messages": [{"role": "user", "content": enhanced_message}]
                }, **kwargs)
                
                response_content = response["messages"][-1].content
                
                # Store in memory
                loop.run_until_complete(
                    self.memory_manager.add_message(
                        session_id=actual_session_id,
                        message=message,  # Store original message, not enhanced
                        response=response_content
                    )
                )
                
                return response_content
                
            finally:
                loop.close()
        else:
            # Standard chat without memory
            response = self.agent.invoke({
                "messages": [{"role": "user", "content": message}]
            }, **kwargs)
            
            return response["messages"][-1].content
    
    def stream_chat(self, message: str, **kwargs):
        """
        Stream the agent's response.
        
        Args:
            message: The user message
            **kwargs: Additional parameters for the agent
        
        Yields:
            Chunks of the agent's response
        """
        if not self.agent:
            self._rebuild_agent()
        
        for chunk in self.agent.stream({
            "messages": [{"role": "user", "content": message}]
        }, **kwargs):
            if "messages" in chunk:
                yield chunk["messages"][-1].content
    
    def enable_commands(self):
        """Enable the command system for this agent."""
        if not self.commands:
            self.commands = CommandRegistry()
    
    def add_command(self, command_func: Callable):
        """
        Add a command to the agent.
        
        Args:
            command_func: Function decorated with @command
        """
        if not self.commands:
            self.enable_commands()
        self.commands.add_command(command_func)
    
    def add_commands(self, command_funcs: List[Callable]):
        """
        Add multiple commands to the agent.
        
        Args:
            command_funcs: List of functions decorated with @command
        """
        for cmd in command_funcs:
            self.add_command(cmd)
    
    def execute_command(self, command: str, **kwargs) -> str:
        """
        Execute a command directly.
        
        Args:
            command: Command to execute (with or without /)
            **kwargs: Command arguments
            
        Returns:
            Command result
        """
        if not self.commands:
            return "Commands not enabled. Call enable_commands() first."
        
        return self.commands.execute_command(command, **kwargs)
    
    def list_commands(self) -> List[str]:
        """List all available commands."""
        if not self.commands:
            return []
        return self.commands.list_command_names()
    
    def get_command_help(self, command_name: str) -> str:
        """Get help for a specific command."""
        if not self.commands:
            return "Commands not enabled."
        return self.execute_command("help", command_name=command_name)


class HITLAgent(Agent):
    """
    Human-in-the-Loop agent that requires approval for sensitive operations.
    Extends the basic Agent class with approval workflows.
    """
    
    def __init__(self, 
                 interrupt_tools: List[str] = None,
                 **kwargs):
        """
        Initialize HITL agent.
        
        Args:
            interrupt_tools: List of tool names that require approval
            **kwargs: Agent parameters
        """
        self.interrupt_tools = interrupt_tools or ["magic_calculator"]
        self.checkpointer = MemorySaver()
        super().__init__(**kwargs)
    
    def _rebuild_agent(self):
        """Build the HITL agent with middleware."""
        middleware = []
        if HumanInTheLoopMiddleware and self.interrupt_tools:
            interrupt_config = {tool_name: True for tool_name in self.interrupt_tools}
            middleware = [HumanInTheLoopMiddleware(interrupt_on=interrupt_config)]
        
        self.agent = create_agent(
            model=self.model,
            tools=self.tools,
            system_prompt=self.system_prompt + " You must get approval for sensitive operations.",
            middleware=middleware,
            checkpointer=self.checkpointer
        )
    
    def chat_with_approval(self, message: str, thread_id: str = None) -> Dict[str, Any]:
        """
        Chat with automatic handling of approval workflows.
        
        Args:
            message: User message
            thread_id: Thread ID for conversation tracking
        
        Returns:
            Dict with response and approval status
        """
        if not thread_id:
            from langsmith import uuid7
            thread_id = str(uuid7())
        
        config = {"configurable": {"thread_id": thread_id}}
        
        # Initial request
        events = list(self.agent.stream({
            "messages": [{"role": "user", "content": message}]
        }, config=config))
        
        # Check for interrupts
        state = self.agent.get_state(config)
        if state.tasks and state.tasks[0].interrupts:
            return {
                "status": "awaiting_approval",
                "thread_id": thread_id,
                "interrupt_id": state.tasks[0].interrupts[0].id,
                "message": "Operation requires approval. Call approve_and_continue() to proceed."
            }
        
        # No interrupts, return response
        if events and "messages" in events[-1]:
            return {
                "status": "completed",
                "response": events[-1]["messages"][-1].content,
                "thread_id": thread_id
            }
        
        return {"status": "error", "message": "No response received"}
    
    def approve_and_continue(self, thread_id: str, interrupt_id: str) -> str:
        """
        Approve an interrupted operation and continue.
        
        Args:
            thread_id: The conversation thread ID
            interrupt_id: The interrupt ID to approve
        
        Returns:
            The agent's final response
        """
        config = {"configurable": {"thread_id": thread_id}}
        resume_payload = {
            interrupt_id: {"decisions": [{"type": "approve"}]}
        }
        
        resume_output = list(self.agent.stream(
            Command(resume=resume_payload), config=config
        ))
        
        if resume_output and "messages" in resume_output[-1]:
            return resume_output[-1]["messages"][-1].content
        
        # Check final state if no events
        final_state = self.agent.get_state(config)
        if final_state.values and "messages" in final_state.values:
            return final_state.values["messages"][-1].content
        
        return "Operation completed but no response received."


# Convenience factory functions that follow the original pattern
def create_simple_agent(**kwargs) -> Agent:
    """Create a basic agent with default tools."""
    return Agent(**kwargs)

async def create_rag_agent(urls: List[str] = None, documents: List[str] = None, **kwargs) -> Agent:
    """Create an agent with RAG capabilities - RAG as tools, not separate agent."""
    agent = Agent(**kwargs)
    
    # Add RAG tools to the agent
    try:
        if urls or documents:
            # Import here to avoid circular imports
            from src.rag import RAGManager
            rag_manager = RAGManager()
            
            if urls:
                rag_tools = await rag_manager.setup_from_urls(urls, "documents")
            else:
                rag_tools = await rag_manager.setup_from_documents(documents, "documents")
            
            agent.add_tools(rag_tools)
        else:
            # Use default setup
            rag_tools = await setup_rag_tools()
            agent.add_tools(rag_tools)
    except Exception as e:
        print(f"Failed to setup RAG tools: {e}")
    
    # Update system prompt for RAG usage
    agent.system_prompt += " Use the search tools to find relevant information before answering questions."
    agent._rebuild_agent()
    
    return agent

def create_coding_agent(enable_commands: bool = True, **kwargs) -> Agent:
    """Create an agent specialized for coding tasks."""
    
    @tool
    def execute_python(code: str) -> str:
        """Execute Python code and return the result. Use with caution."""
        try:
            # In production, use a sandboxed environment
            result = eval(code) if code.strip() else "No code provided"
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"
    
    tools = get_coding_tools() + [execute_python]
    
    agent = Agent(
        system_prompt="You are an expert programming assistant. Help with code analysis, debugging, and development. You can execute Python code when needed.",
        tools=tools,
        enable_commands=enable_commands,
        **kwargs
    )
    
    # Add coding-specific commands
    if enable_commands:
        agent.add_commands(create_coding_commands())
        agent.add_commands(create_agent_commands())
    
    return agent

def create_math_agent(enable_commands: bool = True, **kwargs) -> Agent:
    """Create an agent specialized for mathematical tasks.""" 
    tools = get_math_tools()
    
    agent = Agent(
        system_prompt="You are a mathematical expert. Solve complex equations, perform calculations, and explain mathematical concepts clearly.",
        tools=tools,
        enable_commands=enable_commands,
        **kwargs
    )
    
    # Add math-specific commands
    if enable_commands:
        agent.add_commands(create_math_commands())
        agent.add_commands(create_agent_commands())
    
    return agent

def create_science_agent(enable_commands: bool = True, **kwargs) -> Agent:
    """Create an agent specialized for scientific tasks."""
    tools = get_science_tools()
    
    agent = Agent(
        system_prompt="You are a scientific expert. Help with physics, chemistry, biology, and other scientific calculations and concepts.",
        tools=tools,
        enable_commands=enable_commands,
        **kwargs
    )
    
    # Add science-specific commands
    if enable_commands:
        agent.add_commands(create_science_commands())
        agent.add_commands(create_agent_commands())
    
    return agent


def create_memory_enhanced_agent(enable_commands: bool = True, **kwargs) -> Agent:
    """Create an agent with conversation memory capabilities."""
    agent = Agent(
        system_prompt="""You are an intelligent assistant with access to conversation memory. 
You can search through our previous conversations to find relevant context and information.
Use the memory search tools when users refer to previous discussions, ask about past topics,
or when you need historical context to provide better responses.""",
        enable_memory=True,
        enable_commands=enable_commands,
        **kwargs
    )
    
    # Add comprehensive tool set
    agent.add_tools(get_basic_tools())
    agent.add_tools(get_math_tools())
    agent.add_tools(get_science_tools())
    agent.add_tools(get_coding_tools())
    
    if enable_commands:
        agent.enable_commands()
        agent.add_commands(create_math_commands())
        agent.add_commands(create_science_commands())
        agent.add_commands(create_coding_commands())
        agent.add_commands(create_agent_commands())
    
    return agent


async def create_multi_agent_supervisor(**kwargs) -> Agent:
    """
    Create a supervisor agent that can delegate to other specialized agents.
    This follows the original multi-agent pattern from agent.py.
    """
    
    # Create specialized agents as tools
    math_agent = create_math_agent()
    science_agent = create_science_agent()
    coding_agent = create_coding_agent()
    
    # Try to add RAG agent
    try:
        rag_agent = await create_rag_agent()
    except:
        rag_agent = None
    
    @tool
    def ask_math_agent(query: str) -> str:
        """Ask the math agent for mathematical calculations and problem solving."""
        return math_agent.chat(query)
    
    @tool
    def ask_science_agent(query: str) -> str:
        """Ask the science agent for physics, chemistry, and scientific calculations."""
        return science_agent.chat(query)
    
    @tool
    def ask_coding_agent(query: str) -> str:
        """Ask the coding agent for programming help and code analysis."""
        return coding_agent.chat(query)
    
    supervisor_tools = [ask_math_agent, ask_science_agent, ask_coding_agent]
    
    if rag_agent:
        @tool
        def ask_research_agent(query: str) -> str:
            """Ask the research agent to search documents and provide information."""
            return rag_agent.chat(query)
        supervisor_tools.append(ask_research_agent)
    
    supervisor = Agent(
        system_prompt="""You are a supervisor agent that coordinates multiple specialized agents.
        Route tasks to the most appropriate agent based on the query type:
        - Math agent for calculations and equations
        - Science agent for physics/chemistry questions  
        - Coding agent for programming tasks
        - Research agent for document search (if available)
        
        You can delegate to multiple agents if needed for complex tasks.""",
        tools=supervisor_tools,
        **kwargs
    )
    
    return supervisor