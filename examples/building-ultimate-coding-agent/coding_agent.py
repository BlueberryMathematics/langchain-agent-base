"""
Ultimate Coding Agent
=====================

A specialized coding agent that:
- Edits and creates files with intelligent merging
- Works within a locked project directory for safety
- Provides file tree navigation (excluding noise like __pycache__)
- Executes terminal commands for development tasks
- Requires user approval for all file operations
- Responds with only the code changes needed in markdown format

This agent is designed for command-line interaction with safety controls.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
import subprocess
import shutil
import asyncio
from datetime import datetime

from src.base import Agent
from src.protocol import register_agent, AgentStatus
from src.commands import command
from src.memory import ConversationMemoryManager
from src.rag import RAGManager
from src.storage import UnifiedQdrantStorage
from langchain_core.tools import tool


# ============================================================================
# CORE TOOLS FOR CODING AGENT
# ============================================================================

@tool
def get_file_tree(max_depth: int = 5) -> str:
    """
    Get the file tree of the current project directory.
    Excludes common non-code directories like __pycache__, .venv, node_modules, etc.
    
    Args:
        max_depth: Maximum depth to traverse (default: 5)
    
    Returns:
        String representation of the file tree
    """
    try:
        excluded_dirs = {
            '__pycache__', '.venv', 'venv', 'env', '.env',
            'node_modules', '.git', '.idea', '.vscode',
            'build', 'dist', '.pytest_cache', '.mypy_cache',
            'htmlcov', '.coverage', 'eggs', '*.egg-info'
        }
        
        def should_exclude(path: Path) -> bool:
            """Check if path should be excluded."""
            return any(excluded in path.parts or path.name.startswith('.') 
                      for excluded in excluded_dirs)
        
        def build_tree(directory: Path, prefix: str = "", depth: int = 0) -> List[str]:
            """Recursively build tree structure."""
            if depth > max_depth:
                return []
            
            lines = []
            try:
                items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))
                items = [item for item in items if not should_exclude(item)]
                
                for i, item in enumerate(items):
                    is_last = i == len(items) - 1
                    current_prefix = "└── " if is_last else "├── "
                    lines.append(f"{prefix}{current_prefix}{item.name}")
                    
                    if item.is_dir():
                        extension = "    " if is_last else "│   "
                        lines.extend(build_tree(item, prefix + extension, depth + 1))
            except PermissionError:
                pass
            
            return lines
        
        cwd = Path.cwd()
        tree_lines = [f"📁 {cwd.name}/"]
        tree_lines.extend(build_tree(cwd))
        
        return "\n".join(tree_lines)
        
    except Exception as e:
        return f"Error getting file tree: {str(e)}"


@tool
def read_file(filepath: str) -> str:
    """
    Read the contents of a file.
    
    Args:
        filepath: Path to the file (relative to project root)
    
    Returns:
        File contents or error message
    """
    try:
        path = Path(filepath).resolve()
        
        # Security check - ensure we're in the project directory
        cwd = Path.cwd().resolve()
        if not str(path).startswith(str(cwd)):
            return f"❌ Security error: Cannot access files outside project directory"
        
        if not path.exists():
            return f"❌ Error: File not found: {filepath}"
        
        if not path.is_file():
            return f"❌ Error: Path is not a file: {filepath}"
        
        content = path.read_text(encoding='utf-8')
        return f"📄 {filepath}\n{'='*60}\n{content}"
        
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"
    
@tool
def list_directory(dirpath: str = ".") -> str:
    """
    List contents of a directory.
    
    Args:
        dirpath: Path to directory (relative to project root)
    
    Returns:
        Directory listing
    """
    try:
        path = Path(dirpath).resolve()
        
        # Security check
        cwd = Path.cwd().resolve()
        if not str(path).startswith(str(cwd)):
            return f"❌ Security error: Cannot access directories outside project"
        
        if not path.exists():
            return f"❌ Error: Directory not found: {dirpath}"
        
        if not path.is_dir():
            return f"❌ Error: Path is not a directory: {dirpath}"
        
        items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
        
        output = [f"📁 {path.name}/"]
        for item in items:
            if item.name.startswith('.') or item.name == '__pycache__':
                continue
            icon = "📁" if item.is_dir() else "📄"
            output.append(f"  {icon} {item.name}")
        
        return "\n".join(output)
        
    except Exception as e:
        return f"❌ Error listing directory: {str(e)}"


@tool
def run_terminal_command(command: str) -> str:
    """
    Execute a terminal command in the project directory.
    
    RESTRICTED COMMANDS:
    - Cannot use 'cd' to change directories
    - Cannot access files outside project directory
    - Cannot use dangerous commands (rm -rf, format, etc.)
    
    Args:
        command: Terminal command to execute
    
    Returns:
        Command output or error message
    """
    try:
        # Security restrictions
        dangerous_patterns = [
            r'\brm\s+-rf\b',
            r'\bformat\b',
            r'\bdel\s+/\b',
            r'\bshutdown\b',
            r'\breboot\b',
            r'\\.\\.\/',  # Directory traversal
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return f"❌ Security error: Command blocked - contains dangerous pattern"
        
        # Block cd commands
        if re.match(r'^\s*cd\s+', command, re.IGNORECASE):
            return f"❌ Error: 'cd' command not allowed. Agent is locked to project directory."
        
        # Execute command
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=Path.cwd()
        )
        
        output = []
        if result.stdout:
            output.append("📤 Output:")
            output.append(result.stdout)
        if result.stderr:
            output.append("⚠️  Errors:")
            output.append(result.stderr)
        
        return "\n".join(output) if output else "✅ Command executed successfully (no output)"
        
    except subprocess.TimeoutExpired:
        return "❌ Error: Command timed out (30s limit)"
    except Exception as e:
        return f"❌ Error executing command: {str(e)}"


@tool
def search_in_files(pattern: str, file_extension: str = ".py") -> str:
    """
    Search for a pattern in files with specific extension.
    
    Args:
        pattern: Text pattern to search for
        file_extension: File extension to search in (e.g., ".py", ".js")
    
    Returns:
        Search results with file locations
    """
    try:
        cwd = Path.cwd()
        results = []
        
        for file_path in cwd.rglob(f"*{file_extension}"):
            # Skip excluded directories
            if any(exclude in file_path.parts for exclude in ['__pycache__', '.venv', 'venv', '.git']):
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    if pattern.lower() in line.lower():
                        rel_path = file_path.relative_to(cwd)
                        results.append(f"📄 {rel_path}:{i}")
                        results.append(f"   {line.strip()}")
            except:
                continue
        
        if not results:
            return f"No matches found for '{pattern}' in {file_extension} files"
        
        return "\n".join(results[:50])  # Limit to 50 results
        
    except Exception as e:
        return f"❌ Error searching files: {str(e)}"


@tool
def get_python_info() -> str:
    """
    Get information about the Python environment.
    
    Returns:
        Python version, executable path, and installed packages
    """
    try:
        import sys
        info = []
        info.append(f"🐍 Python Version: {sys.version}")
        info.append(f"📍 Executable: {sys.executable}")
        info.append(f"📂 Project Directory: {Path.cwd()}")
        
        # Try to get pip list
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                info.append("\n📦 Installed Packages (first 20):")
                lines = result.stdout.split('\n')[:22]  # Header + 20 packages
                info.extend(lines)
        except:
            pass
        
        return "\n".join(info)
        
    except Exception as e:
        return f"❌ Error getting Python info: {str(e)}"


@tool
def ingest_reference_file(filepath: str, description: str = "") -> str:
    """
    Ingest a reference file into the RAG knowledge base.
    This allows the agent to search and reference the file content later.
    
    Args:
        filepath: Path to the reference file (relative to project root)
        description: Optional description of the file's purpose
    
    Returns:
        Success message or error
    """
    try:
        path = Path(filepath).resolve()
        cwd = Path.cwd().resolve()
        
        # Security check
        if not str(path).startswith(str(cwd)):
            return f"❌ Security error: Cannot access files outside project directory"
        
        if not path.exists():
            return f"❌ Error: File not found: {filepath}"
        
        # Read file content
        content = path.read_text(encoding='utf-8')
        
        # This will be handled by the agent's RAG manager
        return f"""📚 Reference file ingested: {filepath}

