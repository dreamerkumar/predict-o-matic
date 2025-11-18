#!/usr/bin/env python3
"""
MCP Server that exposes telecom sales prediction analysis as a tool.
Runs the analyze_data.py script and returns the generated PNG visualization.
"""

import sys

# Check Python version before importing MCP SDK
if sys.version_info < (3, 10):
    print(f"Error: MCP SDK requires Python 3.10 or higher", file=sys.stderr)
    print(f"Current Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}", file=sys.stderr)
    print(f"\nPlease upgrade Python or use a newer version.", file=sys.stderr)
    sys.exit(1)

import asyncio
import subprocess
import base64
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
# Path to the analyze_data.py script (one level up, then into telecom-sales-predictor)
ANALYZE_SCRIPT = SCRIPT_DIR.parent / "telecom-sales-predictor" / "analyze_data.py"
# Path where the PNG will be generated
PNG_OUTPUT = SCRIPT_DIR.parent / "telecom-sales-predictor" / "model_predictions_test_set.png"
# CSV data file location
CSV_FILE = SCRIPT_DIR.parent / "telecom-sales-predictor" / "final_dataset.csv"

# Create an MCP server
app = Server("telecom-predictor-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available tools.
    This function is called by MCP clients to discover what tools are available.
    """
    return [
        Tool(
            name="generate_sales_predictions",
            description=(
                "Analyzes telecom sales data using linear regression and generates predictions. "
                "Returns a PNG visualization showing actual vs predicted values for VAS sales "
                "and speed upgrades on the test set (Aug-Oct 2025). The analysis includes:\n"
                "- Linear regression models for VAS_Sold and Speed_Upgrades\n"
                "- R² scores, RMSE, and MAE metrics for model evaluation\n"
                "- Visual comparison of actual vs predicted values with 95% confidence intervals\n"
                "- Feature importance analysis showing impact of emails, push notifications, and temporal factors"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "include_stats": {
                        "type": "boolean",
                        "description": "Whether to include detailed model performance statistics in the response",
                        "default": True
                    }
                },
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent | ImageContent]:
    """
    Handle tool execution requests.
    
    Args:
        name: The name of the tool to execute
        arguments: Dictionary of arguments for the tool
        
    Returns:
        List containing TextContent with stats and ImageContent with the PNG chart
    """
    if name != "generate_sales_predictions":
        raise ValueError(f"Unknown tool: {name}")
    
    # Validate that required files exist
    if not ANALYZE_SCRIPT.exists():
        return [
            TextContent(
                type="text",
                text=f"Error: Analysis script not found at {ANALYZE_SCRIPT}\n"
                     f"Please ensure telecom-sales-predictor/analyze_data.py exists."
            )
        ]
    
    if not CSV_FILE.exists():
        return [
            TextContent(
                type="text",
                text=f"Error: Data file not found at {CSV_FILE}\n"
                     f"Please ensure telecom-sales-predictor/final_dataset.csv exists."
            )
        ]
    
    include_stats = arguments.get("include_stats", True) if arguments else True
    
    try:
        # Run the analysis script
        # Use the telecom-sales-predictor directory as the working directory
        # so that the script can find final_dataset.csv
        result = subprocess.run(
            [sys.executable, str(ANALYZE_SCRIPT)],
            capture_output=True,
            text=True,
            timeout=60,  # Longer timeout for data processing
            check=False,
            cwd=str(ANALYZE_SCRIPT.parent)  # Run in telecom-sales-predictor directory
        )
        
        # Check if the process succeeded
        if result.returncode != 0:
            error_message = result.stderr.strip() if result.stderr else "Unknown error"
            return [
                TextContent(
                    type="text",
                    text=f"Error running analysis:\n{error_message}\n\nOutput:\n{result.stdout}"
                )
            ]
        
        # Prepare response list
        response_content = []
        
        # Add text output if requested
        if include_stats:
            # Extract key metrics from the output
            stdout = result.stdout
            
            # Parse out the key sections for a cleaner response
            lines = stdout.split('\n')
            key_sections = []
            capture = False
            current_section = []
            
            for line in lines:
                if 'MODEL PERFORMANCE' in line.upper() or 'BUILDING MODEL FOR' in line:
                    capture = True
                    if current_section:
                        key_sections.append('\n'.join(current_section))
                        current_section = []
                
                if capture:
                    current_section.append(line)
                
                if 'VISUALIZATION COMPLETE' in line:
                    capture = False
                    if current_section:
                        key_sections.append('\n'.join(current_section))
                        current_section = []
            
            # Create a formatted summary
            summary = "✅ **Telecom Sales Prediction Analysis Complete**\n\n"
            summary += "The linear regression models have been trained and evaluated.\n\n"
            summary += "**Key Results:**\n"
            summary += '\n'.join(key_sections) if key_sections else stdout
            
            response_content.append(
                TextContent(
                    type="text",
                    text=summary
                )
            )
        else:
            response_content.append(
                TextContent(
                    type="text",
                    text="✅ Analysis completed successfully! Visualization generated."
                )
            )
        
        # Read the generated PNG file
        if not PNG_OUTPUT.exists():
            return [
                TextContent(
                    type="text",
                    text=f"Error: PNG file was not generated at expected location: {PNG_OUTPUT}"
                )
            ]
        
        # Read PNG as binary and encode to base64
        with open(PNG_OUTPUT, 'rb') as img_file:
            image_data = img_file.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # Add the image to response
        response_content.append(
            ImageContent(
                type="image",
                data=base64_image,
                mimeType="image/png"
            )
        )
        
        return response_content
            
    except subprocess.TimeoutExpired:
        return [
            TextContent(
                type="text",
                text="Error: Analysis process timed out (exceeded 60 seconds)\n"
                     "This may indicate a problem with the data or computation."
            )
        ]
    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"Error: Unexpected error occurred: {str(e)}\n"
                     f"Script location: {ANALYZE_SCRIPT}\n"
                     f"CSV location: {CSV_FILE}\n"
                     f"PNG output: {PNG_OUTPUT}"
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

