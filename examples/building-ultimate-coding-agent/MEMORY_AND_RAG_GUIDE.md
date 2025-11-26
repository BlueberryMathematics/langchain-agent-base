# Ultimate Coding Agent v2.0 - Memory & RAG Guide

## 🎯 **Overview**

Version 2.0 of the Ultimate Coding Agent introduces powerful memory management, RAG (Retrieval-Augmented Generation), and intelligent context handling to maintain effective performance within token limits.

## ✨ **New Features**

### 1. **Conversation Memory**
- Persistent conversation history across sessions
- Automatic summarization when approaching token limits
- Smart context retrieval for relevant information
- Session-based tracking

### 2. **RAG Knowledge Base**
- Upload reference files to the knowledge base
- Semantic search across ingested files
- Use reference documentation while coding
- Context-aware file suggestions

### 3. **Context Management**
- Optimized for 2000 token context windows (configurable)
- Automatic summarization at 70% threshold (1400 tokens)
- Recent messages always preserved
- Intelligent context compression

### 4. **File Upload System**
- Add reference files from project directory
- Describe file purpose for better retrieval
- Track all uploaded references
- Automatically include recent references in context

---

## 🚀 **Getting Started**

### **Basic Usage**

```bash
# Start with memory enabled (default)
python cli.py ./my_project

# Start without memory
python cli.py ./my_project --no-memory

# Custom session ID
python cli.py ./my_project --session my_coding_session
```

### **Interactive Commands**

```
tree              - Show file structure
upload <file>     - Upload reference file to knowledge base
references        - List all uploaded reference files
summary           - Show conversation statistics
context           - View context usage and limits
quit/exit         - Exit the CLI
```

---

## 📚 **Memory System Details**

### **How It Works**

1. **Message Storage**: All conversations stored in Qdrant vector database
2. **Token Tracking**: Estimates token usage (words × 1.3)
3. **Auto-Summarization**: Triggered at 70% of max context (default: 1400/2000 tokens)
4. **Smart Retrieval**: Uses semantic search to find relevant past messages

### **Summarization Process**

When token limit is approached:

```
[Before Summarization]
Message 1: "Create a user authentication system"
Message 2: "Add password hashing"
Message 3: "Include JWT tokens"
Message 4: "Add email verification"
Message 5: "Implement 2FA"
... (20 more messages)

[After Summarization]
Summary: "Created authentication system with password hashing, 
JWT tokens, email verification, and 2FA support."
Message 24: "Now add OAuth integration"
Message 25: "Support Google and GitHub"
```

**Benefits:**
- Reduces token usage by 60-70%
- Preserves key information
- Maintains searchability
- Keeps recent context intact

### **Configuration Options**

```python
agent = create_coding_agent(
    project_directory="./my_project",
    enable_memory=True,
    session_id="my_session",
    max_context_tokens=2000,  # Adjust based on needs
)
```

---

## 🔍 **RAG System Details**

### **File Upload Workflow**

```bash
# In CLI
You: upload ./docs/api_reference.md
📝 Description for api_reference.md (optional): API documentation for project
✅ Ingested: ./docs/api_reference.md (15234 chars, 456 lines)
📚 Reference file added. Total: 1
```

### **How RAG Enhances Coding**

**Without RAG:**
```
You: "Create an API endpoint for user registration"
Agent: [Generic implementation without project context]
```

**With RAG:**
```
You: upload ./docs/api_spec.md
You: upload ./src/auth/user.py
You: "Create an API endpoint for user registration"
Agent: [Uses uploaded API spec and existing user model for accurate implementation]
```

### **What Gets Ingested**

- Source code files
- Documentation (Markdown, text)
- Configuration files
- Any text-based reference material

### **Programmatic Usage**

```python
import asyncio

# Ingest a file
result = asyncio.run(
    agent.ingest_file_for_reference(
        "./docs/architecture.md",
        description="System architecture documentation"
    )
)

# Search knowledge base
results = asyncio.run(
    agent.search_project_knowledge("authentication flow", limit=5)
)
```

