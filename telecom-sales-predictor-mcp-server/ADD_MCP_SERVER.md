# Adding the Telecom Predictor MCP Server to LLM Clients

This guide explains how to integrate the Telecom Sales Predictor MCP server with Cursor and Claude Desktop.

## Overview

Once configured, you'll be able to:
- Ask the LLM to "Generate sales predictions for telecom data"
- Receive PNG visualizations directly in the chat
- Get model performance metrics and analysis
- Use natural language to interact with your data analysis

## Prerequisites

Before adding the server to an LLM client:

1. ✅ Complete the setup in `instructions.md`
2. ✅ Virtual environment created with Python 3.10+
3. ✅ Dependencies installed (`pip install -r requirements.txt`)
4. ✅ Test that the server runs without errors

## Option 1: Adding to Cursor

Cursor uses MCP servers to extend the AI's capabilities with custom tools.

### Step 1: Locate Cursor's MCP Configuration File

**On macOS/Linux:**
```bash
~/.cursor/mcp.json
```

**On Windows:**
```
%APPDATA%\Cursor\mcp.json
```

### Step 2: Edit the Configuration File

Open the file in a text editor. If it doesn't exist, create it.

**Add this configuration:**

```json
{
  "mcpServers": {
    "telecom-predictor": {
      "command": "/Users/vishalkumar/code/frontier/predict-o-matic/telecom-sales-predictor-mcp-server/venv/bin/python",
      "args": [
        "/Users/vishalkumar/code/frontier/predict-o-matic/telecom-sales-predictor-mcp-server/mcp_server.py"
      ],
      "env": {}
    }
  }
}
```

**If you already have other MCP servers configured:**

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "...",
      "args": ["..."]
    },
    "telecom-predictor": {
      "command": "/Users/vishalkumar/code/frontier/predict-o-matic/telecom-sales-predictor-mcp-server/venv/bin/python",
      "args": [
        "/Users/vishalkumar/code/frontier/predict-o-matic/telecom-sales-predictor-mcp-server/mcp_server.py"
      ],
      "env": {}
    }
  }
}
```

### Step 3: Verify Paths

**IMPORTANT:** Use absolute paths, not relative paths!

Get the absolute path:

```bash
# Get path to Python in virtual environment
cd /Users/vishalkumar/code/frontier/predict-o-matic/telecom-sales-predictor-mcp-server
source venv/bin/activate
which python
# Copy this path

# Get path to mcp_server.py
pwd
# This shows: /Users/vishalkumar/code/frontier/predict-o-matic/telecom-sales-predictor-mcp-server
# Full path to script: [above]/mcp_server.py
```

**Example for different user:**

If your username is `johndoe`, the config would be:

```json
{
  "mcpServers": {
    "telecom-predictor": {
      "command": "/Users/johndoe/code/frontier/predict-o-matic/telecom-sales-predictor-mcp-server/venv/bin/python",
      "args": [
        "/Users/johndoe/code/frontier/predict-o-matic/telecom-sales-predictor-mcp-server/mcp_server.py"
      ],
      "env": {}
    }
  }
}
```

### Step 4: Restart Cursor

1. Save the `mcp.json` file
2. Completely quit Cursor (Cmd+Q on Mac, Alt+F4 on Windows)
3. Reopen Cursor

### Step 5: Verify the Server is Loaded

1. Open a new chat in Cursor
2. Look for an indication that MCP tools are available (varies by Cursor version)
3. Try asking: "What tools do you have available?"
4. The AI should mention `generate_sales_predictions`

### Step 6: Test It

Try these queries:

```
"Generate sales predictions for the telecom data"

"Show me the model predictions with statistics"

"Create a visualization of the sales forecasts"

"Run the telecom analysis and show the chart"
```

The AI will call the MCP tool and display:
- Model performance metrics (R², RMSE, MAE)
- PNG visualization with actual vs predicted values
- Analysis of the results

## Option 2: Adding to Claude Desktop

Claude Desktop (the official Anthropic desktop app) supports MCP servers.

### Step 1: Locate Claude's MCP Configuration File

**On macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**On Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**On Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

### Step 2: Edit the Configuration File

Open the file in a text editor. If it doesn't exist, create it.

**Add this configuration:**

```json
{
  "mcpServers": {
    "telecom-predictor": {
      "command": "/Users/vishalkumar/code/frontier/predict-o-matic/telecom-sales-predictor-mcp-server/venv/bin/python",
      "args": [
        "/Users/vishalkumar/code/frontier/predict-o-matic/telecom-sales-predictor-mcp-server/mcp_server.py"
      ]
    }
  }
}
```

**If you already have other servers:**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
    },
    "telecom-predictor": {
      "command": "/Users/vishalkumar/code/frontier/predict-o-matic/telecom-sales-predictor-mcp-server/venv/bin/python",
      "args": [
        "/Users/vishalkumar/code/frontier/predict-o-matic/telecom-sales-predictor-mcp-server/mcp_server.py"
      ]
    }
  }
}
```

