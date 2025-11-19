# Telecom Sales Predictor MCP Server

An MCP (Model Context Protocol) server that exposes telecom sales predictive analytics as **two specialized tools** for LLM clients like Claude and Cursor.

## What This Does

This MCP server allows LLMs to:
- 📊 **Train & Evaluate** hybrid ML models (Random Forest + Linear Regression) - 83.3% average accuracy
- 🔮 **Forecast December 2025** sales based on planned marketing campaigns
- 🎯 Analyze VAS (Value-Added Services) sales and Speed Upgrades
- 📈 Create visualizations with actual vs predicted values
- 📉 Return optimized PNG charts (200-400 KB, MCP-compatible)
- 📋 Provide detailed model performance metrics (R², RMSE, MAE)

## What's New (Updated November 2025)

### ✨ Major Changes
- **Two Tools Instead of One**: Separate tools for analysis vs prediction
- **Hybrid Model**: Random Forest (86.4% for VAS) + Linear Regression (80.2% for Speed Upgrades)
- **December 2025 Forecasting**: Generate future sales predictions based on marketing plans
- **Optimized Images**: Charts are now 200-400 KB (down from 1-2 MB) for MCP compatibility
- **Timestamped Outputs**: All files have unique timestamps for version tracking

## Architecture

```
LLM Client (Claude/Cursor)
    ↓ MCP Protocol
MCP Server (this project) - Exposes 2 Tools
    ↓ Subprocess (Tool 1)
analyze_data_hybrid.py → Trains Hybrid Model → PNG (402 KB)
    ↓ Subprocess (Tool 2)
predict_december_2025.py → Forecasts Dec 2025 → CSV + PNG (208 KB)
    ↓ Base64 Encode
LLM Client (displays charts & predictions)
```

## Quick Start

### 1. Setup

```bash
# Navigate to this directory
cd telecom-sales-predictor-mcp-server

# Create virtual environment (requires Python 3.10+)
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Test

```bash
# Verify the server can run
python mcp_server.py
# Press Ctrl+C to stop

# Verify required files exist
ls -la ../telecom-sales-predictor/analyze_data_hybrid.py
ls -la ../telecom-sales-predictor/predict_december_2025.py
ls -la ../telecom-sales-predictor/final_dataset.csv
ls -la ../telecom-sales-predictor/test_dataset_dec_2025.csv
```

### 3. Configure

Add to Cursor or Claude Desktop:

**For Cursor:** Edit `~/.cursor/mcp.json`  
**For Claude Desktop:** Edit `~/Library/Application Support/Claude/claude_desktop_config.json`

Use the configuration from `mcp_config.json` (update paths for your system).

**Important:** The server endpoint remains the same - no changes needed to your client configuration if already set up!

### 4. Use

Restart your LLM client, then ask:

**For Hybrid Model Analysis:**
```
"Analyze the telecom sales data using the hybrid model"
"Show me the model performance on the test set"
"Train and evaluate the predictive models"
```

**For December 2025 Predictions:**
```
"Predict December 2025 sales"
"Generate December forecasts based on marketing campaigns"
"Show me the December 2025 sales predictions"
```

## Documentation

| File | Description |
|------|-------------|
| **[instructions.md](instructions.md)** | Complete setup and usage guide |
| **[ADD_MCP_SERVER.md](ADD_MCP_SERVER.md)** | How to integrate with Cursor/Claude |
| **[mcp_config.json](mcp_config.json)** | Example configuration file |
| **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** | Technical implementation details |

## Requirements

- **Python 3.10+** (MCP SDK requirement)
- **Virtual Environment** (recommended)
- **Adjacent telecom-sales-predictor directory** with:
  - `analyze_data_hybrid.py` - Hybrid model analysis script
  - `predict_december_2025.py` - December forecast script
  - `final_dataset.csv` - Historical training data (Sep 2024 - Oct 2025)
  - `test_dataset_dec_2025.csv` - December 2025 test data with marketing plans
  - `output_files/` - Directory for generated visualizations (created automatically)

## Project Structure

```
predict-o-matic/
├── telecom-sales-predictor/             # Analysis project
│   ├── analyze_data_hybrid.py           # Hybrid model training
│   ├── predict_december_2025.py         # December forecasting
│   ├── create_test_dataset_updated.py   # Test data generator
│   ├── final_dataset.csv                # Training data
│   ├── test_dataset_dec_2025.csv        # December test data
│   ├── output_files/                    # Generated outputs
│   │   ├── model_predictions_hybrid_final_<timestamp>.png
│   │   ├── december_2025_predictions_<timestamp>.csv
│   │   └── december_2025_predictions_chart_<timestamp>.png
│   ├── __docs__/                        # Comprehensive documentation
│   └── venv/                            # Project virtual env
│
└── telecom-sales-predictor-mcp-server/  # This MCP server
    ├── mcp_server.py                    # Main server (2 tools)
    ├── requirements.txt                 # Dependencies
    ├── instructions.md                  # Setup guide
    ├── ADD_MCP_SERVER.md               # Integration guide
    ├── mcp_config.json                 # Example config
    ├── README.md                       # This file
    └── venv/                           # MCP server virtual env
