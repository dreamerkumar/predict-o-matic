Here's the quick setup for Cursor:

Add to Cursor MCP Settings

Open Cursor Settings → Search for "MCP" or go to Extensions → MCP

Add this configuration:

```
{
  "mcpServers": {
    "sales_data": {
      "command": "/Users/vishalkumar/code/frontier/predict-o-matic/sales-monthly-data-mcp-server/venv/bin/python",
      "args": [
        "/Users/vishalkumar/code/frontier/predict-o-matic/sales-monthly-data-mcp-server/mcp_server.py"
      ],
      "cwd": "/Users/vishalkumar/code/frontier/predict-o-matic/sales-monthly-data-mcp-server"
    }
  }
}
```

Restart Cursor

Test it - Ask Cursor: "Use the sales_data tool to get sales for January 2023"
