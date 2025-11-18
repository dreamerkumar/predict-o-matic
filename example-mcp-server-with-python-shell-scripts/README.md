# MCP Calculator Server - Shell Command Wrapper Example

## Purpose

This project demonstrates how to create Model Context Protocol (MCP) servers that wrap shell commands and expose them as tools for Large Language Models (LLMs). It showcases a complete progression from a simple command-line calculator to a fully-featured MCP server that can be used with AI assistants like Claude in Cursor or Claude Desktop.

**Why this project exists:**
- Demonstrates best practices for wrapping shell scripts as MCP tools
- Shows the evolution from CLI → API → MCP Server
- Provides a template for creating your own MCP servers
- Illustrates how to expose existing command-line utilities to AI assistants

## Architecture Overview

This project consists of three layers:

1. **CLI Layer** (`calculator.py`): A simple Python script that performs arithmetic operations
2. **API Layer** (`api_server.py`): A FastAPI server that wraps the CLI script with a REST endpoint
3. **MCP Layer** (`mcp_server.py`): An MCP server that exposes the calculator as a tool for LLM clients

## Prerequisites

- **Python 3.10 or higher** (required for MCP SDK)
- pip (Python package installer)

**Note:** Parts 1 and 2 (CLI and API) work with Python 3.8+, but Part 3 (MCP Server) requires Python 3.10+ due to MCP SDK requirements.

## Installation

### 1. Clone or Download this Repository

```bash
cd /path/to/your/project
```

### 2. Activate the Virtual Environment

**A virtual environment is already set up in this project!** Just activate it:

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```cmd
venv\Scripts\activate
```

You'll see `(venv)` appear in your terminal prompt when it's active.

**New to virtual environments?** Read the [Virtual Environment Guide](VIRTUAL_ENV_GUIDE.md) for a complete explanation!

### 3. Verify Installation

All dependencies (including MCP SDK) are already installed in the virtual environment! Verify:

```bash
python -c "import mcp; print('✅ MCP SDK ready!')"
```

### 4. If You Need to Reinstall Dependencies

If something goes wrong, you can always reinstall:

```bash
# Make sure venv is activated (you should see (venv) in your prompt)
source venv/bin/activate

# Reinstall packages
pip install -r requirements.txt
pip install 'git+https://github.com/modelcontextprotocol/python-sdk.git'
```

### 5. Starting Fresh (Optional)

If you need to create a new virtual environment from scratch:

```bash
# Delete old venv
rm -rf venv

# Create new venv
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install 'git+https://github.com/modelcontextprotocol/python-sdk.git'
```

**Python Version Note:** The MCP SDK requires Python 3.10 or higher. Parts 1 and 2 (CLI and API) work with Python 3.8+.

## Usage

**⚠️ Important:** For all examples below, make sure your virtual environment is activated:

```bash
source venv/bin/activate  # You should see (venv) in your prompt
```

To deactivate when done:
```bash
deactivate
```

---

### Part 1: CLI Calculator

The command-line calculator performs addition and multiplication on two numbers.

#### Running the Calculator

```bash
# Addition
python3 calculator.py add 5 3
# Output: 8.0

# Multiplication
python3 calculator.py multiply 4 7
# Output: 28.0

# With negative numbers
python3 calculator.py add -10 5
# Output: -5.0

# With decimals
python3 calculator.py multiply 2.5 4
# Output: 10.0
```

#### Running Tests

Run the comprehensive test suite to verify the calculator works correctly:

```bash
python3 test_calculator.py
```

Expected output:
```
============================================================
Testing calculator.py
============================================================

Addition Tests:
------------------------------------------------------------
✅ Add positive numbers: PASSED - add(5, 3) = 8.0
✅ Add negative numbers: PASSED - add(-5, -3) = -8.0
✅ Add positive and negative: PASSED - add(10, -4) = 6.0
✅ Add with zero: PASSED - add(0, 7) = 7.0
✅ Add decimals: PASSED - add(2.5, 3.7) = 6.2

Multiplication Tests:
------------------------------------------------------------
✅ Multiply positive numbers: PASSED - multiply(5, 3) = 15.0
✅ Multiply negative numbers: PASSED - multiply(-5, -3) = 15.0
✅ Multiply positive and negative: PASSED - multiply(10, -4) = -40.0
✅ Multiply by zero: PASSED - multiply(0, 7) = 0.0
✅ Multiply decimals: PASSED - multiply(2.5, 4) = 10.0

Error Handling Tests:
------------------------------------------------------------
✅ Invalid operation: PASSED - Correctly failed with error
✅ Non-numeric first param: PASSED - Correctly failed with error
✅ Non-numeric second param: PASSED - Correctly failed with error

============================================================
Results: 13 passed, 0 failed
============================================================
✅ All tests passed!
```

### Part 2: FastAPI Web Server

The FastAPI server exposes the calculator via a REST API.

#### Starting the Server

```bash
python3 api_server.py
```

The server will start on `http://localhost:8000`

#### Testing the API

Open another terminal and test the endpoints:

**Using curl:**

```bash
# Addition
curl -X POST http://localhost:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "param1": 5, "param2": 3}'

# Multiplication
curl -X POST http://localhost:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "multiply", "param1": 4, "param2": 7}'

# Health check
curl http://localhost:8000/health
```

**Using Python:**

```python
import requests

response = requests.post(
    "http://localhost:8000/calculate",
    json={"operation": "add", "param1": 10, "param2": 5}
)
print(response.json())
# Output: {"result": 15.0, "operation": "add", "param1": 10.0, "param2": 5.0}
```

#### API Documentation

Once the server is running, visit:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### Part 3: MCP Server

The MCP server exposes the calculator as a tool that can be used by AI assistants.

#### Configuring for Cursor

