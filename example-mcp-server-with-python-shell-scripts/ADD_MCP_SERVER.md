Here's the quick setup for Cursor:

Add to Cursor MCP Settings

Open Cursor Settings → Search for "MCP" or go to Extensions → MCP

Add this configuration:

```
{
  "mcpServers": {
    "calculator": {
      "command": "/Users/vishalkumar/code/frontier/predict-o-matic/example-mcp-server-with-python-shell-scripts/venv/bin/python",
      "args": [
        "/Users/vishalkumar/code/frontier/predict-o-matic/example-mcp-server-with-python-shell-scripts/mcp_server.py"
      ],
      "cwd": "/Users/vishalkumar/code/frontier/predict-o-matic/example-mcp-server-with-python-shell-scripts"
    }
  }
}
```

Restart Cursor

Test it - Ask Cursor: "Use the calculator to add 15 and 27"