```

## Tools Available

### Tool 1: `analyze_hybrid_model`

Trains and evaluates the hybrid machine learning model.

**Parameters:**
- `include_stats` (boolean, optional): Include detailed statistics. Default: `true`

**Returns:**
- TextContent: Model performance metrics for both Random Forest and Linear Regression
- ImageContent: PNG visualization (402 KB) with actual vs predicted values on test set

**What It Does:**
1. Trains Random Forest for VAS_Sold (86.4% R² accuracy)
2. Trains Linear Regression for Speed_Upgrades (80.2% R² accuracy)
3. Evaluates on test set (Aug-Oct 2025)
4. Generates visualization with 95% confidence intervals
5. Returns performance metrics and chart

**Example Usage:**
```python
# LLM calls this tool
analyze_hybrid_model(include_stats=True)

# Returns:
# - Text: "VAS_Sold (Random Forest): R² = 0.864, RMSE = 28.01"
# - Text: "Speed_Upgrades (Linear Regression): R² = 0.802, RMSE = 46.28"
# - PNG: Actual vs predicted comparison chart
```

### Tool 2: `predict_december_2025`

Generates sales forecasts for December 2025 based on marketing campaigns.

**Parameters:**
- `include_stats` (boolean, optional): Include detailed statistics. Default: `true`
- `return_csv` (boolean, optional): Return full CSV content. Default: `false`

**Returns:**
- TextContent: Prediction summary with totals, averages, and top 5 days
- TextContent: Optional CSV data if requested
- ImageContent: PNG cumulative chart (208 KB) showing day-over-day growth

**What It Does:**
1. Trains models on historical data (Sep 2024 - Oct 2025)
2. Loads December 2025 test data with planned marketing campaigns
3. Generates daily predictions for each channel (App/Web)
4. Creates cumulative visualization with campaign markers
5. Identifies top performing days
6. Saves detailed CSV and chart

**Example Usage:**
```python
# LLM calls this tool
predict_december_2025(include_stats=True, return_csv=False)