### Step 3: Adjust Paths for Your System

Replace `/Users/vishalkumar/` with your actual home directory path.

**Get your paths:**

```bash
cd /Users/vishalkumar/code/frontier/predict-o-matic/telecom-sales-predictor-mcp-server
source venv/bin/activate
which python  # Copy this path
pwd           # Use this + /mcp_server.py
```

### Step 4: Restart Claude Desktop

1. Save the configuration file
2. Completely quit Claude Desktop
3. Reopen Claude Desktop

### Step 5: Verify the Server

1. Start a new conversation
2. Claude should automatically discover the tool
3. Try: "What tools do you have access to?"
4. Should list `generate_sales_predictions`

### Step 6: Test It

Ask Claude:

```
"Please generate the telecom sales predictions"

"Show me the sales forecast visualization"

"Run the predictive analysis on the telecom data"
```

Claude will:
1. Call the MCP tool
2. Display the analysis results
3. Show the PNG chart inline
4. Explain the predictions

## Configuration Reference

### Basic Configuration Structure

```json
{
  "mcpServers": {
    "<server-name>": {
      "command": "<path-to-python>",
      "args": ["<path-to-mcp_server.py>"],
      "env": {}
    }
  }
}
```

### Configuration Fields

| Field | Description | Required |
|-------|-------------|----------|
| `command` | Path to Python interpreter in venv | Yes |
| `args` | Array with path to `mcp_server.py` | Yes |
| `env` | Environment variables (optional) | No |

### Advanced: Environment Variables

You can pass environment variables to the server:

```json
{
  "mcpServers": {
    "telecom-predictor": {
      "command": "/Users/vishalkumar/.../venv/bin/python",
      "args": ["/Users/vishalkumar/.../mcp_server.py"],
      "env": {
        "ANALYSIS_TIMEOUT": "120",
        "DEBUG_MODE": "false",
        "LOG_LEVEL": "info"
      }
    }
  }
}
```

Then access in `mcp_server.py`:

```python
import os
timeout = int(os.getenv('ANALYSIS_TIMEOUT', 60))
```

## Troubleshooting

### Server Doesn't Appear in Tool List

**Check 1: Configuration file syntax**
- JSON must be valid (no trailing commas, proper quotes)
- Use a JSON validator: https://jsonlint.com/

**Check 2: Paths are correct**
```bash
# Test the Python path
/Users/vishalkumar/.../venv/bin/python --version
# Should show Python 3.10+

# Test the script path
ls -la /Users/vishalkumar/.../mcp_server.py
# Should exist
```

**Check 3: Restart the client**
- Completely quit and reopen
- Some clients cache the configuration

**Check 4: Virtual environment**
```bash
cd telecom-sales-predictor-mcp-server
source venv/bin/activate
python mcp_server.py
# Should not crash immediately
```

### Server Crashes or Doesn't Respond

**Check logs:**

**For Cursor:**
- Check Console logs (Help → Toggle Developer Tools)
- Look for MCP-related errors

**For Claude Desktop:**
- Check the application logs
- On macOS: `~/Library/Logs/Claude/`

**Common issues:**

1. **Python version too old**
   - Need Python 3.10+
   - Check: `python --version` from venv

2. **Missing dependencies**
   ```bash
   cd telecom-sales-predictor-mcp-server
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Analysis script missing**
   ```bash
   ls -la ../telecom-sales-predictor/analyze_data.py
   # Must exist
   ```

4. **Data file missing**
   ```bash
   ls -la ../telecom-sales-predictor/final_dataset.csv
   # Must exist
   ```

### Tool Call Fails

**Error: "Analysis script not found"**
- Verify the directory structure
- Server expects: `../telecom-sales-predictor/analyze_data.py`

**Error: "Data file not found"**
- Ensure `final_dataset.csv` exists
- Check file permissions

**Error: "Process timed out"**
- Increase timeout in `mcp_server.py`
- Or reduce dataset size for testing

**Error: "PNG file was not generated"**
- Test the analysis script directly
- Check matplotlib installation

### Permission Denied Errors

```bash
# Make the script executable
chmod +x telecom-sales-predictor-mcp-server/mcp_server.py

