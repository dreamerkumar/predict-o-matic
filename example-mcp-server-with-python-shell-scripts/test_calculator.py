#!/usr/bin/env python3
"""
Test script for calculator.py
"""

import subprocess
import sys


def run_calculator(operation, param1, param2):
    """Run calculator.py and return the result."""
    try:
        result = subprocess.run(
            ['python3', 'calculator.py', operation, str(param1), str(param2)],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except Exception as e:
        return -1, "", str(e)


def test_case(name, operation, param1, param2, expected):
    """Run a single test case."""
    returncode, stdout, stderr = run_calculator(operation, param1, param2)
    
    if returncode != 0:
        print(f"❌ {name}: FAILED - Process exited with code {returncode}")
        if stderr:
            print(f"   Error: {stderr}")
        return False
    
    try:
        result = float(stdout)
        if abs(result - expected) < 0.0001:  # Handle floating point comparison
            print(f"✅ {name}: PASSED - {operation}({param1}, {param2}) = {result}")
            return True
        else:
            print(f"❌ {name}: FAILED - Expected {expected}, got {result}")
            return False
    except ValueError:
        print(f"❌ {name}: FAILED - Invalid output: {stdout}")
        return False


def test_error_case(name, operation, param1, param2):
    """Test cases that should fail."""
    returncode, stdout, stderr = run_calculator(operation, param1, param2)
    
    if returncode != 0:
        print(f"✅ {name}: PASSED - Correctly failed with error")
        return True
    else:
        print(f"❌ {name}: FAILED - Should have failed but succeeded")
        return False


def main():
    print("=" * 60)
    print("Testing calculator.py")
    print("=" * 60)
    print()
    
    passed = 0
    failed = 0
    
    # Addition tests
    print("Addition Tests:")
    print("-" * 60)
    tests = [
        ("Add positive numbers", "add", 5, 3, 8),
        ("Add negative numbers", "add", -5, -3, -8),
        ("Add positive and negative", "add", 10, -4, 6),
        ("Add with zero", "add", 0, 7, 7),
        ("Add decimals", "add", 2.5, 3.7, 6.2),
    ]
    
    for test in tests:
        if test_case(*test):
            passed += 1
        else:
            failed += 1
    
    print()
    
    # Multiplication tests
    print("Multiplication Tests:")
    print("-" * 60)
    tests = [
        ("Multiply positive numbers", "multiply", 5, 3, 15),
        ("Multiply negative numbers", "multiply", -5, -3, 15),
        ("Multiply positive and negative", "multiply", 10, -4, -40),
        ("Multiply by zero", "multiply", 0, 7, 0),
        ("Multiply decimals", "multiply", 2.5, 4, 10.0),
    ]
    
    for test in tests:
        if test_case(*test):
            passed += 1
        else:
            failed += 1
    
    print()
    
    # Error cases
    print("Error Handling Tests:")
    print("-" * 60)
    error_tests = [
        ("Invalid operation", "divide", 5, 3),
        ("Non-numeric first param", "add", "abc", 3),
        ("Non-numeric second param", "multiply", 5, "xyz"),
    ]
    
    for test in error_tests:
        if test_error_case(*test):
            passed += 1
        else:
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print(f"❌ {failed} test(s) failed")
        sys.exit(1)


if __name__ == '__main__':
    main()

