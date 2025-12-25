"""
Interactive CLI for Ultimate Coding Agent
==========================================

Provides a command-line interface with:
- User approval for all file operations
- Markdown code block parsing
- Intelligent code merging
- Safety controls
"""

import sys
import re
import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from coding_agent import create_coding_agent


class CodeBlockParser:
    """Parse code blocks from markdown responses."""
    
    @staticmethod
    def extract_code_blocks(text: str) -> List[Dict[str, str]]:
        """
        Extract code blocks from markdown text.
        
        Returns:
            List of dicts with 'language' and 'code' keys
        """
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        blocks = []
        for lang, code in matches:
            blocks.append({
                'language': lang or 'text',
                'code': code.strip()
            })
        
        return blocks
    
    @staticmethod
    def extract_file_list(text: str) -> List[str]:
        """
        Extract file list from agent response.
        Looks for patterns like "FILES: file1.py, file2.py"
        """
        # Pattern 1: FILES: file1, file2
        match = re.search(r'FILES?:\s*([^\n]+)', text, re.IGNORECASE)
        if match:
            files_str = match.group(1)
            files = [f.strip() for f in files_str.split(',')]
            return [f for f in files if f]
        
        # Pattern 2: List with - or *
        pattern = r'[-*]\s+`?([a-zA-Z0-9_./\\-]+\.py)`?'
        files = re.findall(pattern, text)
        if files:
            return files
        
        return []