# Verify Python has execute permissions
ls -la telecom-sales-predictor-mcp-server/venv/bin/python
```

### Path Issues on Windows

Windows uses backslashes. In JSON, escape them:

```json
{
  "mcpServers": {
    "telecom-predictor": {
      "command": "C:\\Users\\vishalkumar\\...\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\vishalkumar\\...\\mcp_server.py"
      ]
    }
  }
}
```

Or use forward slashes (works in most cases):

```json
{
  "mcpServers": {
    "telecom-predictor": {
      "command": "C:/Users/vishalkumar/.../venv/Scripts/python.exe",
      "args": [
        "C:/Users/vishalkumar/.../mcp_server.py"
      ]
    }
  }
}
```

## Example Conversations

### Example 1: Basic Request

**User:** "Generate sales predictions for our telecom data"

**Claude/Cursor:**
- Calls `generate_sales_predictions(include_stats=true)`
- Receives analysis results and PNG
- Displays: "I've generated the sales predictions. Here's what the analysis shows:
  - VAS Sales model achieved R² of 0.87 on test data
  - Speed Upgrades model achieved R² of 0.79
  - The visualization below shows actual vs predicted values..."
- Shows the PNG chart inline

### Example 2: Specific Request

**User:** "Show me just the visualization without all the statistics"

**Claude/Cursor:**
- Calls `generate_sales_predictions(include_stats=false)`
- Receives only the PNG
- Displays the chart with brief explanation

### Example 3: Follow-up Analysis

**User:** "Generate the predictions"  
**Claude:** [Shows chart and stats]

**User:** "What do the confidence intervals tell us?"  
**Claude:** "The 95% confidence intervals in the shaded regions show..."

**User:** "Which features are most important?"  
**Claude:** "Based on the feature coefficients:
  - Emails_Sent has coefficient of X.XX...
  - Push_Notifications_Sent...
  - Temporal factors..."

## Best Practices

### 1. Use Absolute Paths
❌ `"command": "python"`  
✅ `"command": "/full/path/to/venv/bin/python"`

### 2. Keep Virtual Environment Active
The Python path should point to the venv's Python, not system Python.

### 3. Test Manually First
Before configuring in Cursor/Claude, test the server works:
```bash
cd telecom-sales-predictor-mcp-server
source venv/bin/activate
python mcp_server.py
# No immediate crashes = good sign
```

### 4. Restart After Changes
Always completely quit and restart the LLM client after changing configuration.

### 5. Check File Permissions
Ensure the Python executable and script are readable/executable.

## Security Considerations

### What the Server Can Do

✅ **Allowed:**
- Read CSV data from `telecom-sales-predictor` directory
- Run the analysis script
- Generate PNG files
- Return results to the LLM

❌ **Cannot:**
- Access files outside the project directory
- Make network requests
- Modify system files
- Execute arbitrary commands

### Safe Usage

- The server only runs the specific `analyze_data.py` script
- No arbitrary code execution
- Runs in the context of your user account
- Same permissions as running the script manually

### Data Privacy

- Data stays on your local machine
- No data sent to external services
- PNG generated locally
- Results only sent to the LLM client you're using

## Updating the Server

When you modify `mcp_server.py`:

1. **Save changes** to the file
2. **No need to reinstall** dependencies (unless adding new ones)
3. **Restart the LLM client** to reload the server
4. **Test** with a simple query

When you modify `analyze_data.py`:

- No changes needed to MCP server
- Just restart the LLM client
- The server will call the updated script

## Removing the Server

To remove from Cursor or Claude:

1. Edit the configuration file
2. Delete the `"telecom-predictor"` entry
3. Save and restart the client

Or comment it out:

```json
{
  "mcpServers": {
    // "telecom-predictor": {
    //   "command": "...",
    //   "args": ["..."]
    // }
  }
}
```

## Next Steps

1. ✅ Add the server to Cursor or Claude
2. 🧪 Test with sample queries
3. 📊 Use for real analysis tasks
4. 🔧 Customize as needed
5. 🚀 Build more MCP tools!

## Additional Resources

- **MCP Documentation**: https://modelcontextprotocol.io/
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **Cursor Docs**: https://docs.cursor.com/
- **Claude API**: https://docs.anthropic.com/

## Success Checklist

✅ Configuration file created/updated  
✅ Paths are absolute and correct  
✅ JSON syntax is valid  
✅ LLM client restarted  
✅ Tool appears in tool list  
✅ Test query works  
✅ PNG displays correctly  
✅ Statistics are accurate

Congratulations! Your MCP server is now integrated. 🎉

---

**Questions or Issues?**

1. Check `instructions.md` for setup problems
2. Verify paths in configuration
3. Look at LLM client logs for errors
4. Test the server manually first
5. Ensure data files exist

