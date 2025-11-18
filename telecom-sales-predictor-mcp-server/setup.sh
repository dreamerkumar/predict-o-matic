#!/bin/bash
# Setup script for Telecom Sales Predictor MCP Server
# This automates the virtual environment creation and dependency installation

set -e  # Exit on error

echo "======================================================================"
echo "TELECOM SALES PREDICTOR MCP SERVER - SETUP SCRIPT"
echo "======================================================================"
echo ""

# Check Python version
echo "Step 1: Checking Python version..."
echo "----------------------------------------------------------------------"
PYTHON_CMD=""

# Try python3 first
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    echo "Found: Python $PYTHON_VERSION"
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
        PYTHON_CMD="python3"
        echo "✅ Python 3.10+ detected"
    else
        echo "❌ Python version is too old (need 3.10+)"
        echo ""
        echo "Please upgrade Python or use pyenv/conda:"
        echo "  brew install python@3.11  # On macOS"
        echo "  pyenv install 3.11.0      # Using pyenv"
        exit 1
    fi
else
    echo "❌ python3 not found"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

echo ""

# Check if venv already exists
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing old virtual environment..."
        rm -rf venv
    else
        echo "Using existing virtual environment"
        echo "To install dependencies, run: source venv/bin/activate && pip install -r requirements.txt"
        exit 0
    fi
fi

# Create virtual environment
echo "Step 2: Creating virtual environment..."
echo "----------------------------------------------------------------------"
$PYTHON_CMD -m venv venv
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "Step 3: Activating virtual environment..."
echo "----------------------------------------------------------------------"
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "Step 4: Upgrading pip..."
echo "----------------------------------------------------------------------"
pip install --upgrade pip --quiet
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "Step 5: Installing dependencies..."
echo "----------------------------------------------------------------------"
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Run verification tests
echo "Step 6: Running verification tests..."
echo "----------------------------------------------------------------------"
python test_server.py

echo ""
echo "======================================================================"
echo "SETUP COMPLETE!"
echo "======================================================================"
echo ""
echo "Virtual environment is ready. To use it:"
echo ""
echo "  1. Activate: source venv/bin/activate"
echo "  2. Test:     python test_server.py"
echo "  3. Run:      python mcp_server.py"
echo ""
echo "Next steps:"
echo "  - Read ADD_MCP_SERVER.md to configure Cursor or Claude"
echo "  - Update paths in mcp_config.json for your system"
echo "  - Restart your LLM client after configuration"
echo ""
echo "Happy predicting! 📊🚀"
echo ""