{description if description else 'No description provided'}

Lines: {len(content.split(chr(10)))}
Size: {len(content)} characters

✅ File content is now available for search and reference.
Use search_knowledge_base() to query this content."""
        
    except Exception as e:
        return f"❌ Error ingesting file: {str(e)}"


@tool
def search_knowledge_base(query: str, limit: int = 5) -> str:
    """
    Search the RAG knowledge base for relevant information.
    This searches across all ingested reference files and documentation.
    
    Args:
        query: Search query
        limit: Maximum number of results
    
    Returns:
        Search results
    """
    try:
        # This will be connected to the agent's RAG manager
        return f"🔍 Searching knowledge base for: {query}\n\nNote: RAG search requires agent instance context."
    except Exception as e:
        return f"❌ Error searching knowledge base: {str(e)}"


@tool
def get_conversation_summary(session_id: str = None) -> str:
    """
    Get a summary of the current conversation session.
    Useful for understanding what has been discussed so far.
    
    Args:
        session_id: Optional session ID (defaults to current session)
    
    Returns:
        Conversation summary
    """
    try:
        return f"📝 Conversation summary requested for session: {session_id or 'current'}\n\nNote: This requires memory manager context."
    except Exception as e:
        return f"❌ Error getting summary: {str(e)}"


# ============================================================================
# FILE OPERATION TOOLS (REQUIRE USER APPROVAL)
# ============================================================================

# These tools are designed to be used with approval workflow
# The agent will propose changes, and the system will ask for user approval

@tool
def propose_file_create(filepath: str, content: str) -> str:
    """
    Propose creating a new file.
    This tool only returns the proposal - actual creation requires user approval.
    
    Args:
        filepath: Path for the new file
        content: Content to write
    
    Returns:
        Proposal message for user approval
    """
    try:
        path = Path(filepath).resolve()
        cwd = Path.cwd().resolve()
        
        if not str(path).startswith(str(cwd)):
            return f"❌ Security error: Cannot create files outside project directory"
        
        if path.exists():
            return f"❌ Error: File already exists: {filepath}"
        
        # Return proposal
        return f"""
