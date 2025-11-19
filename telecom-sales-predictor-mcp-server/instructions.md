# Running the Telecom Sales Predictor MCP Server

This guide explains how to set up and run the MCP server that exposes telecom sales prediction analysis as **two specialized tools** for LLM clients.

## Overview

This MCP server allows LLM clients (like Claude or Cursor) to:
1. **Train & Evaluate** hybrid ML models (Random Forest + Linear Regression)
2. **Forecast December 2025** sales based on planned marketing campaigns
3. Generate visualizations showing actual vs predicted values
4. Receive optimized PNG charts (200-400 KB) directly as base64-encoded images
5. Get detailed model performance statistics and predictions

## What's New (November 2025 Update)

### Major Changes
- ✨ **Two Tools**: `analyze_hybrid_model` and `predict_december_2025`
- 🤖 **Hybrid Models**: Random Forest (86.4%) + Linear Regression (80.2%)
- 🔮 **Future Forecasting**: Predict December 2025 based on marketing plans
- 📏 **Optimized Images**: 200-400 KB (down from 1-2 MB) for MCP compatibility
- 📝 **Timestamped Outputs**: Unique filenames in `output_files/` directory

## Prerequisites

### Required Software
- **Python 3.10+** (MCP SDK requires 3.10 or higher)
- **pip** (Python package installer)
- **Virtual environment** (recommended)

### Required Files
The MCP server depends on files in the adjacent `telecom-sales-predictor` directory:
- `../telecom-sales-predictor/analyze_data_hybrid.py` - Hybrid model analysis script (renamed from `analyze_data.py`)
- `../telecom-sales-predictor/predict_december_2025.py` - December 2025 forecasting script (new)
- `../telecom-sales-predictor/final_dataset.csv` - Historical training data (Sep 2024 - Oct 2025)
- `../telecom-sales-predictor/test_dataset_dec_2025.csv` - December 2025 test data with marketing campaigns
- `../telecom-sales-predictor/output_files/` - Directory for outputs (created automatically)

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
cd /path/to/predict-o-matic/telecom-sales-predictor-mcp-server
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

# Check that both analysis scripts exist
ls -la ../telecom-sales-predictor/analyze_data_hybrid.py
ls -la ../telecom-sales-predictor/predict_december_2025.py

# Check that data files exist
ls -la ../telecom-sales-predictor/final_dataset.csv
ls -la ../telecom-sales-predictor/test_dataset_dec_2025.csv
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

### Option 1: Test Analysis Scripts Directly

Before testing the MCP server, verify the underlying scripts work:

```bash
# Test hybrid model analysis
cd ../telecom-sales-predictor
source venv/bin/activate  # Or use ./venv/bin/python
python analyze_data_hybrid.py

# Should output model metrics and create PNG:
# output_files/model_predictions_hybrid_final_<timestamp>.png

# Test December prediction
python predict_december_2025.py

# Should output predictions and create:
# output_files/december_2025_predictions_<timestamp>.csv
# output_files/december_2025_predictions_chart_<timestamp>.png
```

### Option 2: Using the MCP Inspector (Recommended)

The MCP Inspector is a tool for testing MCP servers:

```bash
# Install the MCP Inspector globally
npm install -g @modelcontextprotocol/inspector

# Run the inspector with your server
npx @modelcontextprotocol/inspector python mcp_server.py
```

This opens a web UI where you can:
- View available tools (should see 2 tools)
- Test tool calls for both `analyze_hybrid_model` and `predict_december_2025`
- See responses (including images)
- Debug issues

### Option 3: Integration Testing

The best test is to configure it in Cursor/Claude and try using it:

1. Add the server to your MCP configuration (see `ADD_MCP_SERVER.md`)
2. Restart the LLM client
3. Ask: "Analyze the telecom sales data with the hybrid model"
4. Ask: "Predict December 2025 sales"
5. The LLM should call the appropriate tool and display the PNG chart

## What the Tools Do

### Tool 1: `analyze_hybrid_model`

When an LLM calls this tool:

1. **Runs Analysis**: Executes `../telecom-sales-predictor/analyze_data_hybrid.py`
2. **Trains Models**: 
   - Random Forest for VAS_Sold (86.4% accuracy)
   - Linear Regression for Speed_Upgrades (80.2% accuracy)
3. **Evaluates**: Tests on Aug-Oct 2025 data
4. **Generates Visualization**: Creates PNG with actual vs predicted values and confidence intervals
5. **Returns Results**: Sends back:
   - Text: Model performance metrics (R², RMSE, MAE for both models)
   - Image: PNG chart (~402 KB, optimized for MCP)

**Parameters:**
- `include_stats` (boolean, optional): Whether to include detailed statistics
  - Default: `true`

**Example LLM Interaction:**

**User:** "Analyze the telecom sales data using the hybrid model"

**LLM calls:** `analyze_hybrid_model(include_stats=true)`

**Server returns:**
- ✅ Text summary with R² scores (VAS: 86.4%, Speed: 80.2%)
- 📊 PNG visualization with 95% confidence intervals

