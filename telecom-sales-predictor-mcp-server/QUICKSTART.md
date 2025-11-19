# Quick Start Guide

Get the Telecom Sales Predictor MCP Server running in 5 minutes.

## ✨ What's New

**November 2025 Update:**
- 🔧 Two tools instead of one
- 🤖 Hybrid ML models (Random Forest + Linear Regression)
- 🔮 December 2025 forecasting capability
- 📏 Optimized images (200-400 KB, MCP-compatible)
- 📝 No configuration changes needed!

## Prerequisites

- Python 3.10 or higher
- The adjacent `telecom-sales-predictor` directory with:
  - `analyze_data_hybrid.py` (renamed from `analyze_data.py`)
  - `predict_december_2025.py` (new)
  - `final_dataset.csv`
  - `test_dataset_dec_2025.csv` (for December predictions)

## Setup (Automated)

```bash
cd telecom-sales-predictor-mcp-server
./setup.sh
```

The setup script will:
1. Check Python version (must be 3.10+)
2. Create virtual environment
3. Install all dependencies
4. Run verification tests
5. Verify both analysis scripts exist

## Setup (Manual)

```bash
cd telecom-sales-predictor-mcp-server

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify setup
python -c "import mcp; print('MCP SDK installed successfully')"
```

## Test the Scripts

Before configuring the MCP server, verify the underlying scripts work:

```bash
cd ../telecom-sales-predictor
source venv/bin/activate  # Or use ./venv/bin/python

# Test 1: Hybrid model analysis
python analyze_data_hybrid.py
# Should print metrics and create PNG in output_files/

# Test 2: December predictions
python predict_december_2025.py
# Should print summary and create CSV + PNG in output_files/

# Verify outputs
ls -lh output_files/*.png
ls -lh output_files/*.csv
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

**Replace paths** with your actual absolute paths:
```bash
# Get the correct paths
echo "Command: $(pwd)/venv/bin/python"
echo "Args: $(pwd)/mcp_server.py"
```

**Example:**
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

Use the same path replacement strategy as Cursor above.

## Restart & Test

1. **Restart** Cursor or Claude Desktop
2. **Verify** the server is loaded (check logs or settings)
3. **Ask:** "What tools do you have available?"
   - Should see `analyze_hybrid_model` and `predict_december_2025`

## Try the Tools

### Tool 1: Hybrid Model Analysis

Ask:
```
"Analyze the telecom sales data using the hybrid model"
"Show me the model performance"
"Train and evaluate the predictive models"
```

**Expected Result:**
- Performance metrics for Random Forest and Linear Regression
- PNG chart with actual vs predicted values (Aug-Oct 2025)
- 95% confidence intervals
- ~402 KB image

### Tool 2: December 2025 Predictions

Ask:
```
"Predict December 2025 sales"
"What are the December forecasts?"
"Generate December 2025 predictions with marketing campaigns"
```

**Expected Result:**
- Summary: Total sales, daily averages, top 5 days
- Cumulative PNG chart with campaign day markers
- ~208 KB image
- Marketing campaign correlation insights

## Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| "Python 3.10+ required" | `brew install python@3.11` (macOS) or upgrade Python |
| "analyze_data_hybrid.py not found" | Script was renamed - check it exists |
| "test_dataset_dec_2025.csv not found" | Run `create_test_dataset_updated.py` |
| "Only 1 tool appears" | Restart LLM client after server update |
| "Process timeout" | Normal for first run (90 sec limit) |
| "Image too large" | Already optimized to 100 DPI (200-400 KB) |

## Verification Commands

```bash
# 1. Check Python version
python3 --version  # Must be 3.10+

# 2. Check MCP installation
source venv/bin/activate
python -c "import mcp; print('✓ MCP SDK installed')"

# 3. Check scripts exist
ls -la ../telecom-sales-predictor/analyze_data_hybrid.py
ls -la ../telecom-sales-predictor/predict_december_2025.py

# 4. Check data files exist
ls -la ../telecom-sales-predictor/final_dataset.csv
ls -la ../telecom-sales-predictor/test_dataset_dec_2025.csv

# 5. Test server syntax
python -m py_compile mcp_server.py
echo "✓ Server syntax valid"

# 6. Run server (should not crash)
python mcp_server.py
# Press Ctrl+C to stop
```

## File Size Verification

After running the tools, check that images are optimized:

```bash
ls -lh ../telecom-sales-predictor/output_files/*.png

# Should see files around 200-400 KB, not 1-2 MB
# Example output:
# -rw-r--r-- 1 user staff 402K model_predictions_hybrid_final_<timestamp>.png
# -rw-r--r-- 1 user staff 208K december_2025_predictions_chart_<timestamp>.png
```

## Success Indicators

You'll know it's working when:

✅ Server starts without errors  
✅ **Two tools** appear in Cursor/Claude  
✅ Hybrid analysis returns metrics + chart  
✅ December predictions return forecast + chart  
✅ Images display inline in conversation  
✅ File sizes are 200-400 KB (not 1-2 MB)  
✅ Timestamped files in `output_files/`  
✅ No timeout errors (90 sec limit)

## Getting Help

- **Setup Issues**: See `instructions.md`
- **Configuration**: See `ADD_MCP_SERVER.md`
- **Model Details**: See `../telecom-sales-predictor/__docs__/`
- **Changes**: See `CHANGELOG_MCP_UPDATE.md`
- **MCP Protocol**: https://modelcontextprotocol.io/

## Next Steps

Once working:

1. 📊 Try different queries to test both tools
2. 📈 Explore the model performance metrics
3. 🔮 Generate December forecasts with different scenarios
4. 📚 Review detailed docs in `../telecom-sales-predictor/__docs__/`
5. 🚀 Use for real telecom sales analysis!

---

**Total Setup Time:** ~5 minutes  
**Tools Available:** 2 (Hybrid Analysis + December Forecast)  
**Image Sizes:** 200-400 KB (MCP-optimized)  
**Accuracy:** 83.3% average

Happy predicting! 📊🔮🚀
