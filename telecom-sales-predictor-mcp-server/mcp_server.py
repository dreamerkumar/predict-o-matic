#!/usr/bin/env python3
"""
MCP Server that exposes telecom sales prediction analysis as two tools:
1. analyze_hybrid_model: Trains and evaluates hybrid ML model (Random Forest + Linear Regression)
2. predict_december_2025: Generates December 2025 sales forecasts
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
import glob
import os

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
# Path to the main project directory
PROJECT_DIR = SCRIPT_DIR.parent / "telecom-sales-predictor"
# Paths to the analysis scripts
HYBRID_ANALYZE_SCRIPT = PROJECT_DIR / "analyze_data_hybrid.py"
DECEMBER_PREDICT_SCRIPT = PROJECT_DIR / "predict_december_2025.py"
# CSV data file location
CSV_FILE = PROJECT_DIR / "final_dataset.csv"
TEST_DATASET = PROJECT_DIR / "test_dataset_dec_2025.csv"
# Output directory where PNG files are generated
OUTPUT_DIR = PROJECT_DIR / "output_files"

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
            name="analyze_hybrid_model",
            description=(
                "Analyzes telecom sales data using a hybrid machine learning model and generates predictions. "
                "Uses Random Forest for VAS_Sold (86.4% accuracy) and Linear Regression for Speed_Upgrades (80.2% accuracy). "
                "Returns a PNG visualization showing actual vs predicted values on the test set (Aug-Oct 2025). "
                "The analysis includes:\n"
                "- Hybrid model training (Random Forest + Linear Regression)\n"
                "- R² scores, RMSE, and MAE metrics for both models\n"
                "- Visual comparison with 95% confidence intervals\n"
                "- Feature importance analysis\n"
                "- Training data: Sep 2024 - Jul 2025, Test data: Aug-Oct 2025"
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
        ),
        Tool(
            name="predict_december_2025",
            description=(
                "Generates sales predictions for December 2025 using the trained hybrid model. "
                "Trains models on historical data (Sep 2024 - Oct 2025) and applies them to December 2025 "
                "with planned marketing campaigns. Returns:\n"
                "- Detailed CSV with daily predictions by channel\n"
                "- Cumulative visualization chart showing day-over-day growth\n"
                "- Campaign day markers (Push notifications for App, Emails for Web)\n"
                "- Summary statistics (total predicted sales, daily averages, top 5 days)\n"
                "- Predictions for VAS_Sold and Speed_Upgrades based on marketing activities"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "include_stats": {
                        "type": "boolean",
                        "description": "Whether to include detailed prediction statistics in the response",
                        "default": True
                    },
                    "return_csv": {
                        "type": "boolean",
                        "description": "Whether to return the detailed predictions CSV content",
                        "default": False
                    }
                },
                "required": []
            }
        )
    ]


def find_latest_output_file(pattern: str) -> Path | None:
    """
    Find the most recently generated output file matching the pattern.
    
    Args:
        pattern: Glob pattern to match files (e.g., "model_predictions_hybrid_final_*.png")
        
    Returns:
        Path to the most recent file, or None if no files found
    """
    files = glob.glob(str(OUTPUT_DIR / pattern))
    if not files:
        return None
    # Sort by modification time, most recent first
    files.sort(key=os.path.getmtime, reverse=True)
    return Path(files[0])


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
    if name == "analyze_hybrid_model":
        return await run_hybrid_analysis(arguments)
    elif name == "predict_december_2025":
        return await run_december_prediction(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def run_hybrid_analysis(arguments: Any) -> list[TextContent | ImageContent]:
    """
    Run the hybrid model analysis (analyze_data_hybrid.py).
    """
    # Validate that required files exist
    if not HYBRID_ANALYZE_SCRIPT.exists():
        return [
            TextContent(
                type="text",
                text=f"Error: Analysis script not found at {HYBRID_ANALYZE_SCRIPT}\n"
                     f"Please ensure telecom-sales-predictor/analyze_data_hybrid.py exists."
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
        result = subprocess.run(
            [sys.executable, str(HYBRID_ANALYZE_SCRIPT)],
            capture_output=True,
            text=True,
            timeout=90,  # Longer timeout for hybrid model training
            check=False,
            cwd=str(HYBRID_ANALYZE_SCRIPT.parent)  # Run in telecom-sales-predictor directory
        )
        
        # Check if the process succeeded
        if result.returncode != 0:
            error_message = result.stderr.strip() if result.stderr else "Unknown error"
            return [
                TextContent(
                    type="text",
                    text=f"Error running hybrid analysis:\n{error_message}\n\nOutput:\n{result.stdout}"
                )
            ]
        
        # Prepare response list
        response_content = []
        
        # Add text output if requested
        if include_stats:
            # Extract key metrics from the output
            stdout = result.stdout
            
            # Parse out key sections for cleaner response
            lines = stdout.split('\n')
            key_sections = []
            capture = False
            current_section = []
            
            for line in lines:
                if any(keyword in line.upper() for keyword in ['HYBRID MODEL', 'BUILDING', 'MODEL TRAINING COMPLETE', 'FINAL MODEL SUMMARY']):
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
            summary = "✅ **Hybrid Model Analysis Complete**\n\n"
            summary += "The hybrid model (Random Forest for VAS_Sold + Linear Regression for Speed_Upgrades) "
            summary += "has been trained and evaluated on test data (Aug-Oct 2025).\n\n"
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
                    text="✅ Hybrid model analysis completed successfully! Visualization generated."
                )
            )
        
        # Find the most recent PNG file for hybrid analysis
        png_file = find_latest_output_file("model_predictions_hybrid_final_*.png")
        
        if not png_file or not png_file.exists():
            response_content.append(
                TextContent(
                    type="text",
                    text=f"\n⚠️ Warning: PNG file was not found in {OUTPUT_DIR}\n"
                         f"Looking for pattern: model_predictions_hybrid_final_*.png"
                )
            )
            return response_content
        
        # Read PNG as binary and encode to base64
        with open(png_file, 'rb') as img_file:
            image_data = img_file.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # Add file info and image to response
        file_size_kb = len(image_data) / 1024
        response_content.append(
            TextContent(
                type="text",
                text=f"\n📊 **Visualization Details:**\n"
                     f"- File: {png_file.name}\n"
                     f"- Size: {file_size_kb:.1f} KB\n"
                     f"- Location: {png_file.relative_to(PROJECT_DIR)}"
            )
        )
        
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
                text="Error: Analysis process timed out (exceeded 90 seconds)\n"
                     "This may indicate a problem with the data or computation."
            )
        ]
    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"Error: Unexpected error occurred: {str(e)}\n"
                     f"Script location: {HYBRID_ANALYZE_SCRIPT}\n"
                     f"CSV location: {CSV_FILE}\n"
                     f"Output directory: {OUTPUT_DIR}"
            )
        ]


async def run_december_prediction(arguments: Any) -> list[TextContent | ImageContent]:
    """
    Run the December 2025 prediction (predict_december_2025.py).
    """
    # Validate that required files exist
    if not DECEMBER_PREDICT_SCRIPT.exists():
        return [
            TextContent(
                type="text",
                text=f"Error: Prediction script not found at {DECEMBER_PREDICT_SCRIPT}\n"
                     f"Please ensure telecom-sales-predictor/predict_december_2025.py exists."
            )
        ]
    
    if not CSV_FILE.exists():
        return [
            TextContent(
                type="text",
                text=f"Error: Training data file not found at {CSV_FILE}\n"
                     f"Please ensure telecom-sales-predictor/final_dataset.csv exists."
            )
        ]
    
    if not TEST_DATASET.exists():
        return [
            TextContent(
                type="text",
                text=f"Error: Test dataset not found at {TEST_DATASET}\n"
                     f"Please run create_test_dataset_updated.py first to generate December 2025 test data."
            )
        ]
    
    include_stats = arguments.get("include_stats", True) if arguments else True
    return_csv = arguments.get("return_csv", False) if arguments else False
    
    try:
        # Run the prediction script
        result = subprocess.run(
            [sys.executable, str(DECEMBER_PREDICT_SCRIPT)],
            capture_output=True,
            text=True,
            timeout=90,  # Timeout for training + prediction
            check=False,
            cwd=str(DECEMBER_PREDICT_SCRIPT.parent)  # Run in telecom-sales-predictor directory
        )
        
        # Check if the process succeeded
        if result.returncode != 0:
            error_message = result.stderr.strip() if result.stderr else "Unknown error"
            return [
                TextContent(
                    type="text",
                    text=f"Error running December prediction:\n{error_message}\n\nOutput:\n{result.stdout}"
                )
            ]
        
        # Prepare response list
        response_content = []
        
        # Add text output if requested
        if include_stats:
            # Extract key metrics from the output
            stdout = result.stdout
            
            # Parse out summary sections
            lines = stdout.split('\n')
            key_sections = []
            capture = False
            current_section = []
            
            for line in lines:
                if any(keyword in line.upper() for keyword in ['DECEMBER 2025', 'PREDICTIONS SUMMARY', 'TOP 5 DAYS']):
                    capture = True
                    if current_section and not all(line.strip() == '' for line in current_section):
                        key_sections.append('\n'.join(current_section))
                        current_section = []
                
                if capture:
                    current_section.append(line)
                
                if 'PREDICTION COMPLETE' in line:
                    capture = False
                    if current_section:
                        key_sections.append('\n'.join(current_section))
                        current_section = []
            
            # Create a formatted summary
            summary = "✅ **December 2025 Predictions Complete**\n\n"
            summary += "Sales forecasts have been generated for December 2025 based on:\n"
            summary += "- Historical data (Sep 2024 - Oct 2025)\n"
            summary += "- Planned marketing campaigns (Push notifications & Emails)\n"
            summary += "- Hybrid model (Random Forest + Linear Regression)\n\n"
            summary += "**Prediction Summary:**\n"
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
                    text="✅ December 2025 predictions completed successfully!"
                )
            )
        
        # Find the most recent CSV and PNG files for December prediction
        csv_file = find_latest_output_file("december_2025_predictions_*.csv")
        png_file = find_latest_output_file("december_2025_predictions_chart_*.png")
        
        # Handle CSV file if requested
        if return_csv and csv_file and csv_file.exists():
            with open(csv_file, 'r') as f:
                csv_content = f.read()
            response_content.append(
                TextContent(
                    type="text",
                    text=f"\n📄 **Detailed Predictions CSV:**\n```csv\n{csv_content}\n```"
                )
            )
        
        # Handle PNG visualization
        if not png_file or not png_file.exists():
            response_content.append(
                TextContent(
                    type="text",
                    text=f"\n⚠️ Warning: Chart PNG was not found in {OUTPUT_DIR}\n"
                         f"Looking for pattern: december_2025_predictions_chart_*.png"
                )
            )
            return response_content
        
        # Read PNG as binary and encode to base64
        with open(png_file, 'rb') as img_file:
            image_data = img_file.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # Add file info
        file_size_kb = len(image_data) / 1024
        file_info = f"\n📊 **Visualization Details:**\n"
        file_info += f"- Chart: {png_file.name}\n"
        file_info += f"- Chart Size: {file_size_kb:.1f} KB\n"
        
        if csv_file and csv_file.exists():
            csv_size_kb = csv_file.stat().st_size / 1024
            file_info += f"- CSV: {csv_file.name}\n"
            file_info += f"- CSV Size: {csv_size_kb:.1f} KB\n"
        
        file_info += f"- Location: {OUTPUT_DIR.relative_to(PROJECT_DIR)}"
        
        response_content.append(
            TextContent(
                type="text",
                text=file_info
            )
        )
        
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
                text="Error: Prediction process timed out (exceeded 90 seconds)\n"
                     "This may indicate a problem with the data or computation."
            )
        ]
    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"Error: Unexpected error occurred: {str(e)}\n"
                     f"Script location: {DECEMBER_PREDICT_SCRIPT}\n"
                     f"Training data: {CSV_FILE}\n"
                     f"Test data: {TEST_DATASET}\n"
                     f"Output directory: {OUTPUT_DIR}"
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