**LLM displays:** The chart inline with detailed performance analysis

### Tool 2: `predict_december_2025`

When an LLM calls this tool:

1. **Trains Models**: On historical data (Sep 2024 - Oct 2025)
2. **Loads Test Data**: December 2025 with planned marketing campaigns
3. **Generates Predictions**: Daily forecasts for both channels (App/Web)
4. **Creates Visualizations**: Cumulative chart with campaign day markers
5. **Returns Results**: Sends back:
   - Text: Prediction summary (totals, averages, top 5 days)
   - Text: Optional CSV data if requested
   - Image: PNG cumulative chart (~208 KB)

**Parameters:**
- `include_stats` (boolean, optional): Include detailed statistics. Default: `true`
- `return_csv` (boolean, optional): Return full CSV content. Default: `false`

**Example LLM Interaction:**

**User:** "What are the December 2025 sales predictions?"

**LLM calls:** `predict_december_2025(include_stats=true, return_csv=false)`

**Server returns:**
- ✅ Text summary: "Total VAS: 12,450, Total Upgrades: 8,920"
- ✅ Top 5 performing days with marketing campaign details
- 📊 PNG cumulative chart with campaign markers

**LLM displays:** The forecast chart inline with marketing insights

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

### Error: "analyze_data_hybrid.py not found"

**Solution:** The script was renamed from `analyze_data.py`

```bash
# You should have this structure:
predict-o-matic/
├── telecom-sales-predictor/
│   ├── analyze_data_hybrid.py    # Renamed!
│   ├── predict_december_2025.py  # New!
│   ├── final_dataset.csv
│   ├── test_dataset_dec_2025.csv
│   └── output_files/              # Generated outputs
└── telecom-sales-predictor-mcp-server/
    └── mcp_server.py

# Verify paths
ls -la ../telecom-sales-predictor/analyze_data_hybrid.py
ls -la ../telecom-sales-predictor/predict_december_2025.py
```

### Error: "test_dataset_dec_2025.csv not found"

**Solution:** Generate the December test dataset

```bash
cd ../telecom-sales-predictor
source venv/bin/activate
python create_test_dataset_updated.py

# This creates test_dataset_dec_2025.csv with marketing campaigns
```

### Error: "Data file not found"

**Solution:** Ensure both CSV files exist

```bash
ls -la ../telecom-sales-predictor/final_dataset.csv
ls -la ../telecom-sales-predictor/test_dataset_dec_2025.csv

# If missing, you need to generate or obtain the data files
```

### Error: "PNG file was not generated"

**Possible causes:**
1. Analysis script failed to run
2. matplotlib not properly installed
3. Permission issues in `output_files/` directory

**Solution:**

```bash
# Test the scripts directly first
cd ../telecom-sales-predictor
source venv/bin/activate

# Test hybrid analysis
python analyze_data_hybrid.py
ls -la output_files/model_predictions_hybrid_final_*.png

# Test December prediction
python predict_december_2025.py
ls -la output_files/december_2025_predictions_chart_*.png
```

### Error: "Process timed out"

The server has a 90-second timeout (increased from 60 for hybrid models).

**Solution:** If analysis takes longer, edit `mcp_server.py`:

```python
timeout=120,  # Increase from 90 to 120 seconds
```

### Server shows only one tool instead of two

**Solution:** Check your MCP server version

```bash
# Make sure you're using the updated mcp_server.py
grep -c "analyze_hybrid_model" mcp_server.py
grep -c "predict_december_2025" mcp_server.py
# Both should return > 0

# Restart your LLM client after updating
```

### Server doesn't respond in Cursor/Claude

**Checklist:**
1. ✅ Virtual environment activated before running
2. ✅ Python 3.10+ being used
3. ✅ MCP config file syntax is correct
4. ✅ Path to mcp_server.py is absolute
5. ✅ Both analysis scripts exist
6. ✅ Restart Cursor/Claude after config changes

**Debug steps:**

```bash
# Test the server manually
cd telecom-sales-predictor-mcp-server
source venv/bin/activate
python mcp_server.py

# Check for any error messages
# Should not crash immediately
# Press Ctrl+C to stop
```

## File Structure

```
telecom-sales-predictor-mcp-server/
├── mcp_server.py           # Main MCP server (2 tools)
├── requirements.txt        # Python dependencies
├── instructions.md         # This file
├── ADD_MCP_SERVER.md      # How to add to Cursor/Claude
├── README.md              # Overview and features
├── venv/                  # Virtual environment (after setup)
│   ├── bin/
│   ├── lib/
│   └── ...
└── mcp_config.json        # Example configuration
```

## How It Works

### Architecture for Hybrid Analysis

