# Running the Telecom Sales Predictor MCP Server

This guide explains how to set up and run the MCP server that exposes the telecom sales prediction analysis as a tool for LLM clients.

## Overview

This MCP server allows LLM clients (like Claude or Cursor) to:
1. Run predictive analysis on telecom sales data
2. Generate visualizations showing actual vs predicted values
3. Receive PNG charts directly as base64-encoded images
4. Get detailed model performance statistics

## Prerequisites

### Required Software
- **Python 3.10+** (MCP SDK requires 3.10 or higher)
- **pip** (Python package installer)
- **Virtual environment** (recommended)

### Required Files
The MCP server depends on files in the adjacent `telecom-sales-predictor` directory:
- `../telecom-sales-predictor/analyze_data.py` - The analysis script
- `../telecom-sales-predictor/final_dataset.csv` - The data file

Make sure these files exist before running the server.

### Check Your Python Version
```bash
python3 --version
# Must show: Python 3.10.x or higher
```

If you have an older Python version, you'll need to upgrade or use pyenv/conda to get Python 3.10+.

## Setup Instructions

### Step 1: Navigate to the MCP Server Directory

```bash
cd /Users/vishalkumar/code/frontier/predict-o-matic/telecom-sales-predictor-mcp-server
```

### Step 2: Create a Virtual Environment

**IMPORTANT:** Use Python 3.10 or higher!

```bash
# Create virtual environment with Python 3.10+
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- `mcp` - The MCP SDK for server implementation
- `python-dotenv` - For environment variables
- Data science libraries (pandas, numpy, scikit-learn, matplotlib)

### Step 4: Verify Installation

```bash
# Check that MCP is installed
python -c "import mcp; print(f'MCP version: {mcp.__version__}')"

# Check that the analysis script exists
ls -la ../telecom-sales-predictor/analyze_data.py

# Check that the data file exists
ls -la ../telecom-sales-predictor/final_dataset.csv
```

All checks should pass without errors.

## Running the MCP Server

### Local Testing (Manual Mode)

You can test the server manually using stdin/stdout:

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the server
python mcp_server.py
```

The server will wait for MCP protocol messages on stdin. This is mainly for debugging.

**To stop:** Press `Ctrl+C`

### Integration with LLM Clients

For actual use with Claude or Cursor, see the `ADD_MCP_SERVER.md` file for configuration instructions.

The MCP server communicates via stdio (standard input/output), which is the standard way MCP servers work.

## Testing the Server

### Option 1: Using the MCP Inspector (Recommended)

The MCP Inspector is a tool for testing MCP servers:

```bash
# Install the MCP Inspector globally
npm install -g @modelcontextprotocol/inspector

# Run the inspector with your server
npx @modelcontextprotocol/inspector python mcp_server.py
```

This opens a web UI where you can:
- View available tools
- Test tool calls
- See responses (including images)
- Debug issues

### Option 2: Manual Testing with Python

Create a simple test script:

```python
import subprocess
import json
import sys

# Start the MCP server
proc = subprocess.Popen(
    [sys.executable, 'mcp_server.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Send a tool call request (simplified)
# In reality, you'd follow the full MCP protocol
# This is just to demonstrate the concept
```

### Option 3: Integration Testing

The best test is to configure it in Cursor/Claude and try using it:

1. Add the server to your MCP configuration (see `ADD_MCP_SERVER.md`)
2. Restart the LLM client
3. Ask: "Generate sales predictions for the telecom data"
4. The LLM should call the tool and display the PNG chart

## What the Tool Does

When an LLM calls the `generate_sales_predictions` tool:

1. **Runs Analysis**: Executes `../telecom-sales-predictor/analyze_data.py`
2. **Trains Models**: Builds linear regression models for VAS_Sold and Speed_Upgrades
3. **Generates Visualization**: Creates a PNG chart with actual vs predicted values
4. **Returns Results**: Sends back:
   - Text: Model performance metrics (R², RMSE, MAE)
   - Image: PNG chart (base64-encoded)

### Tool Parameters

- `include_stats` (boolean, optional): Whether to include detailed statistics
  - Default: `true`
  - Set to `false` for just the visualization

### Example LLM Interaction

**User:** "Show me the sales predictions for telecom products"

**LLM calls:** `generate_sales_predictions(include_stats=true)`

**Server returns:**
- ✅ Text summary with R² scores and model metrics
- 📊 PNG visualization showing actual vs predicted values with confidence intervals

**LLM displays:** The chart inline with an explanation of the results

## Troubleshooting

### Error: "MCP SDK requires Python 3.10 or higher"

**Solution:** Upgrade Python or use a Python version manager

```bash
# Check your Python version
python3 --version

# If using Homebrew (macOS)
brew install python@3.11

# Create venv with specific Python version
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "Analysis script not found"

**Solution:** Make sure the directory structure is correct

```bash
# You should have this structure:
predict-o-matic/
├── telecom-sales-predictor/
│   ├── analyze_data.py
│   └── final_dataset.csv
└── telecom-sales-predictor-mcp-server/
    └── mcp_server.py

