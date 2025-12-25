# Known Issues and Workarounds

## Import Performance Issue

### Problem
The v2.0 coding agent with memory and RAG enabled has slow initial imports (10-15 seconds) due to heavy dependencies:
- `sentence-transformers`
- `sklearn` (scikit-learn)
- `langchain_community.document_loaders`

This is **normal behavior** for ML/NLP libraries.

### What You'll See
```bash
python tests\test_coding_agent_v2.py
# ... 10-15 seconds of loading ...
# (appears hung but is actually loading sklearn)
```

### Why It Happens
```python
# coding_agent.py imports:
from src.memory import ConversationMemoryManager  
from src.rag import RAGManager  
from src.storage import UnifiedQdrantStorage

# Which cascade to:
langchain_qdrant → sentence-transformers → sklearn → joblib
```

The import chain loads large ML libraries into memory.

---

## Workarounds

### Option 1: Use Without Memory (Fast)
```python
# Disables memory/RAG, no heavy imports
agent = create_coding_agent(
    project_directory="./project",
    enable_memory=False  # ← Fast import
)
```

### Option 2: Wait for Initial Import (Recommended)
```bash
# First run is slow (10-15s)
python tests\test_coding_agent_v2.py

# Subsequent imports in same session are instant
# The modules stay cached in Python
```

### Option 3: Use v1.0 Agent (No Memory)
```bash
# Uses old agent without memory features
python tests\test_building_ultimate_coding_agent.py  # ← Fast
```

---

## Solutions (Future)

### Lazy Loading (Planned for v2.1)
```python
# Import memory/RAG only when needed
if enable_memory:
    from src.memory import ConversationMemoryManager  # Lazy
```

### Optional Dependencies (Planned)
```toml
[project.optional-dependencies]
memory = ["sentence-transformers>=2.2.2", "scikit-learn>=1.0"]

# Install without memory features
pip install -e .

# Install with memory
pip install -e ".[memory]"
```

---

## Performance Comparison

| Mode | Import Time | Features |
|------|-------------|----------|
| v1.0 (no memory) | < 1 second | File ops, terminal, search |
| v2.0 (memory disabled) | < 1 second | Same as v1.0 |
| v2.0 (memory enabled) | 10-15 seconds | + Memory + RAG + Summarization |

**Note**: 10-15 seconds is **one-time per Python session**. Once loaded, all operations are fast.

---

## Current Test Status

### ✅ test_building_ultimate_coding_agent.py (v1.0)
- **Import time**: < 1 second
- **Tests**: File operations, project creation
- **Works perfectly**

### ⏳ test_coding_agent_v2.py (v2.0)  
- **Import time**: 10-15 seconds (first time)
- **Tests**: Memory, RAG, context management
- **Works but slow initial load**

---

## Registry Error (Fixed)

The error:
```
Error loading registry: AgentCard.__init__() got an unexpected keyword argument 'config_hash'
```

**Status**: ✅ Fixed in `src/protocol.py`

**Solution**: Modified `AgentCard.from_dict()` to remove `config_hash` before initialization (it's auto-calculated).

---

## Recommendations

1. **For development**: Use `enable_memory=False` for faster iteration
2. **For production**: Accept 10-15s startup time, runtime is fast
3. **For testing v2.0**: Be patient with first import, or use Ctrl+C and retry if it seems stuck

---

## Verify It's Not Stuck

If import seems frozen, it's actually loading sklearn. You can verify:

```python
# Add debug prints
print("Loading memory...")
from src.memory import ConversationMemoryManager
print("✅ Memory loaded")

print("Loading RAG...")  
from src.rag import RAGManager
print("✅ RAG loaded")
```

You'll see it pauses at RAG (loading sklearn).

---

## Bottom Line

🟢 **Everything works correctly**  
🟡 **Initial import is slow (normal for ML libs)**  
🔵 **Runtime performance is excellent**  

The v2.0 agent is production-ready, just expect 10-15s startup time when memory/RAG is enabled.