1. Open Cursor Settings
2. Navigate to the MCP section
3. Add the following configuration (replace paths with your actual paths):

**Recommended: Use the virtual environment's Python directly**

```json
{
  "mcpServers": {
    "calculator": {
      "command": "/absolute/path/to/example-mcp-server-with-python-shell-scripts/venv/bin/python",
      "args": [
        "/absolute/path/to/example-mcp-server-with-python-shell-scripts/mcp_server.py"
      ],
      "cwd": "/absolute/path/to/example-mcp-server-with-python-shell-scripts"
    }
  }
}
```

**Important:** 
- Replace `/absolute/path/to/` with your actual project path
- Use absolute paths, not relative paths
- Use the venv's Python to ensure MCP SDK is available
- On Windows, use `venv/Scripts/python.exe` instead of `venv/bin/python`

Example for macOS/Linux:
```json
{
  "mcpServers": {
    "calculator": {
      "command": "/Users/username/projects/example-mcp-server-with-python-shell-scripts/venv/bin/python",
      "args": [
        "/Users/username/projects/example-mcp-server-with-python-shell-scripts/mcp_server.py"
      ],
      "cwd": "/Users/username/projects/example-mcp-server-with-python-shell-scripts"
    }
  }
}
```

Example for Windows:
```json
{
  "mcpServers": {
    "calculator": {
      "command": "C:/Users/username/projects/example-mcp-server-with-python-shell-scripts/venv/Scripts/python.exe",
      "args": [
        "C:/Users/username/projects/example-mcp-server-with-python-shell-scripts/mcp_server.py"
      ],
      "cwd": "C:/Users/username/projects/example-mcp-server-with-python-shell-scripts"
    }
  }
}
```

#### Configuring for Claude Desktop

1. Locate your Claude Desktop config file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the calculator server configuration (use the venv Python):

```json
{
  "mcpServers": {
    "calculator": {
      "command": "/absolute/path/to/example-mcp-server-with-python-shell-scripts/venv/bin/python",
      "args": [
        "/absolute/path/to/example-mcp-server-with-python-shell-scripts/mcp_server.py"
      ],
      "cwd": "/absolute/path/to/example-mcp-server-with-python-shell-scripts"
    }
  }
}
```

**Remember:** 
- Use absolute paths
- On Windows, use `venv/Scripts/python.exe` instead of `venv/bin/python`

3. Restart Claude Desktop

#### Using the MCP Tool

Once configured, you can interact with the calculator through your AI assistant:

**Example prompts in Cursor or Claude Desktop:**

- "Use the calculator to add 15 and 27"
- "Calculate 8 multiplied by 12 using the calculator tool"
- "What is 100 plus 250?"

The AI assistant will automatically invoke the calculator tool and return the results.

#### Testing the MCP Server Directly

You can test the MCP server using the MCP inspector:

```bash
# Install MCP inspector if you haven't already
npm install -g @modelcontextprotocol/inspector

# Run the inspector
mcp-inspector python3 mcp_server.py
```

This will open a web interface where you can test the MCP server interactively.

## Project Structure

```
.
├── README.md                    # This file - main documentation
├── VIRTUAL_ENV_GUIDE.md        # Complete guide to virtual environments
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore file (excludes venv/)
├── calculator.py                # CLI calculator script
├── test_calculator.py          # Test suite for CLI calculator
├── api_server.py               # FastAPI web server
├── mcp_server.py               # MCP server implementation
├── mcp_config.json             # Example MCP configuration
└── venv/                        # Virtual environment (not in git)
    ├── bin/                     # Python executables
    ├── lib/                     # Installed packages
    └── ...
```

## Testing

### Manual Testing Checklist

1. **CLI Calculator:**
   ```bash
   python3 test_calculator.py
   ```
   All tests should pass.

2. **API Server:**
   ```bash
   # Terminal 1: Start server
   python3 api_server.py
   
   # Terminal 2: Test endpoint
   curl -X POST http://localhost:8000/calculate \
     -H "Content-Type: application/json" \
     -d '{"operation": "add", "param1": 5, "param2": 3}'
   ```
   Should return: `{"result": 8.0, "operation": "add", "param1": 5.0, "param2": 3.0}`

3. **MCP Server:**
   - Configure in Cursor or Claude Desktop as described above
   - Ask the AI to perform a calculation
   - Verify the tool is invoked and returns correct results

## Troubleshooting

### Common Issues

**Issue: "command not found: python3"**
- Solution: Use `python` instead of `python3` on Windows, or create a Python alias

**Issue: "Module not found: mcp"**
- Solution: Make sure you've activated your virtual environment and installed dependencies:
  ```bash
  source venv/bin/activate
  pip install -r requirements.txt
  ```

**Issue: MCP server not showing up in Cursor**
- Solution: 
  - Verify absolute paths in configuration
  - Restart Cursor after adding configuration
  - Check Cursor's MCP logs for errors

**Issue: Calculator returns errors in MCP**
- Solution: 
  - Ensure `calculator.py` is in the same directory as `mcp_server.py`
  - Verify Python can find and execute `calculator.py`
  - Check that the working directory (`cwd`) is set correctly in config

## Extending This Example

This example can be extended in many ways:

1. **Add more operations**: Extend calculator.py with division, subtraction, powers, etc.
2. **Support more parameters**: Allow operations on lists of numbers
3. **Add more tools**: Create additional MCP tools that wrap other shell commands
4. **Error handling**: Add more sophisticated error handling and logging
5. **Authentication**: Add API key authentication to the FastAPI server
6. **Database**: Store calculation history in a database

## Learn More

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Cursor Documentation](https://cursor.sh/docs)

## License

This is an example project for educational purposes. Feel free to use and modify as needed.

