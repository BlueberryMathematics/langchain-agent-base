# Contributing to LangChain Agent Base

Thank you for your interest in contributing! This guide will help you get started with contributing to the LangChain Agent Base project.

## 🎯 Project Goals

The LangChain Agent Base aims to be:
- **Production-Ready**: Reliable, well-tested code for real applications
- **Easy to Use**: Simple imports and intuitive APIs
- **Extensible**: Easy to add new tools, agents, and features
- **Well-Documented**: Comprehensive guides and examples
- **Fast**: Optimized for performance with Groq integration

## 🤝 How to Contribute

### Types of Contributions

1. **🐛 Bug Reports**: Found an issue? Report it!
2. **✨ Feature Requests**: Have an idea? Suggest it!
3. **🔧 Tool Additions**: Add new tools for agents
4. **📚 Documentation**: Improve guides and examples
5. **🧪 Tests**: Add or improve test coverage
6. **🔄 Code Improvements**: Refactoring and optimizations

### Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/your-username/langchain-agent-base.git
   cd langchain-agent-base
   ```

2. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -e .  # Install in development mode
   
   # Install development dependencies
   pip install pytest black flake8 mypy
   ```