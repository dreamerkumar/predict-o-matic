# Adding the Telecom Predictor MCP Server to LLM Clients

This guide explains how to integrate the Telecom Sales Predictor MCP server with Cursor and Claude Desktop.

## Overview

Once configured, you'll be able to:
- 🤖 Ask the LLM to "Analyze the telecom sales data with the hybrid model"
- 🔮 Ask to "Predict December 2025 sales"
- 📊 Receive PNG visualizations directly in the chat
- 📈 Get model performance metrics and forecasts
- 🎯 Use natural language to interact with your data analysis

## What's New (November 2025)

✨ **Two Tools Available:**
1. **`analyze_hybrid_model`** - Train & evaluate ML models (Random Forest + Linear Regression)
2. **`predict_december_2025`** - Generate December 2025 forecasts

✅ **No Configuration Changes Needed** - Same MCP endpoint, just restart your LLM client!

## Prerequisites

Before adding the server to an LLM client:

1. ✅ Complete the setup in `instructions.md`
2. ✅ Virtual environment created with Python 3.10+
3. ✅ Dependencies installed (`pip install -r requirements.txt`)
4. ✅ Test that both analysis scripts run successfully
5. ✅ Verify both data files exist (`final_dataset.csv`, `test_dataset_dec_2025.csv`)

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
2. Look for an indication that MCP tools are available
3. Try asking: "What tools do you have available?"
4. The AI should mention **two tools**: `analyze_hybrid_model` and `predict_december_2025`

### Step 6: Test Both Tools

**Test Tool 1 - Hybrid Analysis:**
```
"Analyze the telecom sales data using the hybrid model"
"Show me the model performance"
"Train and evaluate the predictive models"
```

Expected: Performance metrics + PNG chart with actual vs predicted values

**Test Tool 2 - December Predictions:**
```
"Predict December 2025 sales"
"What are the December forecasts?"
"Generate December 2025 predictions"
```

Expected: Prediction summary + Cumulative forecast chart

The AI will call the appropriate MCP tool and display:
- Model performance metrics / Prediction summaries
- PNG visualizations (200-400 KB, optimized for MCP)
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
2. Claude should automatically discover the tools
3. Try: "What tools do you have access to?"
4. Should list both `analyze_hybrid_model` and `predict_december_2025`

### Step 6: Test Both Tools

Ask Claude:

**For Hybrid Analysis:**
```
"Please analyze the telecom sales data using the hybrid model"
"Show me the model performance evaluation"
"Train the Random Forest and Linear Regression models"
```

**For December Predictions:**
```
"Predict December 2025 sales"
"What will our sales be in December based on marketing campaigns?"
"Generate the December 2025 forecast"
```

Claude will:
1. Call the appropriate MCP tool
2. Display the analysis results or forecasts
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
timeout = int(os.getenv('ANALYSIS_TIMEOUT', 90))
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

### Only One Tool Appears Instead of Two

**Cause:** Using old server code

**Solution:**
```bash
# Verify server has both tools
grep -c "analyze_hybrid_model" mcp_server.py
grep -c "predict_december_2025" mcp_server.py
# Both should return > 0

# Restart LLM client completely
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

3. **Analysis scripts missing or renamed**
   ```bash
   ls -la ../telecom-sales-predictor/analyze_data_hybrid.py
   ls -la ../telecom-sales-predictor/predict_december_2025.py
   # Both must exist
   ```

4. **Data files missing**
   ```bash
   ls -la ../telecom-sales-predictor/final_dataset.csv
   ls -la ../telecom-sales-predictor/test_dataset_dec_2025.csv
   # Both must exist
   ```

### Tool Call Fails

**Error: "analyze_data_hybrid.py not found"**
- Script was renamed from `analyze_data.py`
- Verify it exists in `telecom-sales-predictor/` directory

**Error: "test_dataset_dec_2025.csv not found"**
- Run `create_test_dataset_updated.py` to generate December test data
- Or verify the file exists

**Error: "Data file not found"**
- Ensure `final_dataset.csv` exists
- Check file permissions

**Error: "Process timed out"**
- Timeout is 90 seconds (hybrid models need time)
- Normal for first run
- Increase timeout in `mcp_server.py` if needed

**Error: "PNG file was not generated"**
- Test the scripts directly first
- Check matplotlib installation
- Verify `output_files/` directory permissions

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

### Example 1: Hybrid Model Analysis

**User:** "Analyze the telecom sales data using the hybrid model"

**Claude/Cursor:**
- 🔧 Calls `analyze_hybrid_model(include_stats=true)`
- ⏳ Runs analysis (20-30 seconds)
- 📊 Receives metrics and PNG
- 💬 Displays: "I've analyzed the telecom sales data using the hybrid model:
  
  **VAS_Sold (Random Forest):**
  - Test Accuracy: 86.4% (R² = 0.864)
  - RMSE: 28.01, MAE: 19.58
  
  **Speed_Upgrades (Linear Regression):**
  - Test Accuracy: 80.2% (R² = 0.802)
  - RMSE: 46.28, MAE: 30.82
  
  The visualization shows actual vs predicted values with 95% confidence intervals..."
- 🖼️ Shows the PNG chart inline

### Example 2: December 2025 Predictions

**User:** "What are the December 2025 sales predictions?"

**Claude/Cursor:**
- 🔧 Calls `predict_december_2025(include_stats=true)`
- ⏳ Generates forecasts (20-30 seconds)
- 📈 Receives summary and PNG
- 💬 Displays: "Here are the December 2025 sales forecasts:
  
  **VAS_Sold:**
  - Total for December: 12,450
  - Daily Average: 401.6
  - Peak Day: Dec 10 (620 sales with 175K push notifications)
  
  **Speed_Upgrades:**
  - Total for December: 8,920
  - Daily Average: 287.7
  - Peak Day: Dec 18 (380 upgrades with 250K emails)
  
  The cumulative chart shows strong growth aligned with marketing campaigns..."
- 🖼️ Shows the cumulative forecast chart with campaign markers

### Example 3: Quick Visualization (No Stats)

**User:** "Show me just the hybrid model chart without all the statistics"

**Claude/Cursor:**
- Calls `analyze_hybrid_model(include_stats=false)`
- Displays the chart with brief explanation

### Example 4: Follow-up Analysis

**User:** "Predict December 2025 sales"  
**Claude:** [Shows forecast chart and summary]

**User:** "Which days have the highest predicted sales?"  
**Claude:** "Based on the predictions, the top 5 days are:
  1. December 10: 620 VAS sales (175K push notifications)
  2. December 15: 580 VAS sales (150K push notifications)..."

**User:** "How do the marketing campaigns affect sales?"  
**Claude:** "The correlation is clear - days with large push notification campaigns (marked with gold stars on the chart) show significant spikes in VAS sales..."

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
# Press Ctrl+C to stop
```