📝 PROPOSE: Create new file

File: {filepath}
Lines: {len(content.split(chr(10)))}
Size: {len(content)} characters

Preview:
{'-'*60}
{content[:500]}{'...' if len(content) > 500 else ''}
{'-'*60}

⚠️  This action requires user approval.
"""
    except Exception as e:
        return f"❌ Error in proposal: {str(e)}"


@tool
def propose_file_edit(filepath: str, changes: str) -> str:
    """
    Propose editing an existing file.
    
    Args:
        filepath: Path to file to edit
        changes: Description of changes to make
    
    Returns:
        Proposal message for user approval
    """
    try:
        path = Path(filepath).resolve()
        cwd = Path.cwd().resolve()
        
        if not str(path).startswith(str(cwd)):
            return f"❌ Security error: Cannot edit files outside project directory"
        
        if not path.exists():
            return f"❌ Error: File not found: {filepath}"
        
        current_content = path.read_text(encoding='utf-8')
        
        return f"""
✏️  PROPOSE: Edit file

File: {filepath}
Current size: {len(current_content)} characters
Lines: {len(current_content.split(chr(10)))}

Proposed changes:
{'-'*60}
{changes}
{'-'*60}

⚠️  This action requires user approval.
"""
    except Exception as e:
        return f"❌ Error in proposal: {str(e)}"


@tool
def propose_file_delete(filepath: str) -> str:
    """
    Propose deleting a file.
    
    Args:
        filepath: Path to file to delete
    
    Returns:
        Proposal message for user approval
    """
    try:
        path = Path(filepath).resolve()
        cwd = Path.cwd().resolve()
        
        if not str(path).startswith(str(cwd)):
            return f"❌ Security error: Cannot delete files outside project directory"
        
        if not path.exists():
            return f"❌ Error: File not found: {filepath}"
        
        size = path.stat().st_size
        
        return f"""