# Returns:
# - Text: "Total VAS_Sold: 12,450, Daily Average: 401.6"
# - Text: "Top 5 Days by VAS_Sold: Dec 10 (620), Dec 15 (580)..."
# - PNG: Cumulative line chart with campaign day markers
```

## How It Works

### Hybrid Model Analysis Flow

1. **LLM receives** user query about model evaluation
2. **LLM calls** `analyze_hybrid_model` tool
3. **MCP server** spawns subprocess running `analyze_data_hybrid.py`
4. **Script executes:**
   - Loads `final_dataset.csv` (14 months of data)
   - Engineers features (temporal, holidays, marketing)
   - Trains Random Forest for VAS_Sold
   - Trains Linear Regression for Speed_Upgrades
   - Evaluates on test set (Aug-Oct 2025)
   - Generates PNG with timestamp in `output_files/`
5. **Server finds** most recent PNG using glob pattern
6. **Server returns:**
   - Performance metrics (R², RMSE, MAE)
   - PNG chart encoded as base64
7. **LLM displays** results and explains model performance

### December Prediction Flow

1. **LLM receives** user query about December forecasts
2. **LLM calls** `predict_december_2025` tool
3. **MCP server** spawns subprocess running `predict_december_2025.py`
4. **Script executes:**
   - Trains models on historical data
   - Loads `test_dataset_dec_2025.csv` (marketing campaigns)
   - Generates daily predictions for each channel
   - Calculates cumulative totals
   - Saves CSV and PNG with timestamps
5. **Server finds** most recent CSV and PNG files
6. **Server returns:**
   - Prediction summary statistics
   - CSV data (if requested)
   - Cumulative visualization chart
7. **LLM displays** forecasts and explains marketing impact

## Key Features

### ✅ Two Specialized Tools
- **Analysis Tool**: Train and evaluate models
- **Prediction Tool**: Generate future forecasts
- Choose the right tool for the task

### ✅ Hybrid Machine Learning
- Random Forest for non-linear patterns (VAS_Sold)
- Linear Regression for linear relationships (Speed_Upgrades)
- Best-of-breed approach: 83.3% average accuracy

### ✅ Optimized for MCP
- Images are 200-400 KB (well under 1 MB limit)
- Fast transmission over MCP protocol
- Cloud Desktop compatible
- 100 DPI resolution (perfect for screens)

### ✅ Timestamped Outputs
- Each run creates unique files
- Track different scenarios
- No file conflicts
- Easy version comparison

### ✅ Marketing Campaign Analysis
- Correlates sales with email campaigns
- Tracks push notification impact
- Identifies top performing days
- Cumulative visualization shows growth

### ✅ Local Execution
- All processing on your machine
- No data sent externally
- Complete privacy
- No API costs

### ✅ Visual Results
- PNG charts encoded as base64
- Displayed inline in conversations
- Actual vs predicted comparisons
- 95% confidence intervals
- Campaign day markers

## Example Conversations

### Scenario 1: Model Evaluation

**User:** "Analyze the telecom sales data with the hybrid model"

**Claude/Cursor:**
- 🔧 Calls `analyze_hybrid_model` tool
- ⏳ Server runs analysis (20-30 seconds)
- 📊 Receives PNG chart and metrics
- 💬 Responds: "I've analyzed the telecom sales data using the hybrid model:

  **VAS_Sold (Random Forest):**
  - Test Accuracy: 86.4% (R² = 0.864)
  - RMSE: 28.01, MAE: 19.58
  
  **Speed_Upgrades (Linear Regression):**
  - Test Accuracy: 80.2% (R² = 0.802)
  - RMSE: 46.28, MAE: 30.82
  
  **Overall Average: 83.3% accuracy**
  
  The visualization shows actual vs predicted values on the test set (Aug-Oct 2025) with 95% confidence intervals..."
- 🖼️ Displays PNG chart inline

### Scenario 2: December Forecasting

**User:** "What are the December 2025 sales predictions?"

**Claude/Cursor:**
- 🔧 Calls `predict_december_2025` tool
- ⏳ Server runs prediction (20-30 seconds)
- 📈 Receives chart and summary
- 💬 Responds: "Here are the December 2025 sales forecasts:

  **VAS_Sold:**
  - Total for December: 12,450
  - Daily Average: 401.6
  - Peak Day: Dec 10 (620 sales with 175K push notifications)
  
  **Speed_Upgrades:**
  - Total for December: 8,920
  - Daily Average: 287.7
  - Peak Day: Dec 18 (380 upgrades with 250K emails)
  
  The cumulative chart shows strong growth aligned with marketing campaigns (marked with gold stars)..."
- 🖼️ Displays cumulative forecast chart

## Dependencies

### Core MCP Dependencies
```
mcp>=1.1.2              # MCP Python SDK
python-dotenv>=1.0.0    # Environment variables
```

### Analysis Dependencies
```
pandas>=2.0.0           # Data manipulation
numpy>=1.24.0           # Numerical operations
scikit-learn>=1.3.0     # Machine learning models
matplotlib>=3.7.0       # Visualization
openpyxl>=3.1.0         # Excel file reading (for test data generation)
```

Note: Analysis dependencies should already be installed in `../telecom-sales-predictor/venv`. This server's venv only needs MCP SDK packages.

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "MCP SDK requires Python 3.10+" | Upgrade Python or use pyenv/conda |
| "analyze_data_hybrid.py not found" | Check directory structure, script was renamed from `analyze_data.py` |
| "test_dataset_dec_2025.csv not found" | Run `create_test_dataset_updated.py` first |
| "PNG not generated" | Test scripts directly in telecom-sales-predictor directory |
| Server doesn't show two tools | Check config syntax, restart LLM client |
| Process timeout | Normal for first run, models take 20-30 seconds to train |
| Images too large | Already optimized to 100 DPI (200-400 KB) |

### Debug Steps

```bash
# 1. Test Python version
python3 --version  # Should be 3.10+

# 2. Test server manually
cd telecom-sales-predictor-mcp-server
source venv/bin/activate
python mcp_server.py
# Should not crash, press Ctrl+C to stop

# 3. Test hybrid analysis script
cd ../telecom-sales-predictor
source venv/bin/activate  # Or use ./venv/bin/python directly
python analyze_data_hybrid.py
# Should print metrics and generate PNG in output_files/

