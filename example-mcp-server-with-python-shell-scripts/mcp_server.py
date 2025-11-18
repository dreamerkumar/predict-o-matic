#!/usr/bin/env python3
"""
MCP Server that exposes calculator.py as a tool for LLM clients.
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
CALCULATOR_PATH = SCRIPT_DIR / "calculator.py"


# Create an MCP server
app = Server("calculator-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available tools.
    This function is called by MCP clients to discover what tools are available.
    """
    return [
        Tool(
            name="calculator",
            description=(
                "Performs arithmetic operations (addition or multiplication) on two numbers. "
                "This tool wraps a CLI calculator script and demonstrates how to create "
                "MCP servers that call shell commands."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "multiply"],
                        "description": "The operation to perform: 'add' for addition or 'multiply' for multiplication"
                    },
                    "param1": {
                        "type": "number",
                        "description": "The first number"
                    },
                    "param2": {
                        "type": "number",
                        "description": "The second number"
                    }
                },
                "required": ["operation", "param1", "param2"]
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
    if name != "calculator":
        raise ValueError(f"Unknown tool: {name}")
    
    # Validate arguments
    if not isinstance(arguments, dict):
        raise ValueError("Arguments must be a dictionary")
    
    operation = arguments.get("operation")
    param1 = arguments.get("param1")
    param2 = arguments.get("param2")
    
    if operation not in ["add", "multiply"]:
        raise ValueError(f"Invalid operation: {operation}. Must be 'add' or 'multiply'")
    
    if not isinstance(param1, (int, float)):
        raise ValueError(f"param1 must be a number, got {type(param1).__name__}")
    
    if not isinstance(param2, (int, float)):
        raise ValueError(f"param2 must be a number, got {type(param2).__name__}")
    
    try:
        # Call the calculator CLI script
        result = subprocess.run(
            [
                sys.executable,
                str(CALCULATOR_PATH),
                operation,
                str(param1),
                str(param2)
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
        
        # Parse and return the result
        try:
            calculation_result = float(result.stdout.strip())
            return [
                TextContent(
                    type="text",
                    text=f"Result: {calculation_result}\n\nOperation: {operation}({param1}, {param2}) = {calculation_result}"
                )
            ]
        except ValueError:
            return [
                TextContent(
                    type="text",
                    text=f"Error: Invalid output from calculator: {result.stdout}"
                )
            ]
            
    except subprocess.TimeoutExpired:
        return [
            TextContent(
                type="text",
                text="Error: Calculator process timed out"
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