---

## ⚙️ **Context Management**

### **Token Budget Strategy**

For a 2000 token context window:

```
Total: 2000 tokens
├─ System Prompt: ~300 tokens (15%)
├─ Recent Messages: ~700 tokens (35%)
├─ Reference Files: ~500 tokens (25%)
├─ Summarized History: ~400 tokens (20%)
└─ User Query: ~100 tokens (5%)
```

### **Automatic Optimization**

**At 70% Usage (1400 tokens):**
- Oldest 50% of messages summarized
- Summary stored in knowledge base
- Token usage reduced to ~50%

**At 90% Usage (1800 tokens):**
- Additional compression triggered
- Only last 3 messages kept
- Critical information preserved in summaries

### **Manual Context Control**

```python
# Get optimized context
context = agent.get_optimized_context(recent_messages=3)

# Chat with specific file context
response = agent.chat_with_context(
    "Implement feature X",
    include_files=["./src/base.py", "./docs/spec.md"]
)
```

---

## 🔧 **Advanced Features**

### **1. Multi-File Context Injection**

```python
# Include specific files in query context
response = agent.chat_with_context(
    message="Refactor the authentication module",
    include_files=[
        "./src/auth/login.py",
        "./src/auth/register.py",
        "./docs/security.md"
    ]
)
```

**Automatic Truncation:**
- Files over 1000 chars truncated with "... (truncated)"
- Prevents context overflow
- Preserves essential information

### **2. Session Management**

```python
# Create multiple sessions for different projects
session_1 = "frontend_development"
session_2 = "backend_api"
session_3 = "database_migration"

# Each session maintains separate:
# - Conversation history
# - Token tracking
# - Reference files
# - Summaries
```

### **3. Memory Search**

```python
import asyncio

# Search past conversations
results = asyncio.run(
    agent.memory_manager.search_memory(
        query="authentication implementation",
        session_id="my_session",
        limit=10
    )
)

for result in results:
    print(f"[{result['timestamp']}] {result['message']}")
```

---

## 📊 **Monitoring & Debugging**

### **Context Usage Visualization**

```bash
You: context

📐 Context Information:
============================================================
Current tokens: 1247 / 2000
Usage: [████████████████████░░░░░░░░░░░░░░░░░░░░] 62.4%
============================================================
```

### **Conversation Statistics**

```bash
You: summary

📊 Conversation Summary:
============================================================
Session: coding_20251126_143022
Messages: 42
Estimated tokens: 1247
Max context: 2000 tokens
============================================================
```

### **Reference File Tracking**

```bash
You: references

📚 Reference Files:
============================================================
1. api_reference.md
   Path: ./docs/api_reference.md
   Description: API documentation for project
   Size: 15234 chars, 456 lines

2. user.py
   Path: ./src/auth/user.py
   Description: User model implementation
   Size: 3421 chars, 127 lines
============================================================
```

---

## 🎓 **Best Practices**

### **1. Upload Reference Files Early**

```bash
# At start of session
You: upload ./README.md
You: upload ./docs/architecture.md
You: upload ./src/config.py

# Then ask questions
You: "Create a new service following the project architecture"
```

### **2. Use Descriptive File Descriptions**

```bash
# ❌ Bad
You: upload ./utils.py
Description: utils

# ✅ Good
You: upload ./utils.py
Description: Helper functions for data validation and formatting
```

### **3. Monitor Context Usage**

```bash
# Check before large requests
You: context
[Usage: 85%]

# If high, summarization is coming
# Consider starting new focused session
```

### **4. Leverage Session IDs**

```bash
# Organize work by feature/task
python cli.py ./project --session user_auth_feature
python cli.py ./project --session api_refactoring
python cli.py ./project --session bug_fix_123
```

### **5. Reference Recent Files**

The agent automatically includes last 3 uploaded files in context. For specific needs:

```python
response = agent.chat_with_context(
    "Implement the feature",
    include_files=["./specific/file.py"]
)
```

---

## 🐛 **Troubleshooting**

