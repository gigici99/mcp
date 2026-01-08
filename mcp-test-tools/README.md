# MCP Universal Test Suite Generator 🚀

An advanced **Model Context Protocol (MCP)** server built with Python to empower AI assistants (like Claude Desktop) with the ability to analyze projects and automatically generate, manage, and execute testing suites.

Currently supports **Java (JUnit)** and **Web (Selenium)** projects.

## ✨ Features

- 📂 **Project Analysis**: Deep scans project structures to identify classes, methods, and dependencies.
- 🧪 **Automated JUnit Generation**: Generates unit tests following best practices and project-specific patterns.
- 🌐 **Web Testing**: Integrated tools for Selenium-based end-to-end testing.
- 🛠️ **Direct Execution**: Run Maven or NPM commands directly through the AI assistant to validate generated tests.
- ⚡ **Optimized with `uv`**: Uses the lightning-fast Python package manager for dependency resolution.

---

## 🚀 Quick Start

### Prerequisites
- [Python 3.10+](https://www.python.org/)
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- [Claude Desktop](https://claude.ai/download) (to use the tools in chat)

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/gigici99/mcp.git](https://github.com/gigici99/mcp.git)
   cd mcp