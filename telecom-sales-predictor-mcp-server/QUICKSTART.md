# Quick Start Guide

Get the Telecom Sales Predictor MCP Server running in 5 minutes.

## Prerequisites

- Python 3.10 or higher
- The adjacent `telecom-sales-predictor` directory with `analyze_data.py` and `final_dataset.csv`

## Setup (Automated)

```bash
cd telecom-sales-predictor-mcp-server
./setup.sh
```

The setup script will:
1. Check Python version
2. Create virtual environment
3. Install all dependencies
4. Run verification tests

## Setup (Manual)

```bash
cd telecom-sales-predictor-mcp-server

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify setup
python test_server.py
```

## Configure for Cursor

Edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "telecom-predictor": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["/absolute/path/to/mcp_server.py"]
    }
  }
}
```

Replace paths with your actual paths:

```bash
cd telecom-sales-predictor-mcp-server
source venv/bin/activate
which python  # Copy this for "command"
pwd           # Use this + /mcp_server.py for "args"
```

**Restart Cursor completely** (Cmd+Q, then reopen).

## Configure for Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "telecom-predictor": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["/absolute/path/to/mcp_server.py"]
    }
  }
}
```

**Restart Claude Desktop completely**.

## Test It

Open Cursor or Claude and ask:

```
"Generate sales predictions for the telecom data"
```

You should see:
- ✅ Model performance metrics
- 📊 PNG visualization with actual vs predicted values

## Troubleshooting

**Problem:** Server doesn't appear

```bash
# Check configuration syntax
cat ~/.cursor/mcp.json | python -m json.tool

# Verify paths are absolute
cat ~/.cursor/mcp.json | grep command
cat ~/.cursor/mcp.json | grep args
```

**Problem:** Tool call fails

```bash
# Test the server manually
cd telecom-sales-predictor-mcp-server
source venv/bin/activate
python test_server.py  # Should all pass

# Test the analysis script
cd ../telecom-sales-predictor
python analyze_data.py  # Should generate PNG
```

## Full Documentation

For detailed information, see:

- **[README.md](README.md)** - Project overview
- **[instructions.md](instructions.md)** - Complete setup guide
- **[ADD_MCP_SERVER.md](ADD_MCP_SERVER.md)** - Detailed configuration guide

## Common Commands

```bash
# Activate virtual environment
cd telecom-sales-predictor-mcp-server
source venv/bin/activate

# Run verification tests
python test_server.py

# Test the server manually
python mcp_server.py

# Deactivate when done
deactivate
```

## Success Checklist

✅ Python 3.10+ installed  
✅ Virtual environment created  
✅ Dependencies installed  
✅ `test_server.py` passes all tests  
✅ Configuration added to Cursor/Claude  
✅ Paths are absolute  
✅ LLM client restarted  
✅ Tool appears in tool list  
✅ Test query works

Done! 🎉