### **Memory Not Working**

```bash
# Check if Qdrant is running
docker ps | grep qdrant

# Start Qdrant if needed
docker run -d -p 6333:6333 -p 6334:6334 --name qdrant qdrant/qdrant

# Or use without memory
python cli.py ./project --no-memory
```

### **Context Overflow**

If you see "context too large" errors:

```python
# Reduce max context
agent = create_coding_agent(
    max_context_tokens=1500  # Smaller window
)

# Or enable aggressive summarization
memory_manager = ConversationMemoryManager(
    summarization_threshold=1000  # Trigger earlier
)
```

### **RAG Search Not Finding Files**

```bash
# Ensure files are uploaded
You: references

# Re-upload if needed
You: upload ./path/to/file.py
```

---

## 🔒 **Security Notes**

### **File Access Restrictions**

```python
# ✅ Allowed - within project
upload ./src/module.py

# ❌ Blocked - outside project
upload ../../sensitive/file.py
# Error: Can only upload files from project directory
```

### **Memory Storage**

- All conversations stored in Qdrant
- Local storage by default (`:memory:` or file-based)
- For persistent storage across restarts, use external Qdrant server

---

## 📈 **Performance Tips**

### **Optimal Token Usage**

```
✅ Good: 1200-1400 tokens (60-70%)
⚠️  High: 1600-1800 tokens (80-90%)
❌ Critical: 1900+ tokens (95%+)
```

### **File Size Guidelines**

```
✅ Optimal: < 1000 chars per file
⚠️  Large: 1000-5000 chars (will truncate)
❌ Too Large: > 5000 chars (consider splitting)
```

### **Message Length**

```
✅ Concise queries: 50-200 tokens
⚠️  Detailed requests: 200-500 tokens
❌ Very long: > 500 tokens (break into steps)
```

---

## 🚀 **Migration from v1.0**

### **Updating Existing Code**

```python
# v1.0
agent = create_coding_agent(
    project_directory="./project",
    enable_memory=False
)

# v2.0
agent = create_coding_agent(
    project_directory="./project",
    enable_memory=True,        # NEW
    session_id="my_session",   # NEW
    max_context_tokens=2000    # NEW
)
```

### **New CLI Features**

```bash
# v1.0 commands still work
tree
quit

# v2.0 new commands
upload <file>    # NEW
references       # NEW
summary          # NEW
context          # NEW
```

---

## 📚 **API Reference**

### **Agent Methods**

```python
# File ingestion
await agent.ingest_file_for_reference(filepath, description)

# Knowledge search
await agent.search_project_knowledge(query, limit)

# Context management
context = agent.get_optimized_context(recent_messages=3)

# Enhanced chat
response = agent.chat_with_context(message, include_files)
```

### **Memory Manager Methods**

```python
# Add message
await memory_manager.add_message(session_id, message, response)

# Search memory
results = await memory_manager.search_memory(query, session_id)

# Get context
context = await memory_manager.get_context_for_session(session_id)
```

---

## 💡 **Example Workflow**

### **Building a New Feature**

```bash
# 1. Start session
python cli.py ./project --session user_profile_feature

# 2. Upload references
You: upload ./docs/user_model.md
You: upload ./src/models/base.py

# 3. Start building
You: "Create a user profile model based on the uploaded docs"

# 4. Continue with context
You: "Add profile picture upload functionality"

# 5. Monitor progress
You: summary
You: context

# 6. Reference specific files
You: "Refactor following the patterns in base.py"
```

---

## 🤝 **Contributing**

To extend memory/RAG features:

1. Enhance summarization algorithms in `src/memory.py`
2. Add custom RAG retrievers in `src/rag.py`
3. Implement new context strategies in `coding_agent.py`

---

## 📖 **Related Documentation**

- [README.md](README.md) - Main documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick reference
- [../../docs/memory-and-rag.md](../../docs/memory-and-rag.md) - Framework memory docs

---

**Version**: 2.0.0  
**Last Updated**: November 26, 2025  
**Status**: Production Ready
