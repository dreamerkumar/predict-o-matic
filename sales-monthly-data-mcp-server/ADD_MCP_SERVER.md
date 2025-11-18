## Setup for Cursor IDE

Here's the quick setup for Cursor:

1. Open Cursor Settings → Search for "MCP" or go to Extensions → MCP
2. Add this configuration:

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

3. Restart Cursor
4. Test it - Ask Cursor: "Use the sales_data tool to get sales for January 2023"

## Setup for Claude Desktop App

Here's how to add this MCP server to the Claude desktop app:

Open the configuration file:
```
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Or navigate to it manually and open with your preferred text editor.

Add the server configuration. The file should have a structure like this:

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

If you already have other MCP servers configured, add the sales_data server to the existing mcpServers object:

```
{
  "mcpServers": {
    "existing_server": {
      // ... existing configuration
    },
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

Save the file and restart Claude Desktop for the changes to take effect.

The MCP server should now be available in Claude Desktop. You can verify it's working by checking if Claude can access the tools and resources provided by your sales_data MCP server.
Make sure that:

The Python virtual environment at the specified path exists and has all necessary dependencies installed
The mcp_server.py file is executable and properly configured
The working directory path is correct