# LangChain Agent Base Documentation

Welcome to the comprehensive documentation for LangChain Agent Base - the ultimate import library for AI agents powered by Groq's blazing-fast `gpt-oss-120b` model.

## 📚 Documentation Structure

### 🚀 **Getting Started**
**[Getting Started Guide](getting-started.md)** - Installation, setup, and first steps
- Quick installation options
- Your first agent in 30 seconds  
- Adding capabilities and tools
- Commands for direct execution
- Multi-agent systems
- Human-in-the-loop workflows

### 📖 **Core Documentation**

#### **[API Reference](api-reference.md)** - Complete class and method documentation
- **Core Classes**: Agent, HITLAgent with all methods
- **Factory Functions**: Pre-configured specialist agents
- **Tool Collections**: Math, science, coding tools
- **RAG System**: Document indexing and retrieval
- **Command System**: Direct tool execution
- **Error Handling**: Exception types and handling

#### **[Tool Collections](tool-collections.md)** - All available tools organized by domain
- **🧮 Math Tools**: Calculator, equations, matrices
- **🔬 Science Tools**: Unit conversion, chemistry, physics  
- **💻 Coding Tools**: Code analysis, regex, JSON formatting
- **🌍 Basic Tools**: Weather, general utilities
- **📚 RAG Tools**: Document search and retrieval
- **🛠️ Custom Tools**: How to create your own

#### **[Advanced Usage](advanced-usage.md)** - Sophisticated patterns and techniques
- **🤖 Multi-Agent Systems**: Coordination and delegation
- **🛡️ Human-in-the-Loop**: Approval workflows
- **📚 Advanced RAG**: Multi-collection and hierarchical search
- **⚡ Command Systems**: Batch processing and automation
- **🔧 Custom Architectures**: ReAct, Chain-of-Thought patterns
- **📊 Performance Optimization**: Caching, async operations

#### **[Examples](examples.md)** - Real-world application patterns
- **🏢 Business Applications**: Customer support, sales analytics, HR
- **🔬 Technical Applications**: Code review, monitoring, databases
- **🎓 Educational Applications**: Math tutoring, science labs
- **🔄 Integration Patterns**: APIs, workflow automation

#### **[Contributing](contributing.md)** - How to extend and improve the project
- **🔧 Adding Tools**: Step-by-step tool creation guide
- **🤖 Agent Types**: Creating specialized agent classes
- **📝 Documentation**: Writing guides and examples
- **🧪 Testing**: Test requirements and coverage
- **🎨 Code Style**: Formatting and quality standards

## 🎯 **Quick Navigation**

### By Use Case

| **Use Case** | **Start Here** | **Advanced Topics** |
|-------------|----------------|-------------------|
| **New to the library** | [Getting Started](getting-started.md) | [Examples](examples.md) |
| **Building agents** | [API Reference](api-reference.md) | [Advanced Usage](advanced-usage.md) |
| **Adding tools** | [Tool Collections](tool-collections.md) | [Contributing](contributing.md) |
| **Real applications** | [Examples](examples.md) | [Advanced Usage](advanced-usage.md) |
| **Contributing** | [Contributing](contributing.md) | [API Reference](api-reference.md) |

### By Experience Level

#### **Beginner** (New to AI agents)
1. **[Getting Started](getting-started.md)** - Learn the basics
2. **[Examples](examples.md)** - See real applications  
3. **[Tool Collections](tool-collections.md)** - Discover available capabilities

#### **Intermediate** (Building applications)
1. **[API Reference](api-reference.md)** - Master the classes and methods
2. **[Advanced Usage](advanced-usage.md)** - Learn sophisticated patterns
3. **[Examples](examples.md)** - Study production patterns

#### **Advanced** (Extending the system)
1. **[Contributing](contributing.md)** - Add new features
2. **[Advanced Usage](advanced-usage.md)** - Custom architectures
3. **[API Reference](api-reference.md)** - Deep system understanding

## 🔍 **Quick Reference**

### Essential Imports
```python
# Core classes
from src.base import Agent, HITLAgent

# Specialized agents
from src.base import create_math_agent, create_science_agent, create_coding_agent

# Tool collections  
from src.tools import get_math_tools, get_science_tools, get_coding_tools

# RAG system
from src.rag import RAGManager, setup_rag_tools

# Commands
from src.commands import CommandRegistry, command
```