# 4. Test December prediction script
python predict_december_2025.py
# Should print summary and generate CSV + PNG in output_files/

# 5. Verify output files
ls -lh output_files/
# Should see timestamped PNG and CSV files

# 6. Verify paths in config
cat ../telecom-sales-predictor-mcp-server/mcp_config.json
# Update paths to match your system
```

## Performance

- **Startup:** Instant (server is lightweight)
- **Hybrid Analysis:** 20-30 seconds (Random Forest + Linear Regression training)
- **December Prediction:** 20-30 seconds (training + forecasting)
- **Memory:** ~300-500 MB during execution
- **Timeout:** 90 seconds (increased from 60 for hybrid models)
- **Image Sizes:** 200-400 KB (optimized for MCP)

## Migration Guide (For Existing Users)

If you were using the old single-tool version:

### What Changed
1. ~~`analyze_data.py`~~ → `analyze_data_hybrid.py` (renamed)
2. ~~Single tool~~ → Two tools (`analyze_hybrid_model` + `predict_december_2025`)
3. ~~Fixed filename~~ → Timestamped filenames in `output_files/`
4. ~~300 DPI images (1-2 MB)~~ → 100 DPI images (200-400 KB)

### What Stays the Same
- MCP server endpoint (no config changes needed!)
- Same `mcp_config.json` format
- Same setup process
- Same LLM clients (Cursor/Claude)

### Action Required
- **None!** The MCP server automatically handles the changes
- Just restart your LLM client to pick up the new tools
- Old queries like "generate predictions" will still work

## Limitations

- Requires Python 3.10+ for MCP SDK
- Depends on external scripts (not self-contained)
- Regenerates models on each call (no caching by design for fresh forecasts)
- December predictions require `test_dataset_dec_2025.csv` to exist

## Future Enhancements

Possible improvements:
- [ ] Add model caching for faster repeated analysis
- [ ] Support custom date ranges for predictions
- [ ] Multiple visualization formats (SVG, interactive HTML)
- [ ] Additional tools (what-if analysis, trend forecasting)
- [ ] Streaming responses for large datasets
- [ ] Model comparison tool (compare different months)

## Security

- ✅ Runs with your user permissions
- ✅ No network access required
- ✅ Only accesses specified directories
- ✅ No arbitrary code execution
- ✅ Data stays local
- ✅ MCP protocol ensures secure communication

## Contributing

To modify or extend this server:

1. **Edit `mcp_server.py`** for server logic
2. **Update tool descriptions** in `list_tools()` function
3. **Add new tools** by creating new async functions
4. **Update `requirements.txt`** if adding dependencies
5. **Test manually** before configuring in LLM client
6. **Restart LLM client** to reload changes

## Resources

- **MCP Documentation**: https://modelcontextprotocol.io/
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **MCP Servers Examples**: https://github.com/modelcontextprotocol/servers
- **Project Documentation**: `../telecom-sales-predictor/__docs__/`
- **Cursor Docs**: https://docs.cursor.com/
- **Claude API**: https://docs.anthropic.com/

## License

This is part of the predict-o-matic project. Use freely for learning and development.

## Support

For issues:
1. Check `instructions.md` for setup problems
2. Review `ADD_MCP_SERVER.md` for configuration help
3. Test the analysis scripts independently
4. Check `../telecom-sales-predictor/__docs__/` for script documentation
5. Verify paths and permissions
6. Check LLM client logs

## Success Indicators

You'll know it's working when:

✅ Server runs without Python version errors  
✅ Dependencies install cleanly  
✅ Both analysis scripts generate outputs successfully  
✅ **Two tools** appear in LLM tool list  
✅ LLM can call either tool without errors  
✅ PNGs display correctly in conversation  
✅ Statistics are accurate and complete  
✅ File sizes are 200-400 KB (not 1-2 MB)  
✅ Timestamped files appear in `output_files/`

## Getting Started

**First time?** Read these in order:

1. 📖 **[instructions.md](instructions.md)** - Complete setup walkthrough
2. 🔧 **[ADD_MCP_SERVER.md](ADD_MCP_SERVER.md)** - Add to Cursor/Claude
3. 📚 **[../telecom-sales-predictor/__docs__/](../telecom-sales-predictor/__docs__/)** - Understanding the models
4. 🧪 Test with both tools
5. 🚀 Start using for real analysis and forecasting!

---

Built with ❤️ using the Model Context Protocol

**Happy predicting!** 📊🔮🚀
