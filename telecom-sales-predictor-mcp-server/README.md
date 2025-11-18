# Telecom Sales Predictor MCP Server

An MCP (Model Context Protocol) server that exposes telecom sales predictive analytics as a tool for LLM clients like Claude and Cursor.

## What This Does

This MCP server allows LLMs to:
- 📊 Generate sales predictions using linear regression models
- 🎯 Analyze VAS (Value-Added Services) sales and Speed Upgrades
- 📈 Create visualizations with actual vs predicted values
- 📉 Return PNG charts directly to the conversation
- 📋 Provide detailed model performance metrics (R², RMSE, MAE)

## Architecture

```
LLM Client (Claude/Cursor)
    ↓ MCP Protocol
MCP Server (this project)
    ↓ Subprocess
Analysis Script (../telecom-sales-predictor/analyze_data.py)
    ↓ Process Data
Linear Regression Models
    ↓ Generate
PNG Visualization
    ↓ Base64 Encode
LLM Client (displays chart)
```

## Quick Start

### 1. Setup

```bash
# Navigate to this directory
cd telecom-sales-predictor-mcp-server

# Create virtual environment (requires Python 3.10+)
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Test

```bash
# Verify the server can run
python mcp_server.py
# Press Ctrl+C to stop

# Verify data files exist
ls -la ../telecom-sales-predictor/analyze_data.py
ls -la ../telecom-sales-predictor/final_dataset.csv
```

### 3. Configure

Add to Cursor or Claude Desktop:

**For Cursor:** Edit `~/.cursor/mcp.json`  
**For Claude Desktop:** Edit `~/Library/Application Support/Claude/claude_desktop_config.json`

Use the configuration from `mcp_config.json` (update paths for your system).

### 4. Use

Restart your LLM client, then ask:

```
"Generate sales predictions for the telecom data"
"Show me the model performance visualization"
"Run the predictive analysis"
```

## Documentation

| File | Description |
|------|-------------|
| **[instructions.md](instructions.md)** | Complete setup and usage guide |
| **[ADD_MCP_SERVER.md](ADD_MCP_SERVER.md)** | How to integrate with Cursor/Claude |
| **[mcp_config.json](mcp_config.json)** | Example configuration file |

## Requirements

- **Python 3.10+** (MCP SDK requirement)
- **Virtual Environment** (recommended)
- **Adjacent telecom-sales-predictor directory** with:
  - `analyze_data.py` - The analysis script
  - `final_dataset.csv` - The data file

## Project Structure

```
predict-o-matic/
├── telecom-sales-predictor/          # Original analysis project
│   ├── analyze_data.py               # Script that does the work
│   ├── final_dataset.csv             # Data source
│   └── venv/                         # Its own virtual env
│
└── telecom-sales-predictor-mcp-server/  # This MCP server
    ├── mcp_server.py                 # Main server implementation
    ├── requirements.txt              # Dependencies
    ├── instructions.md               # Setup guide
    ├── ADD_MCP_SERVER.md            # Integration guide
    ├── mcp_config.json              # Example config
    ├── README.md                    # This file
    └── venv/                        # MCP server virtual env
```

## Tool Available

### `generate_sales_predictions`

Runs predictive analysis and returns visualization.

**Parameters:**
- `include_stats` (boolean, optional): Include detailed statistics. Default: `true`

**Returns:**
- TextContent: Model performance metrics, R² scores, feature coefficients
- ImageContent: PNG visualization with actual vs predicted values

**Example Usage:**

```python
# LLM calls this tool
generate_sales_predictions(include_stats=True)