# Verify paths
ls -la ../telecom-sales-predictor/analyze_data.py
```

### Error: "Data file not found"

**Solution:** Ensure `final_dataset.csv` exists

```bash
ls -la ../telecom-sales-predictor/final_dataset.csv

# If missing, you need to generate or obtain the data file
```

### Error: "PNG file was not generated"

**Possible causes:**
1. Analysis script failed to run
2. matplotlib not properly installed
3. Permission issues

**Solution:**

```bash
# Test the analysis script directly first
cd ../telecom-sales-predictor
source venv/bin/activate
python analyze_data.py

# Should create model_predictions_test_set.png
ls -la model_predictions_test_set.png
```

### Error: "Process timed out"

The server has a 60-second timeout. If the analysis takes longer:

**Solution:** Edit `mcp_server.py` and increase the timeout:

```python
timeout=120,  # Increase from 60 to 120 seconds
```

### Server doesn't respond in Cursor/Claude

**Checklist:**
1. ✅ Virtual environment activated before running
2. ✅ Python 3.10+ being used
3. ✅ MCP config file syntax is correct
4. ✅ Path to mcp_server.py is absolute
5. ✅ Restart Cursor/Claude after config changes

**Debug steps:**

```bash
# Test the server manually
cd telecom-sales-predictor-mcp-server
source venv/bin/activate
python mcp_server.py

# Check for any error messages
# Press Ctrl+C to stop
```

## File Structure

```
telecom-sales-predictor-mcp-server/
├── mcp_server.py           # Main MCP server implementation
├── requirements.txt        # Python dependencies
├── instructions.md         # This file
├── ADD_MCP_SERVER.md      # How to add to Cursor/Claude
├── venv/                  # Virtual environment (after setup)
│   ├── bin/
│   ├── lib/
│   └── ...
└── mcp_config.json        # Example configuration
```

## How It Works

### Architecture

```
LLM Client (Claude/Cursor)
    ↓ (MCP Protocol via stdio)
MCP Server (mcp_server.py)
    ↓ (subprocess call)
Analysis Script (analyze_data.py)
    ↓ (reads CSV, generates PNG)
PNG File (model_predictions_test_set.png)
    ↓ (read and base64 encode)
MCP Server
    ↓ (returns ImageContent + TextContent)
LLM Client (displays chart and stats)
```

### Key Components

1. **Server Registration**: `@app.list_tools()` declares available tools
2. **Tool Handler**: `@app.call_tool()` processes requests
3. **Subprocess Execution**: Runs the analysis script
4. **File Reading**: Loads the generated PNG
5. **Base64 Encoding**: Converts binary image to string
6. **Response Construction**: Creates TextContent + ImageContent
7. **Stdio Communication**: Sends response via MCP protocol

## Performance Notes

- **First Run**: 10-15 seconds (model training + visualization)
- **Subsequent Runs**: 10-15 seconds (script reruns each time)
- **Memory**: ~200MB during execution
- **Timeout**: 60 seconds (configurable)

## Next Steps

1. ✅ Complete this setup guide
2. 📝 Read `ADD_MCP_SERVER.md` to integrate with Cursor or Claude
3. 🧪 Test the tool with simple queries
4. 🚀 Use it for telecom sales analysis!

## Advanced Usage

### Custom Configuration

You can modify `mcp_server.py` to:
- Change timeout values
- Adjust response formatting
- Add additional tools
- Filter or transform the output

### Environment Variables

Create a `.env` file for custom settings:

```bash
# .env
ANALYSIS_TIMEOUT=120
DEBUG_MODE=false
```

Then load in `mcp_server.py`:

```python
from dotenv import load_dotenv
import os

load_dotenv()
timeout = int(os.getenv('ANALYSIS_TIMEOUT', 60))
```

### Multiple Tools

You can add more tools to the same server:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="generate_sales_predictions", ...),
        Tool(name="analyze_trends", ...),
        Tool(name="forecast_next_month", ...),
    ]
```

## Getting Help

- **MCP Documentation**: https://modelcontextprotocol.io/
- **Python MCP SDK**: https://github.com/modelcontextprotocol/python-sdk
- **Issues**: Check the analysis script first (`../telecom-sales-predictor/analyze_data.py`)
- **Debugging**: Use the MCP Inspector for detailed diagnostics

## Success Criteria

You'll know everything is working when:

✅ Virtual environment created with Python 3.10+  
✅ Dependencies installed without errors  
✅ Server runs without crashing  
✅ Analysis script can be called successfully  
✅ PNG chart is generated and returned  
✅ LLM client can discover and call the tool  
✅ Visualization displays correctly in the client

Happy predicting! 📊🚀

