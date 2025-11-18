#!/usr/bin/env python3
"""
MCP Server that exposes sales_data.py as a tool for LLM clients.
"""

import sys

# Check Python version before importing MCP SDK
if sys.version_info < (3, 10):
    print(f"Error: MCP SDK requires Python 3.10 or higher", file=sys.stderr)
    print(f"Current Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}", file=sys.stderr)
    print(f"\nPlease upgrade Python or use a newer version.", file=sys.stderr)
    print(f"Parts 1 and 2 of this project work with Python 3.8+", file=sys.stderr)
    sys.exit(1)

import asyncio
import subprocess
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
SALES_DATA_PATH = SCRIPT_DIR / "sales_data.py"


# Create an MCP server
app = Server("sales-data-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available tools.
    This function is called by MCP clients to discover what tools are available.
    """
    return [
        Tool(
            name="sales_data",
            description=(
                "Retrieves monthly sales data based on month and year parameters. "
                "Returns sales data in dollars or 'No data exists' if no data is found "
                "for the specified month and year."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "month": {
                        "type": "string",
                        "description": "The month (e.g., January, February)"
                    },
                    "year": {
                        "type": "string",
                        "description": "The year (e.g., 2023, 2024, 2025)"
                    }
                },
                "required": ["month", "year"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    Handle tool execution requests.
    
    Args:
        name: The name of the tool to execute
        arguments: Dictionary of arguments for the tool
        
    Returns:
        List of TextContent with the result
    """
    if name != "sales_data":
        raise ValueError(f"Unknown tool: {name}")
    
    # Validate arguments
    if not isinstance(arguments, dict):
        raise ValueError("Arguments must be a dictionary")
    
    month = arguments.get("month")
    year = arguments.get("year")
    
    if not month:
        raise ValueError("Month parameter is required")
    
    if not year:
        raise ValueError("Year parameter is required")
    
    try:
        # Call the sales_data.py script
        result = subprocess.run(
            [
                sys.executable,
                str(SALES_DATA_PATH),
                month,
                year
            ],
            capture_output=True,
            text=True,
            timeout=5,
            check=False
        )
        
        # Check if the process succeeded
        if result.returncode != 0:
            error_message = result.stderr.strip() if result.stderr else "Unknown error"
            return [
                TextContent(
                    type="text",
                    text=f"Error: {error_message}"
                )
            ]
        
        # Get the result
        sales_data = result.stdout.strip()
        
        # Format the response
        if sales_data == "No data exists":
            return [
                TextContent(
                    type="text",
                    text=f"No sales data exists for {month} {year}."
                )
            ]
        else:
            return [
                TextContent(
                    type="text",
                    text=f"Sales for {month} {year}: ${sales_data}"
                )
            ]
            
    except subprocess.TimeoutExpired:
        return [
            TextContent(
                type="text",
                text="Error: Sales data process timed out"
            )
        ]
    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"Error: Unexpected error occurred: {str(e)}"
            )
        ]


async def main():
    """Main entry point for the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
