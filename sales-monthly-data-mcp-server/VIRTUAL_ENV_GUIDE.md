# Virtual Environment Guide

## What is a Virtual Environment?

A **virtual environment** is an isolated Python workspace for your project. It keeps your project's dependencies separate from other Python projects and your system Python installation.

### Why Use Virtual Environments?

1. **Isolation**: Each project has its own packages without conflicts
2. **Clean System**: Your system Python stays clean and unmodified
3. **Reproducibility**: Easy to share exact dependencies with others
4. **Version Control**: Different projects can use different package versions

---

## Quick Start

### 1. Create a Virtual Environment (One Time Only)

```bash
cd /path/to/sales-monthly-data-mcp-server
python3 -m venv venv
```

This creates a `venv` folder containing a fresh Python installation.

### 2. Activate the Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```cmd
venv\Scripts\activate
```

**You'll know it's active** when you see `(venv)` at the beginning of your terminal prompt:
```
(venv) user@computer:~/project$
```

### 3. Install Dependencies

Once activated, install packages normally:

```bash
pip install -r requirements.txt
pip install 'git+https://github.com/modelcontextprotocol/python-sdk.git'
```

These packages install ONLY in the virtual environment, not system-wide.

### 4. Work on Your Project

While activated, any Python commands use the virtual environment:

```bash
# Run scripts
python sales_data.py January 2023
python test_sales_data.py
python api_server.py

# Run MCP server
python mcp_server.py
```

### 5. Deactivate When Done

To exit the virtual environment and return to your system Python:

```bash
deactivate
```

The `(venv)` prefix disappears from your prompt.

---

## Complete Workflow Example

```bash
# Navigate to project
cd /path/to/sales-monthly-data-mcp-server

# Activate virtual environment
source venv/bin/activate

# Your prompt now shows (venv)
# Install or update packages if needed
pip install -r requirements.txt

# Run tests
python test_sales_data.py

# Start API server
python api_server.py

# When done, deactivate
deactivate
```

---

## Common Scenarios

### Starting Fresh Each Day

```bash
# Navigate to project
cd /path/to/sales-monthly-data-mcp-server

# Activate
source venv/bin/activate

# Work on your code...

# Deactivate when done
deactivate
```

### Installing New Packages

```bash
# Activate first
source venv/bin/activate

# Install package
pip install some-new-package

# Update requirements.txt (optional)
pip freeze > requirements.txt

# Deactivate
deactivate
```

### Running Scripts Without Activating

You can also run scripts directly without activating:

```bash
# Use the venv's Python directly
./venv/bin/python sales_data.py January 2023
./venv/bin/python test_sales_data.py

# On Windows
venv\Scripts\python.exe sales_data.py January 2023
```

This is useful for one-off commands or automation scripts.

---

## Troubleshooting

### Problem: "Command not found: python3"

**Solution:** Use `python` instead of `python3` on some systems:
```bash
python -m venv venv
```

### Problem: "Permission denied" when activating

**Solution:** Make sure the activate script is executable:
```bash
chmod +x venv/bin/activate
```

### Problem: Forgot if virtual environment is active

**Check:** Look for `(venv)` in your terminal prompt, or run:
```bash
which python
```

If active, it should show a path containing `venv`:
```
/path/to/project/venv/bin/python
```

### Problem: Virtual environment not working after system Python upgrade

**Solution:** Delete and recreate the virtual environment:
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Problem: "No module named 'mcp'" even in venv

**Solution:** Make sure you've installed the MCP SDK:
```bash
source venv/bin/activate
pip install 'git+https://github.com/modelcontextprotocol/python-sdk.git'
```

---

## Best Practices

### ✅ DO:
- Always activate the virtual environment before working on the project
- Keep `requirements.txt` updated with your dependencies
- Add `venv/` to `.gitignore` (virtual environments shouldn't be committed)
- Create a new virtual environment for each project

### ❌ DON'T:
- Don't install packages without activating the venv first
- Don't commit the `venv/` folder to version control (it's huge!)
- Don't modify files inside the `venv/` folder directly
- Don't use `sudo pip install` (virtual environments don't need sudo)

---

## Understanding the venv Folder Structure

```
venv/
├── bin/               # Executables (python, pip, activate script)
│   ├── activate       # Activation script for bash/zsh
│   ├── python         # Python interpreter
│   └── pip            # Package installer
├── include/           # C headers
├── lib/               # Installed packages
│   └── python3.13/
│       └── site-packages/  # Your installed packages go here
└── pyvenv.cfg         # Configuration file
```

You rarely need to look inside `venv/` - just activate it and work normally!

---

## Advanced: Using with MCP in Cursor

When configuring the MCP server in Cursor, you have two options:

### Option 1: Use venv Python directly (Recommended)

```json
{
  "mcpServers": {
    "sales_data": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": [
        "/absolute/path/to/mcp_server.py"
      ],
      "cwd": "/absolute/path/to/project"
    }
  }
}
```

### Option 2: Use activation script

```json
{
  "mcpServers": {
    "sales_data": {
      "command": "bash",
      "args": [
        "-c",
        "source /absolute/path/to/venv/bin/activate && python /absolute/path/to/mcp_server.py"
      ],
      "cwd": "/absolute/path/to/project"
    }
  }
}
```

**Replace `/absolute/path/to/` with your actual project path!**

---

## Summary

| Action | Command |
|--------|---------|
| Create venv | `python3 -m venv venv` |
| Activate (Mac/Linux) | `source venv/bin/activate` |
| Activate (Windows) | `venv\Scripts\activate` |
| Install packages | `pip install package-name` |
| Deactivate | `deactivate` |
| Check if active | Look for `(venv)` in prompt |
| Run without activating | `./venv/bin/python script.py` |

---

## Need More Help?

- **Python Virtual Environments Official Docs**: https://docs.python.org/3/tutorial/venv.html
- **Real Python Tutorial**: https://realpython.com/python-virtual-environments-a-primer/
- **Video Tutorial**: Search "Python virtual environment tutorial" on YouTube

Remember: Virtual environments are your friend! They make Python development much cleaner and more manageable. 🐍✨