```
LLM Client (Claude/Cursor)
    ↓ (MCP Protocol via stdio)
    ↓ Calls: analyze_hybrid_model
MCP Server (mcp_server.py)
    ↓ (subprocess call)
Analysis Script (analyze_data_hybrid.py)
    ↓ (reads final_dataset.csv)
    ↓ (trains Random Forest + Linear Regression)
    ↓ (generates timestamped PNG)
output_files/model_predictions_hybrid_final_<timestamp>.png
    ↓ (server finds most recent file)
    ↓ (read and base64 encode)
MCP Server
    ↓ (returns ImageContent + TextContent)
LLM Client (displays chart and metrics)
```

### Architecture for December Prediction

```
LLM Client (Claude/Cursor)
    ↓ (MCP Protocol via stdio)
    ↓ Calls: predict_december_2025
MCP Server (mcp_server.py)
    ↓ (subprocess call)
Prediction Script (predict_december_2025.py)
    ↓ (reads final_dataset.csv for training)
    ↓ (reads test_dataset_dec_2025.csv for prediction)
    ↓ (generates predictions + timestamped files)
output_files/december_2025_predictions_<timestamp>.csv
output_files/december_2025_predictions_chart_<timestamp>.png
    ↓ (server finds most recent files)
    ↓ (read CSV and PNG, base64 encode)
MCP Server
    ↓ (returns ImageContent + TextContent)
LLM Client (displays forecast chart and summary)
```

### Key Components

1. **Server Registration**: `@app.list_tools()` declares 2 available tools
2. **Tool Handler**: `@app.call_tool()` routes to appropriate handler
3. **Subprocess Execution**: Runs analysis or prediction script
4. **File Discovery**: Uses glob patterns to find most recent timestamped files
5. **File Reading**: Loads generated PNG (and CSV if requested)
6. **Base64 Encoding**: Converts binary images to strings
7. **Response Construction**: Creates TextContent + ImageContent
8. **Stdio Communication**: Sends response via MCP protocol

## Performance Notes

- **First Run Hybrid Analysis**: 20-30 seconds (Random Forest + Linear Regression training)
- **First Run December Prediction**: 20-30 seconds (training + forecasting)
- **Subsequent Runs**: Same time (models retrain each time for fresh forecasts)
- **Memory**: ~300-500 MB during execution
- **Timeout**: 90 seconds (increased from 60, configurable)
- **Image Sizes**: 200-400 KB (optimized for MCP, down from 1-2 MB)

## Migration from Old Version

If you were using the old single-tool version:

### What Changed
1. ✨ **Two tools** instead of one
2. 📝 `analyze_data.py` → `analyze_data_hybrid.py` (renamed)
3. 🆕 `predict_december_2025.py` (new tool)
4. 📂 Outputs in `output_files/` with timestamps
5. 📏 Images optimized to 200-400 KB

### What Stays the Same
- ✅ Same MCP server endpoint
- ✅ Same `mcp_config.json` format
- ✅ No client configuration changes needed
- ✅ Just restart your LLM client

## Next Steps

1. ✅ Complete this setup guide
2. 📝 Read `ADD_MCP_SERVER.md` to integrate with Cursor or Claude
3. 🧪 Test both tools with simple queries
4. 📚 Review `../telecom-sales-predictor/__docs__/` for model details
5. 🚀 Use it for telecom sales analysis and forecasting!

## Advanced Usage

### Custom Configuration

You can modify `mcp_server.py` to:
- Change timeout values (currently 90 seconds)
- Adjust response formatting
- Add additional tools
- Filter or transform the output
- Enable/disable CSV returns by default

### Environment Variables

Create a `.env` file for custom settings:

```bash
# .env
ANALYSIS_TIMEOUT=120
PREDICTION_TIMEOUT=120
DEBUG_MODE=false
OUTPUT_DIR=/custom/path/output_files
```

Then load in `mcp_server.py`:

```python
from dotenv import load_dotenv
import os

load_dotenv()
timeout = int(os.getenv('ANALYSIS_TIMEOUT', 90))
```

### Adding More Tools

You can add more tools to the same server:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="analyze_hybrid_model", ...),
        Tool(name="predict_december_2025", ...),
        Tool(name="compare_models", ...),         # New!
        Tool(name="forecast_next_quarter", ...),  # New!
    ]
```

## Getting Help

- **MCP Documentation**: https://modelcontextprotocol.io/
- **Python MCP SDK**: https://github.com/modelcontextprotocol/python-sdk
- **Project Documentation**: `../telecom-sales-predictor/__docs__/`
- **Issues**: Check the analysis scripts first
- **Debugging**: Use the MCP Inspector for detailed diagnostics

## Success Criteria

You'll know everything is working when:

✅ Virtual environment created with Python 3.10+  
✅ Dependencies installed without errors  
✅ Server runs without crashing  
✅ **Two tools** appear in LLM client tool list  
✅ Both analysis scripts can be called successfully  
✅ PNG charts are generated (200-400 KB each)  
✅ Timestamped files appear in `output_files/`  
✅ LLM client can discover and call both tools  
✅ Visualizations display correctly in the client  
✅ December predictions include campaign markers

Happy predicting! 📊🔮🚀