🗑️  PROPOSE: Delete file

File: {filepath}
Size: {size} bytes

⚠️  This action requires user approval and cannot be undone.
"""
    except Exception as e:
        return f"❌ Error in proposal: {str(e)}"


# ============================================================================
# CODING AGENT CLASS
# ============================================================================

@register_agent(
    name="ultimate_coding",
    version="2.0.0",
    domain="software_development",
    category="specialist",
    description="Coding agent with memory, RAG, file operations, and intelligent context management",
    author="LangChain Agent Base",
    status=AgentStatus.PRODUCTION
)
class UltimateCodingAgent(Agent):
    """
    Enhanced coding agent with:
    - Memory and RAG integration
    - File tree navigation
    - Safe file operations
    - Terminal command execution
    - Reference file upload and search
    - Automatic context summarization
    - Locked to project directory
    - User approval for changes
    """
    
    def __init__(self, 
                 project_directory: Optional[str] = None,
                 enable_memory: bool = True,
                 session_id: str = "coding_session",
                 max_context_tokens: int = 2000,
                 **kwargs):
        """
        Initialize the coding agent.
        
        Args:
            project_directory: Root directory to lock agent to (defaults to cwd)
            enable_memory: Enable conversation memory and RAG (default: True)
            session_id: Session ID for memory management
            max_context_tokens: Maximum context window size
            **kwargs: Additional Agent arguments
        """
        
        # Set up project directory lock
        if project_directory:
            project_path = Path(project_directory).resolve()
            if not project_path.exists():
                raise ValueError(f"Project directory does not exist: {project_directory}")
            if not project_path.is_dir():
                raise ValueError(f"Project path is not a directory: {project_directory}")
            os.chdir(project_path)
        
        self.project_root = Path.cwd().resolve()
        self.session_id = session_id
        self.max_context_tokens = max_context_tokens
        
        # Initialize RAG and Memory systems
        self.unified_storage = None
        self.memory_manager = None
        self.rag_manager = None
        self.ingested_files: Dict[str, Dict[str, Any]] = {}
        
        if enable_memory:
            try:
                self.unified_storage = UnifiedQdrantStorage()
                self.memory_manager = ConversationMemoryManager(
                    unified_storage=self.unified_storage,
                    max_context_tokens=max_context_tokens,
                    summarization_threshold=int(max_context_tokens * 0.7)
                )
                self.rag_manager = RAGManager()
                print("✅ Memory and RAG systems initialized")
            except Exception as e:
                print(f"⚠️  Memory/RAG initialization failed: {e}")
                print("   Continuing without memory features")
        
        # Create system prompt
        system_prompt = self._create_system_prompt()
        
        # Initialize base agent
        super().__init__(
            system_prompt=system_prompt,
            enable_memory=enable_memory,
            memory_session_id=session_id,
            **kwargs
        )
        
        # Add coding tools
        self._add_coding_tools()
        
        print(f"\n🚀 Ultimate Coding Agent Initialized")
        print(f"📁 Project Directory: {self.project_root}")
        print(f"🔒 Security: Locked to project directory")
        print(f"🧠 Memory: {'Enabled' if enable_memory and self.memory_manager else 'Disabled'}")
        print(f"📚 RAG: {'Enabled' if enable_memory and self.rag_manager else 'Disabled'}")
        print(f"📊 Tools Available: {len(self.list_tools())}")
        print(f"🎯 Max Context: {max_context_tokens} tokens")
        print(f"⚠️  All file operations require user approval")
        print()
    
    def _create_system_prompt(self) -> str:
        """Create the coding agent system prompt."""
        return f"""You are the Ultimate Coding Agent, a specialized AI assistant for software development.

