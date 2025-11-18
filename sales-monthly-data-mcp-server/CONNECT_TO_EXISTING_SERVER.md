# Connecting to an Existing MCP Server

This guide explains how to connect to an MCP server that's already running locally, rather than having the Claude IDE spawn a new server process.

## Part 1: Start the MCP Server Locally

Before configuring Claude or Cursor to connect to your local server, you need to start the server:

1. Open a terminal window
2. Navigate to the server directory:
   ```
   cd /Users/vishalkumar/code/frontier/predict-o-matic/sales-monthly-data-mcp-server
   ```
3. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```
4. Start the MCP server:
   ```
   python mcp_server.py --host localhost --port 8080
   ```
   Note: The default port is 8080, but you can change it if needed

5. You should see output indicating that the server has started successfully:
   ```
   INFO:     Started server process [12345]
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://localhost:8080 (Press CTRL+C to quit)
   ```

Keep this terminal window open while you use the server.

## Part 2: Configure Claude IDE to Connect to the Local Server

### Setup for Cursor IDE

Here's how to connect Cursor to your running local server:

1. Open Cursor Settings → Search for "MCP" or go to Extensions → MCP
2. Add this configuration:

```
{
  "mcpServers": {
    "sales_data": {
      "url": "http://localhost:8080"
    }
  }
}
```

3. Restart Cursor
4. Test it - Ask Cursor: "Use the sales_data tool to get sales for January 2023"

### Setup for Claude Desktop App

Here's how to connect the Claude desktop app to your running local server:

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
      "url": "http://localhost:8080"
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
      "url": "http://localhost:8080"
    }
  }
}
```

Save the file and restart Claude Desktop for the changes to take effect.

## Troubleshooting

If you encounter issues:

1. **Make sure your server is running**: Check the terminal window where you started the server. It should show no errors.

2. **Verify the port**: If you changed the default port, ensure your configuration matches the port you specified.

3. **Check for network issues**: Make sure no firewall or other security software is blocking connections to your localhost port.

4. **Test the server directly**: You can use curl or your browser to verify the server is responding:
   ```
   curl http://localhost:8080/schema
   ```
   This should return the JSON schema for the server's API.

5. **Examine logs**: Look for error messages in both the terminal where the server is running and in the Cursor or Claude Desktop logs.

Remember to keep the terminal window with the running server open throughout your session. If you close it, the server will stop and the connection will be lost.