class ApprovalSystem:
    """Handle user approval for agent actions."""
    
    @staticmethod
    def ask_approval(action: str, details: str) -> bool:
        """
        Ask user to approve an action.
        
        Args:
            action: Type of action (CREATE, EDIT, DELETE, TOOL)
            details: Details about the action
        
        Returns:
            True if approved, False if declined
        """
        print(f"\n{'='*70}")
        print(f"🔔 APPROVAL REQUIRED: {action}")
        print(f"{'='*70}")
        print(details)
        print(f"{'='*70}")
        
        while True:
            response = input("\n👉 Approve this action? [y/n/q]: ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                print("❌ Action declined.")
                return False
            elif response in ['q', 'quit']:
                print("🛑 Quitting...")
                sys.exit(0)
            else:
                print("Please enter 'y' for yes, 'n' for no, or 'q' to quit.")
    
    @staticmethod
    def show_diff(filepath: str, old_content: str, new_content: str):
        """Show a simple diff between old and new content."""
        print("\n📊 Changes:")
        print(f"File: {filepath}")
        print("-" * 60)
        
        old_lines = old_content.split('\n')
        new_lines = new_content.split('\n')
        
        # Simple line-by-line comparison
        max_lines = max(len(old_lines), len(new_lines))
        
        for i in range(min(max_lines, 20)):  # Show first 20 lines
            old_line = old_lines[i] if i < len(old_lines) else ""
            new_line = new_lines[i] if i < len(new_lines) else ""
            
            if old_line != new_line:
                if old_line:
                    print(f"- {old_line}")
                if new_line:
                    print(f"+ {new_line}")
        
        if max_lines > 20:
            print(f"... ({max_lines - 20} more lines)")
        print("-" * 60)


class FileOperations:
    """Handle actual file operations with approval."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.approval_system = ApprovalSystem()
    
    def create_file(self, filepath: str, content: str) -> bool:
        """Create a new file with user approval."""
        path = Path(filepath).resolve()
        
        # Security check
        if not str(path).startswith(str(self.project_root)):
            print(f"❌ Security error: Cannot create files outside project")
            return False
        
        if path.exists():
            print(f"❌ Error: File already exists: {filepath}")
            return False
        
        # Get approval
        details = f"""
📝 Create new file: {filepath}
Lines: {len(content.split(chr(10)))}
Size: {len(content)} characters

Preview:
{'-'*60}
{content[:500]}{'...' if len(content) > 500 else ''}
{'-'*60}
"""
        
        if not self.approval_system.ask_approval("CREATE FILE", details):
            return False
        
        # Create file
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
            print(f"✅ Created: {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error creating file: {e}")
            return False
    
    def edit_file(self, filepath: str, new_content: str) -> bool:
        """Edit an existing file with user approval."""
        path = Path(filepath).resolve()
        
        # Security check
        if not str(path).startswith(str(self.project_root)):
            print(f"❌ Security error: Cannot edit files outside project")
            return False
        
        if not path.exists():
            print(f"❌ Error: File not found: {filepath}")
            return False
        
        # Read current content
        try:
            old_content = path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return False
        
        # Show diff and get approval
        self.approval_system.show_diff(filepath, old_content, new_content)
        
        if not self.approval_system.ask_approval("EDIT FILE", f"Apply changes to {filepath}?"):
            return False
        
        # Write new content
        try:
            path.write_text(new_content, encoding='utf-8')
            print(f"✅ Edited: {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error writing file: {e}")
            return False
    
    def delete_file(self, filepath: str) -> bool:
        """Delete a file with user approval."""
        path = Path(filepath).resolve()
        
        # Security check
        if not str(path).startswith(str(self.project_root)):
            print(f"❌ Security error: Cannot delete files outside project")
            return False
        
        if not path.exists():
            print(f"❌ Error: File not found: {filepath}")
            return False
        
        # Get approval
        size = path.stat().st_size
        details = f"""
🗑️  Delete file: {filepath}
Size: {size} bytes

⚠️  This action cannot be undone!
"""
        
        if not self.approval_system.ask_approval("DELETE FILE", details):
            return False
        
        # Delete file
        try:
            path.unlink()
            print(f"✅ Deleted: {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error deleting file: {e}")
            return False


class CodingAgentCLI:
    """Interactive CLI for the coding agent with memory and RAG support."""
    
    def __init__(self, project_directory: str, enable_memory: bool = True, session_id: str = None):
        self.project_root = Path(project_directory).resolve()
        
        # Change to project directory
        os.chdir(self.project_root)
        
        # Generate session ID if not provided
        if not session_id:
            from datetime import datetime
            session_id = f"coding_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.session_id = session_id
        
        # Initialize agent
        print("🚀 Initializing Ultimate Coding Agent...")
        print(f"📝 Session ID: {session_id}")
        
        self.agent = create_coding_agent(
            project_directory=str(self.project_root),
            enable_memory=enable_memory,
            session_id=session_id,
            max_context_tokens=2000
        )
        
        self.parser = CodeBlockParser()
        self.file_ops = FileOperations(self.project_root)
        self.approval_system = ApprovalSystem()
        self.reference_files: List[str] = []
    
    def run(self):
        """Run the interactive CLI."""
        print("\n" + "="*70)
        print("🎯 ULTIMATE CODING AGENT - Interactive Mode v2.0")
        print("="*70)
        print(f"📁 Project: {self.project_root.name}")
        print(f"🔒 Locked to: {self.project_root}")
        print(f"📝 Session: {self.session_id}")
        print(f"🧠 Memory: {'Enabled' if self.agent.memory_manager else 'Disabled'}")
        print("\nCommands:")
        print("  - Type your request naturally")
        print("  - 'tree' - Show file structure")
        print("  - 'upload <filepath>' - Add reference file to knowledge base")
        print("  - 'references' - List uploaded reference files")
        print("  - 'summary' - Get conversation summary")
        print("  - 'context' - Show current context size")
        print("  - 'quit' or 'exit' - Exit the CLI")
        print("  - All file operations require approval")
        print("="*70 + "\n")
        
        while True:
            try:
                # Get user input
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'tree':
                    user_input = "Show me the file tree"
                
                elif user_input.lower().startswith('upload '):
                    filepath = user_input[7:].strip()
                    self.upload_reference_file(filepath)
                    continue
                
                elif user_input.lower() == 'references':
                    self.show_references()
                    continue
                
                elif user_input.lower() == 'summary':
                    self.show_summary()
                    continue
                
                elif user_input.lower() == 'context':
                    self.show_context_info()
                    continue
                
                # Send to agent with context
                print("\n🤖 Agent: ", end="", flush=True)
                
                # Use enhanced chat if we have reference files
                if self.reference_files:
                    response = self.agent.chat_with_context(
                        user_input,
                        include_files=self.reference_files[-3:]  # Include last 3 references
                    )
                else:
                    response = self.agent.chat(user_input, session_id=self.session_id)
                
                print(response)
                
                # Parse response for file operations
                self.process_response(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    def process_response(self, response: str):
        """Process agent response for code blocks and file operations."""
        
        # Extract code blocks
        code_blocks = self.parser.extract_code_blocks(response)
        
        if not code_blocks:
            return
        
        # Extract file list if mentioned
        files = self.parser.extract_file_list(response)
        
        # If we have code blocks and files, offer to apply changes
        if code_blocks and files:
            print(f"\n📝 Found {len(code_blocks)} code block(s) for {len(files)} file(s)")
            
            # Match code blocks to files
            for i, filepath in enumerate(files):
                if i < len(code_blocks):
                    code_block = code_blocks[i]
                    self.apply_code_to_file(filepath, code_block['code'])
        
        elif code_blocks:
            # Ask user which file to apply to
            print(f"\n📝 Found {len(code_blocks)} code block(s)")
            print("Which file should these changes apply to?")
            filepath = input("📄 File path: ").strip()
            
            if filepath:
                # Combine all code blocks
                combined_code = "\n\n".join(block['code'] for block in code_blocks)
                self.apply_code_to_file(filepath, combined_code)
    
    def apply_code_to_file(self, filepath: str, code: str):
        """Apply code to a file (create or edit)."""
        path = Path(filepath)
        
        if path.exists():
            # Edit existing file
            self.file_ops.edit_file(filepath, code)
        else:
            # Create new file
            self.file_ops.create_file(filepath, code)
    
    def upload_reference_file(self, filepath: str):
        """Upload a reference file to the RAG knowledge base."""
        try:
            path = Path(filepath).resolve()
            
            # Security check
            if not str(path).startswith(str(self.project_root)):
                print("❌ Error: Can only upload files from project directory")
                return
            
            if not path.exists():
                print(f"❌ Error: File not found: {filepath}")
                return
            
            # Get description
            description = input(f"📝 Description for {path.name} (optional): ").strip()
            
            # Ingest file using agent's async method
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    self.agent.ingest_file_for_reference(str(path), description)
                )
                print(result)
                
                if "✅" in result:
                    self.reference_files.append(str(path))
                    print(f"📚 Reference file added. Total: {len(self.reference_files)}")
            finally:
                loop.close()
                
        except Exception as e:
            print(f"❌ Error uploading file: {e}")
    
    def show_references(self):
        """Show all uploaded reference files."""
        if not self.reference_files:
            print("📚 No reference files uploaded yet.")
            print("   Use 'upload <filepath>' to add files to the knowledge base")
            return
        
        print("\n📚 Reference Files:")
        print("="*60)
        for i, filepath in enumerate(self.reference_files, 1):
            path = Path(filepath)
            info = self.agent.ingested_files.get(filepath, {})
            print(f"{i}. {path.name}")
            print(f"   Path: {filepath}")
            if info.get('description'):
                print(f"   Description: {info['description']}")
            print(f"   Size: {info.get('size', 'Unknown')} chars, {info.get('lines', 'Unknown')} lines")
        print("="*60)
    
    def show_summary(self):
        """Show conversation summary."""
        if not self.agent.memory_manager:
            print("⚠️  Memory not enabled. No summary available.")
            return
        
        try:
            # Get session info
            session = self.agent.memory_manager.active_sessions.get(self.session_id, {})
            message_count = len(session.get("messages", []))
            token_count = session.get("token_count", 0)
            
            print("\n📊 Conversation Summary:")
            print("="*60)
            print(f"Session: {self.session_id}")
            print(f"Messages: {message_count}")
            print(f"Estimated tokens: {int(token_count)}")
            print(f"Max context: {self.agent.max_context_tokens} tokens")
            
            if token_count > self.agent.max_context_tokens * 0.7:
                print("\n⚠️  Approaching context limit. Auto-summarization will trigger soon.")
            
            print("="*60)
            
        except Exception as e:
            print(f"❌ Error getting summary: {e}")
    
    def show_context_info(self):
        """Show context information."""
        if not self.agent.memory_manager:
            print("⚠️  Memory not enabled.")
            return
        
        try:
            session = self.agent.memory_manager.active_sessions.get(self.session_id, {})
            token_count = session.get("token_count", 0)
            max_tokens = self.agent.max_context_tokens
            
            print("\n📐 Context Information:")
            print("="*60)
            print(f"Current tokens: {int(token_count)} / {max_tokens}")
            
            # Calculate percentage
            percentage = (token_count / max_tokens) * 100
            bar_length = 40
            filled = int(bar_length * percentage / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            print(f"Usage: [{bar}] {percentage:.1f}%")
            
            if percentage > 70:
                print("\n⚠️  Context usage high. Consider:")
                print("   - Agent will auto-summarize to compress context")
                print("   - Older messages will be summarized")
                print("   - Recent messages always preserved")
            
            print("="*60)
            
        except Exception as e:
            print(f"❌ Error getting context info: {e}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Ultimate Coding Agent CLI v2.0 - Memory & RAG Enabled",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py ./my_project                    # Start with memory enabled
  python cli.py ./my_project --no-memory        # Start without memory
  python cli.py ./my_project --session my_sess  # Custom session ID
        """
    )
    
    parser.add_argument(
        "project_dir",
        nargs="?",
        default=None,
        help="Project directory path (default: current directory)"
    )
    
    parser.add_argument(
        "--no-memory",
        action="store_true",
        help="Disable memory and RAG features"
    )
    
    parser.add_argument(
        "--session",
        type=str,
        default=None,
        help="Custom session ID for memory tracking"
    )
    
    args = parser.parse_args()
    
    # Get project directory
    if args.project_dir:
        project_dir = args.project_dir
    else:
        project_dir = input("📁 Enter project directory path (. for current): ").strip()
        if not project_dir:
            project_dir = "."
    
    project_path = Path(project_dir).resolve()
    
    if not project_path.exists():
        print(f"❌ Error: Directory does not exist: {project_dir}")
        sys.exit(1)
    
    if not project_path.is_dir():
        print(f"❌ Error: Path is not a directory: {project_dir}")
        sys.exit(1)
    
    # Start CLI
    enable_memory = not args.no_memory
    cli = CodingAgentCLI(
        str(project_path),
        enable_memory=enable_memory,
        session_id=args.session
    )
    cli.run()


if __name__ == "__main__":
    main()