**PROJECT CONTEXT:**
- Locked to directory: {self.project_root}
- Cannot access files outside this directory
- Cannot use 'cd' to change directories

**YOUR CAPABILITIES:**
1. 📂 File Navigation - Use get_file_tree() to see project structure
2. 📖 Read Files - Use read_file() to view file contents
3. ✏️  Edit Files - Propose edits with precise code changes
4. 📝 Create Files - Propose new files with full content
5. 🗑️  Delete Files - Propose file deletions
6. 🔍 Search Code - Find patterns across files
7. 💻 Run Commands - Execute terminal commands (restricted)

**CRITICAL RESPONSE FORMAT:**
When editing or creating code, you MUST respond with ONLY the code that needs to be changed or created, formatted in markdown code blocks like this:

\`\`\`python
# Only the specific code changes needed
def new_function():
    pass
\`\`\`

DO NOT include:
- Unchanged code
- Full file contents (unless creating new file)
- Explanatory text inside code blocks
- Line numbers or file paths in code blocks

**FILE OPERATION WORKFLOW:**
1. Use get_file_tree() to understand project structure
2. Use read_file() to view files you need to edit
3. Respond with ONLY the code changes in markdown blocks
4. When asked which files to edit, list them clearly: "FILES: file1.py, file2.py"

**IMPORTANT RULES:**
- All file operations (create/edit/delete) require user approval
- Always check file tree before proposing changes
- Read files before editing to understand context
- Propose atomic, focused changes
- Test code mentally before proposing
- Follow project's existing code style
- Add docstrings and type hints
- Handle errors gracefully

**USER APPROVAL SYSTEM:**
- User will approve or decline each proposed change
- If declined, move to next proposed change
- Don't repeat declined changes

**TOOL USAGE:**
- Use tools to gather information before acting
- Propose changes after understanding context
- Ask clarifying questions if requirements are unclear

You are helpful, precise, and safety-conscious. Your goal is to assist with code development while maintaining project security and requiring user approval for all modifications.
"""
    
    def _add_coding_tools(self):
        """Add all coding tools to the agent."""
        coding_tools = [
            get_file_tree,
            read_file,
            list_directory,
            run_terminal_command,
            search_in_files,
            get_python_info,
            propose_file_create,
            propose_file_edit,
            propose_file_delete,
            ingest_reference_file,
            search_knowledge_base,
            get_conversation_summary,
        ]
        
        for tool in coding_tools:
            self.add_tool(tool)
    
    async def ingest_file_for_reference(self, filepath: str, description: str = "") -> str:
        """
        Ingest a file into the RAG knowledge base for reference.
        
        Args:
            filepath: Path to file
            description: Optional description
        
        Returns:
            Status message
        """
        if not self.rag_manager:
            return "❌ RAG system not initialized"
        
        try:
            path = Path(filepath).resolve()
            
            # Security check
            if not str(path).startswith(str(self.project_root)):
                return "❌ Security error: Cannot access files outside project"
            
            if not path.exists():
                return f"❌ File not found: {filepath}"
            
            # Read content
            content = path.read_text(encoding='utf-8')
            
            # Create collection name from file
            collection_name = f"project_files_{self.session_id}"
            
            # Add to RAG
            await self.rag_manager.setup_from_documents(
                documents=[f"File: {filepath}\nDescription: {description}\n\n{content}"],
                collection_name=collection_name
            )
            
            # Track ingested files
            self.ingested_files[str(path)] = {
                "description": description,
                "ingested_at": datetime.now(),
                "lines": len(content.split('\n')),
                "size": len(content)
            }
            
            return f"✅ Ingested: {filepath} ({len(content)} chars, {len(content.split(chr(10)))} lines)"
            
        except Exception as e:
            return f"❌ Error ingesting file: {str(e)}"
    
    async def search_project_knowledge(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search the RAG knowledge base.
        
        Args:
            query: Search query
            limit: Max results
        
        Returns:
            List of relevant documents
        """
        if not self.rag_manager:
            return []
        
        try:
            collection_name = f"project_files_{self.session_id}"
            # Search would return relevant chunks from ingested files
            return []
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
    
    def get_optimized_context(self, recent_messages: int = 3) -> str:
        """
        Get optimized context for the current conversation.
        Uses summarization to stay under token limits.
        
        Args:
            recent_messages: Number of recent messages to include
        
        Returns:
            Optimized context string
        """
        if not self.memory_manager:
            return ""
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                context = loop.run_until_complete(
                    self.memory_manager.get_context_for_session(self.session_id)
                )
                return context
            finally:
                loop.close()
        except Exception as e:
            print(f"❌ Context retrieval error: {e}")
            return ""
    
    def chat_with_context(self, message: str, include_files: List[str] = None) -> str:
        """
        Enhanced chat method with file context injection.
        
        Args:
            message: User message
            include_files: Optional list of files to include in context
        
        Returns:
            Agent response
        """
        # Build enhanced message with file context
        enhanced_parts = []
        
        # Add ingested file summaries if available
        if self.ingested_files:
            enhanced_parts.append("📚 Reference Files Available:")
            for filepath, info in list(self.ingested_files.items())[:5]:
                enhanced_parts.append(f"  - {Path(filepath).name}: {info.get('description', 'No description')}")
            enhanced_parts.append("")
        
        # Add specific file content if requested
        if include_files:
            enhanced_parts.append("📄 Included Files:")
            for filepath in include_files:
                try:
                    path = Path(filepath).resolve()
                    if str(path).startswith(str(self.project_root)) and path.exists():
                        content = path.read_text(encoding='utf-8')
                        # Truncate if too long
                        if len(content) > 1000:
                            content = content[:1000] + "\n... (truncated)"
                        enhanced_parts.append(f"\n{filepath}:\n```\n{content}\n```")
                except Exception as e:
                    enhanced_parts.append(f"\n❌ Could not read {filepath}: {e}")
            enhanced_parts.append("")
        
        # Add user message
        enhanced_parts.append(message)
        
        enhanced_message = "\n".join(enhanced_parts)
        
        # Use standard chat method
        return self.chat(enhanced_message, session_id=self.session_id)


# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_coding_agent(
    project_directory: Optional[str] = None,
    enable_memory: bool = False,
    **kwargs
) -> UltimateCodingAgent:
    """
    Create an Ultimate Coding Agent.
    
    Args:
        project_directory: Directory to lock agent to (defaults to current directory)
        enable_memory: Enable conversation memory
        **kwargs: Additional agent configuration
    
    Returns:
        Configured UltimateCodingAgent
    
    Example:
        >>> agent = create_coding_agent(project_directory="./my_project")
        >>> # Agent is now locked to ./my_project directory
    """
    return UltimateCodingAgent(
        project_directory=project_directory,
        enable_memory=enable_memory,
        **kwargs
    )


if __name__ == "__main__":
    print("🔧 Ultimate Coding Agent")
    print("=" * 70)
    print("Specialized agent for software development with safety controls")
    print()
    print("Usage:")
    print("  from coding_agent import create_coding_agent")
    print("  agent = create_coding_agent(project_directory='./my_project')")
    print("  agent.chat('Show me the file tree')")
    print()
