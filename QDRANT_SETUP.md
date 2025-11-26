# Enable Memory in Math Discovery Agent

To enable persistent conversation memory across sessions, you need a Qdrant server running on `localhost:6333`.

## Option 1: Download Qdrant Binary (Recommended)

### Windows:
1. Download the latest Qdrant release from: https://github.com/qdrant/qdrant/releases
2. Extract the zip file
3. Run: `.\qdrant.exe`

The server will start on `http://localhost:6333`

## Option 2: Use Python Local Storage (Simpler, but limited)

The RAG system already uses local Qdrant storage (`:memory:` or file-based), which is sufficient for the knowledge base.

**For your math discovery use case, you don't need external memory** - the RAG knowledge base stores all your formulas and discoveries.

## What Each System Does

- **RAG (Knowledge Base)**: ✅ Already working with in-memory Qdrant
  - Stores mathematical formulas
  - Stores discoveries
  - Enables semantic search
  - **This is what you need for math research**

- **Memory (Conversations)**: Requires external server
  - Stores chat history
  - Remembers context across sessions
  - Optional for your use case

## Current Status

Your agent works perfectly with:
```python
agent = create_math_discovery_agent(
    enable_memory=False  # ✅ This is fine for math discovery
)
```

If you want conversation memory, download the Qdrant binary and run it, then set `enable_memory=True`.