### Common Patterns
```python
# Basic agent
agent = Agent()
response = agent.chat("Hello!")

# Specialist agent
math_agent = create_math_agent()
result = math_agent.chat("Solve x² + 5x + 6 = 0")

# Agent with tools
agent = Agent()
agent.add_tools(get_math_tools())
agent.enable_commands()

# RAG agent
rag_agent = await create_rag_agent(documents=["doc1.txt", "doc2.txt"])

# HITL agent
hitl_agent = HITLAgent(interrupt_tools=["dangerous_tool"])
```

## 📋 **Feature Matrix**

| **Feature** | **Basic Agent** | **Specialist Agents** | **RAG Agent** | **HITL Agent** | **Multi-Agent** |
|------------|----------------|---------------------|---------------|----------------|-----------------|
| **Chat Interface** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Custom Tools** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Pre-configured Tools** | ➖ | ✅ | ➖ | ➖ | ✅ |
| **Document Search** | ➖ | ➖ | ✅ | ➖ | ✅ |
| **Approval Workflows** | ➖ | ➖ | ➖ | ✅ | ✅ |
| **Command System** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Agent Coordination** | ➖ | ➖ | ➖ | ➖ | ✅ |

## 🛠️ **Development Workflow**

### For New Users
1. **Installation**: Follow [Getting Started](getting-started.md#installation)
2. **First Agent**: Create your [first agent](getting-started.md#your-first-agent-30-seconds)
3. **Add Capabilities**: Explore [tool collections](tool-collections.md)
4. **Real Examples**: Study [application examples](examples.md)

### For Developers  
1. **API Mastery**: Study [API Reference](api-reference.md)
2. **Advanced Patterns**: Learn [advanced usage](advanced-usage.md)
3. **Custom Tools**: Create tools following [contributing guide](contributing.md)
4. **Testing**: Add tests per [testing guidelines](contributing.md#testing)

### For Contributors
1. **Setup**: Follow [development setup](contributing.md#getting-started)
2. **Guidelines**: Read [code style](contributing.md#code-style) and [architecture](contributing.md#architecture-guidelines)  
3. **Testing**: Ensure [test coverage](contributing.md#test-coverage-guidelines)
4. **Documentation**: Update relevant [documentation](contributing.md#documentation-guidelines)

## 🔗 **External Resources**

### Core Technologies
- **[LangChain Documentation](https://python.langchain.com/)** - Framework fundamentals
- **[Groq Documentation](https://console.groq.com/docs)** - Model API details
- **[HuggingFace Transformers](https://huggingface.co/docs/transformers)** - Embedding models

### Community
- **[GitHub Repository](https://github.com/your-repo/langchain-agent-base)** - Source code and issues
- **[GitHub Discussions](https://github.com/your-repo/langchain-agent-base/discussions)** - Community Q&A
- **[Example Projects](examples.md)** - Real-world implementations

## 🆘 **Need Help?**

### Common Issues
- **Installation Problems**: Check [getting started requirements](getting-started.md#installation)
- **API Key Issues**: Verify [environment setup](getting-started.md#installation)
- **Import Errors**: Review [project structure](getting-started.md#installation)
- **Tool Problems**: Consult [tool collections guide](tool-collections.md)

### Support Channels
1. **Documentation**: Search these guides first
2. **Examples**: Check [real-world patterns](examples.md)
3. **GitHub Issues**: Report bugs and request features
4. **GitHub Discussions**: Ask questions and get community help

### Quick Troubleshooting
```python
# Verify installation
from src.base import Agent
agent = Agent()
print("✅ Installation working!")

# Check API key
import os
print("GROQ_API_KEY set:", bool(os.getenv("GROQ_API_KEY")))

# Test basic functionality  
response = agent.chat("Hello!")
print("✅ Agent responding:", response)
```

---

## 🎉 **Welcome to LangChain Agent Base!**

Whether you're building your first AI agent or scaling a production system, this documentation provides everything you need. Start with [Getting Started](getting-started.md) and explore from there.

**Happy building! 🚀**

---

*Last updated: January 2024 | [Edit this page](https://github.com/your-repo/langchain-agent-base/edit/main/docs/README.md)*