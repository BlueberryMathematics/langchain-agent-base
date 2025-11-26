# Calculator Project

A simple, elegant calculator built with HTML, CSS, and JavaScript.

## 🎯 Overview

This project demonstrates a functional calculator application built entirely with:
- **HTML** - Structure and layout
- **Embedded CSS** - Modern, clean styling with hover effects
- **Embedded JavaScript** - Calculator logic and keyboard support

## 📁 Project Structure

```
test_coding_project_2/
├── README.md              # Project documentation (this file)
└── calculator/
    └── index.html         # Complete calculator application
```

## ✨ Features

- **Basic Arithmetic Operations**: `+`, `-`, `*`, `/`
- **Parentheses Support**: `(` and `)` for complex expressions
- **Decimal Numbers**: Full decimal point support
- **Keyboard Input**: Type directly or use mouse
- **Error Handling**: Displays "Error" for invalid expressions
- **Clean UI**: Modern design with soft colors and hover effects
- **Responsive**: Clean layout that works on different screen sizes

## 🚀 How to Use

### Option 1: Open Directly
1. Navigate to the `calculator/` folder
2. Double-click `index.html`
3. Calculator opens in your default browser

### Option 2: Use Local Server
```bash
cd calculator
python -m http.server 8000
```
Then visit: `http://localhost:8000`

## 🎮 Controls

### Mouse
- Click number buttons (0-9)
- Click operators (+, -, *, /)
- Click `=` to calculate result
- Click `C` to clear

### Keyboard
- **Numbers**: Type `0-9`
- **Operators**: Type `+`, `-`, `*`, `/`
- **Parentheses**: Type `(` or `)`
- **Decimal**: Type `.`
- **Calculate**: Press `Enter`
- **Clear**: Press `Escape`
- **Backspace**: Press `Backspace` to delete last character

## 🎨 Design

The calculator features:
- **Light theme** with soft blue/gray background
- **Card-based design** with shadow for depth
- **Color-coded buttons**:
  - Blue: Numbers
  - Orange: Operators
  - Green: Equals button
  - Red: Clear button
- **Hover effects** for better interactivity
- **Large, readable display** with right-aligned text

## 🔧 Technical Details

### Expression Evaluation
The calculator uses the `Function` constructor for safe expression evaluation:
```javascript
const result = Function(`'use strict'; return (${expression})`)();
```

This is safer than `eval()` and allows:
- Complex arithmetic expressions
- Parentheses for order of operations
- Proper operator precedence

### Input Sanitization
Multiple consecutive operators are automatically cleaned:
```javascript
const sanitized = expression.replace(/([+\-*/]){2,}/g, '$1');
```

### Error Handling
All invalid expressions display "Error" instead of crashing:
```javascript
try {
  // Evaluate expression
} catch (e) {
  display.value = 'Error';
}
```

## 🛠️ Built With

This project was created using the **Ultimate Coding Agent v2.0**:
- **Project**: [langchain-agent-base](https://github.com/BlueberryMathematician/langchain-agent-base)
- **Agent**: Ultimate Coding Agent with memory, RAG, and safety controls
- **Features Used**:
  - Project directory locking (security)
  - User approval workflow
  - Code block parsing from agent responses
  - Intelligent file creation

### About the Coding Agent

The Ultimate Coding Agent is an AI-powered development assistant that:
- 🔒 Works within a locked project directory (cannot access files outside)
- 👥 Requires approval for all file operations
- 🧠 Has conversation memory and RAG for context
- 📝 Generates only the code changes needed
- 💻 Can execute safe terminal commands
- 🔍 Searches and navigates your codebase

**Learn more**: `M:\_tools\langchain-agent-base\examples\building-ultimate-coding-agent\`

## 📝 Example Calculations

```
Simple: 5 + 3 = 8
Decimals: 3.14 * 2 = 6.28
Parentheses: (5 + 3) * 2 = 16
Complex: (10 + 5) * 3 - 8 / 2 = 41
```

## 🔮 Future Enhancements

Potential improvements:
- Scientific functions (sin, cos, sqrt, etc.)
- History of calculations
- Theme switcher (light/dark mode)
- Memory functions (M+, M-, MR, MC)
- Percentage calculations
- Export calculation history

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

To modify or enhance:
1. Open the CLI: `python examples/building-ultimate-coding-agent/cli.py ./test_coding_project_2`
2. Ask the agent to make changes
3. Approve the proposed modifications
4. Test the updated calculator

---

**Created with AI assistance** • Built with ❤️ using the Ultimate Coding Agent
