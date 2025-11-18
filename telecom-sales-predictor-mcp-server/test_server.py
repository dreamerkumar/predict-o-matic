#!/usr/bin/env python3
"""
Simple test script to verify the MCP server setup is correct.
Run this before integrating with Cursor or Claude.
"""

import sys
from pathlib import Path

def main():
    """Run setup verification tests."""
    print("="*60)
    print("TELECOM PREDICTOR MCP SERVER - SETUP VERIFICATION")
    print("="*60)
    print()
    
    all_passed = True
    
    # Test 1: Python version
    print("Test 1: Python Version")
    print("-" * 40)
    version = sys.version_info
    print(f"Current Python: {version.major}.{version.minor}.{version.micro}")
    if version >= (3, 10):
        print("✅ PASS: Python 3.10+ detected")
    else:
        print("❌ FAIL: Need Python 3.10+")
        all_passed = False
    print()
    
    # Test 2: MCP SDK
    print("Test 2: MCP SDK Installation")
    print("-" * 40)
    try:
        import mcp
        from mcp.server import Server
        from mcp.types import Tool, TextContent, ImageContent
        print("✅ PASS: MCP SDK installed")
        print("   Core modules: Server, Tool, TextContent, ImageContent")
    except ImportError as e:
        print("❌ FAIL: MCP SDK not installed")
        print(f"   Error: {e}")
        print("   Run: pip install -r requirements.txt")
        all_passed = False
    print()
    
    # Test 3: Required packages
    print("Test 3: Required Packages")
    print("-" * 40)
    required_packages = ['pandas', 'numpy', 'sklearn', 'matplotlib']
    for package in required_packages:
        try:
            if package == 'sklearn':
                __import__('sklearn')
            else:
                __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} NOT installed")
            all_passed = False
    print()
    
    # Test 4: Analysis script exists
    print("Test 4: Analysis Script")
    print("-" * 40)
    script_path = Path(__file__).parent.parent / "telecom-sales-predictor" / "analyze_data.py"
    if script_path.exists():
        print(f"✅ PASS: Found at {script_path}")
    else:
        print(f"❌ FAIL: Not found at {script_path}")
        all_passed = False
    print()
    
    # Test 5: Data file exists
    print("Test 5: Data File")
    print("-" * 40)
    data_path = Path(__file__).parent.parent / "telecom-sales-predictor" / "final_dataset.csv"
    if data_path.exists():
        print(f"✅ PASS: Found at {data_path}")
        # Show file size
        size_mb = data_path.stat().st_size / (1024 * 1024)
        print(f"   File size: {size_mb:.2f} MB")
    else:
        print(f"❌ FAIL: Not found at {data_path}")
        all_passed = False
    print()
    
    # Test 6: MCP server script
    print("Test 6: MCP Server Script")
    print("-" * 40)
    server_path = Path(__file__).parent / "mcp_server.py"
    if server_path.exists():
        print(f"✅ PASS: Found at {server_path}")
    else:
        print(f"❌ FAIL: Not found at {server_path}")
        all_passed = False
    print()
    
    # Test 7: Try importing the server
    print("Test 7: Server Import Test")
    print("-" * 40)
    try:
        # Add current directory to path
        sys.path.insert(0, str(Path(__file__).parent))
        # Try to import (but don't run)
        import mcp_server
        print("✅ PASS: Server imports without errors")
    except Exception as e:
        print(f"❌ FAIL: Server import error: {e}")
        all_passed = False
    print()
    
    # Summary
    print("="*60)
    print("SUMMARY")
    print("="*60)
    if all_passed:
        print("✅ All tests passed! You're ready to configure the MCP server.")
        print()
        print("Next steps:")
        print("1. Read ADD_MCP_SERVER.md for configuration instructions")
        print("2. Add the server to Cursor or Claude Desktop")
        print("3. Restart your LLM client")
        print("4. Test with: 'Generate sales predictions'")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print()
        print("Common fixes:")
        print("- Run: pip install -r requirements.txt")
        print("- Ensure Python 3.10+ is active in virtual environment")
        print("- Verify directory structure is correct")
        print("- Check that telecom-sales-predictor directory exists")
    print()
    print("="*60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

