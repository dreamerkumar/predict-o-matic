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
    print("Updated for dual-tool architecture")
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
        print(f"   MCP version: {mcp.__version__ if hasattr(mcp, '__version__') else 'unknown'}")
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
            print("   Note: Analysis scripts use their own venv")
            # Don't fail - these packages might be in the analysis project's venv
    print()
    
    # Test 4: Analysis scripts exist
    print("Test 4: Analysis Scripts")
    print("-" * 40)
    
    # Script 1: Hybrid analysis
    script1_path = Path(__file__).parent.parent / "telecom-sales-predictor" / "analyze_data_hybrid.py"
    if script1_path.exists():
        print(f"✅ PASS: analyze_data_hybrid.py found")
        print(f"   Path: {script1_path}")
    else:
        print(f"❌ FAIL: analyze_data_hybrid.py not found")
        print(f"   Expected: {script1_path}")
        all_passed = False
    
    # Script 2: December prediction
    script2_path = Path(__file__).parent.parent / "telecom-sales-predictor" / "predict_december_2025.py"
    if script2_path.exists():
        print(f"✅ PASS: predict_december_2025.py found")
        print(f"   Path: {script2_path}")
    else:
        print(f"❌ FAIL: predict_december_2025.py not found")
        print(f"   Expected: {script2_path}")
        all_passed = False
    print()
    
    # Test 5: Data files exist
    print("Test 5: Data Files")
    print("-" * 40)
    
    # File 1: Training data
    data1_path = Path(__file__).parent.parent / "telecom-sales-predictor" / "final_dataset.csv"
    if data1_path.exists():
        size_kb = data1_path.stat().st_size / 1024
        print(f"✅ PASS: final_dataset.csv found")
        print(f"   Size: {size_kb:.1f} KB")
    else:
        print(f"❌ FAIL: final_dataset.csv not found")
        print(f"   Expected: {data1_path}")
        all_passed = False
    
    # File 2: Test data
    data2_path = Path(__file__).parent.parent / "telecom-sales-predictor" / "test_dataset_dec_2025.csv"
    if data2_path.exists():
        size_kb = data2_path.stat().st_size / 1024
        print(f"✅ PASS: test_dataset_dec_2025.csv found")
        print(f"   Size: {size_kb:.1f} KB")
    else:
        print(f"⚠️  WARN: test_dataset_dec_2025.csv not found")
        print(f"   Expected: {data2_path}")
        print(f"   Note: December predictions won't work without this file")
        print(f"   Run: create_test_dataset_updated.py to generate it")
        # Don't fail - hybrid analysis can still work
    print()
    
    # Test 6: Output directory
    print("Test 6: Output Directory")
    print("-" * 40)
    output_dir = Path(__file__).parent.parent / "telecom-sales-predictor" / "output_files"
    if output_dir.exists():
        print(f"✅ PASS: output_files/ directory exists")
        # Count files
        png_files = list(output_dir.glob("*.png"))
        csv_files = list(output_dir.glob("*.csv"))
        print(f"   PNG files: {len(png_files)}")
        print(f"   CSV files: {len(csv_files)}")
    else:
        print(f"ℹ️  INFO: output_files/ directory doesn't exist yet")
        print("   Will be created automatically on first run")
    print()
    
    # Test 7: MCP server script
    print("Test 7: MCP Server Script")
    print("-" * 40)
    server_path = Path(__file__).parent / "mcp_server.py"
    if server_path.exists():
        print(f"✅ PASS: Found at {server_path}")
    else:
        print(f"❌ FAIL: Not found at {server_path}")
        all_passed = False
    print()
    
    # Test 8: Try importing the server
    print("Test 8: Server Import Test")
    print("-" * 40)
    try:
        # Add current directory to path
        sys.path.insert(0, str(Path(__file__).parent))
        # Try to import (but don't run)
        import mcp_server
        print("✅ PASS: Server imports without errors")
        
        # Check for tool functions
        if hasattr(mcp_server, 'list_tools'):
            print("✅ PASS: list_tools() function found")
        if hasattr(mcp_server, 'call_tool'):
            print("✅ PASS: call_tool() function found")
        if hasattr(mcp_server, 'run_hybrid_analysis'):
            print("✅ PASS: run_hybrid_analysis() function found")
        if hasattr(mcp_server, 'run_december_prediction'):
            print("✅ PASS: run_december_prediction() function found")
            
    except Exception as e:
        print(f"❌ FAIL: Server import error: {e}")
        all_passed = False
    print()
    
    # Summary
    print("="*60)
    print("SUMMARY")
    print("="*60)
    if all_passed:
        print("✅ All critical tests passed!")
        print()
        print("🎉 You're ready to configure the MCP server.")
        print()
        print("Your MCP server exposes TWO tools:")
        print("  1. analyze_hybrid_model - Train & evaluate models")
        print("  2. predict_december_2025 - Generate December forecasts")
        print()
        print("Next steps:")
        print("1. Read ADD_MCP_SERVER.md for configuration instructions")
        print("2. Add the server to Cursor or Claude Desktop")
        print("3. Restart your LLM client")
        print("4. Test Tool 1: 'Analyze the hybrid model'")
        print("5. Test Tool 2: 'Predict December 2025 sales'")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print()
        print("Common fixes:")
        print("- Run: pip install -r requirements.txt")
        print("- Ensure Python 3.10+ is active in virtual environment")
        print("- Verify directory structure is correct")
        print("- Check that telecom-sales-predictor directory exists")
        print("- Run create_test_dataset_updated.py for December test data")
    print()
    print("="*60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