# Returns:
# - Text with R² scores, RMSE, MAE
# - PNG chart showing predictions vs actuals
```

## How It Works

1. **LLM receives user query** about sales predictions
2. **LLM calls the MCP tool** `generate_sales_predictions`
3. **MCP server receives request** via stdio
4. **Server runs subprocess** calling `analyze_data.py`
5. **Analysis script:**
   - Loads CSV data
   - Trains linear regression models
   - Generates PNG visualization
   - Saves to disk
6. **Server reads PNG** and encodes to base64
7. **Server returns response:**
   - TextContent with metrics
   - ImageContent with PNG
8. **LLM displays** the chart and explains results

## Key Features

### ✅ Local Execution
- All processing happens on your machine
- No data sent to external services
- Complete privacy

### ✅ Visual Results
- PNG charts encoded as base64
- Displayed inline in LLM conversations
- Actual vs predicted comparisons
- 95% confidence intervals

### ✅ Statistical Analysis
- R² scores for model accuracy
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- Feature coefficients

### ✅ Easy Integration
- Standard MCP protocol
- Works with Cursor and Claude
- Simple configuration
- No additional authentication needed

## Example Conversation

**User:** "Generate the telecom sales predictions"

**Claude/Cursor:**
- 🔧 Calls `generate_sales_predictions` tool
- ⏳ Server runs analysis (10-15 seconds)
- 📊 Receives PNG chart and metrics
- 💬 Responds: "I've generated the sales predictions. The models achieved strong performance:
  - VAS_Sold: R² = 0.87, RMSE = 12.34
  - Speed_Upgrades: R² = 0.79, RMSE = 8.56
  
  The visualization below shows actual values (blue) vs predictions (purple) on the test set..."
- 🖼️ Displays PNG chart inline

**User:** "What does this tell us about the predictions?"

**Claude/Cursor:** "The high R² scores indicate the models are capturing most of the variance in the data. The confidence intervals show we can be reasonably certain about predictions within the shaded bands..."

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
```

Note: Analysis dependencies should already be installed in the `../telecom-sales-predictor/venv`. This server's venv only needs them if running in a completely separate environment.

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "MCP SDK requires Python 3.10+" | Upgrade Python or use pyenv/conda |
| "Analysis script not found" | Check directory structure, ensure paths are correct |
| "Data file not found" | Ensure `final_dataset.csv` exists |
| "PNG not generated" | Test `analyze_data.py` directly first |
| Server doesn't appear in tool list | Check config syntax, restart LLM client |
| Process timeout | Increase timeout in `mcp_server.py` |

### Debug Steps

```bash
# 1. Test Python version
python3 --version  # Should be 3.10+

# 2. Test server manually
cd telecom-sales-predictor-mcp-server
source venv/bin/activate
python mcp_server.py
# Should not crash immediately

# 3. Test analysis script
cd ../telecom-sales-predictor
source venv/bin/activate
python analyze_data.py
# Should generate PNG

# 4. Verify paths in config
cat mcp_config.json
# Update paths to match your system
```

## Performance

- **Startup:** Instant (server is lightweight)
- **Analysis:** 10-15 seconds (model training + visualization)
- **Memory:** ~200MB during execution
- **Timeout:** 60 seconds (configurable)

## Limitations

- Requires Python 3.10+ for MCP SDK
- Depends on external script (not self-contained)
- Regenerates models on each call (no caching)
- Single tool per server instance

## Future Enhancements

Possible improvements:
- [ ] Add model caching for faster responses
- [ ] Support custom date ranges for analysis
- [ ] Multiple visualization formats (SVG, PDF)
- [ ] Additional tools (trend analysis, forecasting)
- [ ] Error recovery and retry logic
- [ ] Streaming responses for large datasets

## Security

- ✅ Runs with your user permissions
- ✅ No network access required
- ✅ Only accesses specified directories
- ✅ No arbitrary code execution
- ✅ Data stays local

## Contributing

To modify or extend this server:

1. **Edit `mcp_server.py`** for server logic
2. **Update `requirements.txt`** if adding dependencies
3. **Test manually** before configuring in LLM client
4. **Restart LLM client** to reload changes

## Resources

- **MCP Documentation**: https://modelcontextprotocol.io/
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **MCP Servers Examples**: https://github.com/modelcontextprotocol/servers
- **Cursor Docs**: https://docs.cursor.com/
- **Claude API**: https://docs.anthropic.com/

## License

This is part of the predict-o-matic project. Use freely for learning and development.

## Support

For issues:
1. Check `instructions.md` for setup problems
2. Review `ADD_MCP_SERVER.md` for configuration help
3. Test the analysis script independently
4. Verify paths and permissions
5. Check LLM client logs

## Success Indicators

You'll know it's working when:

✅ Server runs without Python version errors  
✅ Dependencies install cleanly  
✅ Analysis script generates PNG successfully  
✅ Server appears in LLM tool list  
✅ LLM can call the tool without errors  
✅ PNG displays correctly in conversation  
✅ Statistics are accurate and complete

## Getting Started

**First time?** Read these in order:

1. 📖 **[instructions.md](instructions.md)** - Complete setup walkthrough
2. 🔧 **[ADD_MCP_SERVER.md](ADD_MCP_SERVER.md)** - Add to Cursor/Claude
3. 🧪 Test with a simple query
4. 🚀 Start using for real analysis!

---

Built with ❤️ using the Model Context Protocol

**Happy predicting!** 📊🚀

