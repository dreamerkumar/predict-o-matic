# Sales Monthly Data MCP Server

This project implements an MCP server that provides sales data for specific months and years through a simple command-line interface, API, and MCP tool integration.

## Project Structure

- `sales_data.csv`: CSV file containing sales data by month and year
- `sales_data.py`: Command-line script to retrieve sales data
- `test_sales_data.py`: Test suite for the sales data script
- `api_server.py`: FastAPI server to expose sales data as a REST API
- `mcp_server.py`: MCP server to expose sales data as an MCP tool

## Getting Started

### Prerequisites

- Python 3.10 or higher (required for MCP SDK)
- Git (for installing the MCP SDK)

### Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate     # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install 'git+https://github.com/modelcontextprotocol/python-sdk.git'
   ```

## Usage

**Note:** All commands below should be run with the virtual environment activated.

### Command Line

```bash
# Make sure your virtual environment is activated
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows

# Get sales data for a specific month and year
python sales_data.py January 2023

# Test the sales data script
python test_sales_data.py
```

### API Server

Start the API server:

```bash
# Make sure your virtual environment is activated first
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows

# Then run the API server
python api_server.py
```

Then access the API at:
- Docs: http://localhost:8000/docs
- API endpoint: http://localhost:8000/sales?month=January&year=2023

### MCP Server

To use the MCP server with Cursor:

1. See the `ADD_MCP_SERVER.md` file for Cursor configuration
2. After configuring, restart Cursor
3. Ask Cursor: "Use the sales_data tool to get sales for January 2023"

## CSV Data Format

The sales data is stored in `sales_data.csv` with the following format:

```
month,year,sales
January,2023,125467.89
February,2023,98345.67
...
```

## Development

To add new functionality:

1. Add new sales data to the CSV file
2. Update the tests to cover new functionality
3. Implement new features in the scripts

## Documentation

Additional documentation:
- `VIRTUAL_ENV_GUIDE.md`: Guide to Python virtual environments
- `ADD_MCP_SERVER.md`: Instructions for adding the MCP server to Cursor
- `RUN_SERVER.md`: Tips for running the API server properly
- `SETUP_COMPLETE.md`: Verification that setup is complete

## License

This project is licensed under the MIT License.