### 4. Restart After Changes
Always completely quit and restart the LLM client after changing configuration.

### 5. Check File Permissions
Ensure the Python executable and script are readable/executable.

## Security Considerations

### What the Server Can Do

✅ **Allowed:**
- Read CSV data from `telecom-sales-predictor` directory
- Run the two analysis scripts
- Generate PNG and CSV files in `output_files/`
- Return results to the LLM

❌ **Cannot:**
- Access files outside the project directory
- Make network requests
- Modify system files
- Execute arbitrary commands

### Safe Usage

- The server only runs the specific analysis scripts
- No arbitrary code execution
- Runs in the context of your user account
- Same permissions as running the scripts manually

### Data Privacy

- Data stays on your local machine
- No data sent to external services
- PNG and CSV generated locally
- Results only sent to the LLM client you're using
- MCP protocol ensures secure local communication

## Updating the Server

### When you modify `mcp_server.py`:

1. **Save changes** to the file
2. **No need to reinstall** dependencies (unless adding new ones)
3. **Restart the LLM client** to reload the server
4. **Test** with a simple query

### When you modify analysis scripts:

- No changes needed to MCP server
- Just restart the LLM client
- The server will call the updated scripts

### Migration from Old Version

**Good News:** If you already had the server configured:
- ✅ Same endpoint (`telecom-predictor`)
- ✅ Same configuration format
- ✅ No config file changes needed
- ✅ Just restart your LLM client
- ✅ Two tools will appear automatically

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

## Verification Checklist

Before adding to your LLM client:

✅ Python 3.10+ installed  
✅ Virtual environment created  
✅ Dependencies installed  
✅ Both scripts exist and run successfully:
  - `analyze_data_hybrid.py` ✓
  - `predict_december_2025.py` ✓  
✅ Both data files exist:
  - `final_dataset.csv` ✓
  - `test_dataset_dec_2025.csv` ✓  
✅ Server starts without crashes  
✅ Absolute paths in config file  
✅ JSON syntax is valid

After adding to your LLM client:

✅ Configuration file saved  
✅ LLM client completely restarted  
✅ **Two tools** appear in tool list  
✅ Test queries work  
✅ PNGs display correctly (200-400 KB)  
✅ Statistics are accurate  
✅ No timeout errors

## Next Steps

1. ✅ Add the server to Cursor or Claude
2. 🧪 Test both tools with sample queries
3. 📊 Use for real analysis and forecasting
4. 📚 Explore `../telecom-sales-predictor/__docs__/` for model details
5. 🔧 Customize as needed
6. 🚀 Build more MCP tools!

## Quick Reference

### Tool 1: analyze_hybrid_model
**Purpose:** Train and evaluate ML models  
**Output:** Performance metrics + Test set visualization  
**Image Size:** ~402 KB  
**Accuracy:** 83.3% average (VAS: 86.4%, Speed: 80.2%)

### Tool 2: predict_december_2025
**Purpose:** Forecast December 2025 sales  
**Output:** Prediction summary + Cumulative forecast chart  
**Image Size:** ~208 KB  
**Features:** Campaign day markers, top performing days

## Additional Resources

- **MCP Documentation**: https://modelcontextprotocol.io/
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **Setup Instructions**: See `instructions.md`
- **Model Details**: See `../telecom-sales-predictor/__docs__/`
- **Changelog**: See `CHANGELOG_MCP_UPDATE.md`
- **Cursor Docs**: https://docs.cursor.com/
- **Claude API**: https://docs.anthropic.com/

## Success Indicators

✅ Configuration file created/updated  
✅ Paths are absolute and correct  
✅ JSON syntax is valid  
✅ LLM client restarted  
✅ **Two tools** appear in tool list  
✅ Test queries work for both tools  
✅ PNGs display correctly  
✅ Statistics are accurate  
✅ Images are 200-400 KB (not 1-2 MB)  
✅ Timestamped files in `output_files/`

Congratulations! Your MCP server is now integrated. 🎉

---

**Questions or Issues?**

1. Check `instructions.md` for detailed setup
2. Review `CHANGELOG_MCP_UPDATE.md` for what changed
3. Verify paths in configuration
4. Look at LLM client logs for errors
5. Test the server manually first
6. Ensure both data files exist

**Happy predicting with your dual-tool MCP server!** 📊🔮🚀
