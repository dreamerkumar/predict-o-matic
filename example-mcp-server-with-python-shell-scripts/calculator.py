#!/usr/bin/env python3
"""
Simple calculator CLI script that performs addition or multiplication.
"""

import argparse
import sys


def add(a, b):
    """Add two numbers."""
    return a + b


def multiply(a, b):
    """Multiply two numbers."""
    return a * b


def main():
    parser = argparse.ArgumentParser(
        description='Simple calculator that adds or multiplies two numbers'
    )
    parser.add_argument(
        'operation',
        choices=['add', 'multiply'],
        help='Operation to perform: add or multiply'
    )
    parser.add_argument(
        'param1',
        type=float,
        help='First number'
    )
    parser.add_argument(
        'param2',
        type=float,
        help='Second number'
    )
    
    try:
        args = parser.parse_args()
        
        if args.operation == 'add':
            result = add(args.param1, args.param2)
        elif args.operation == 'multiply':
            result = multiply(args.param1, args.param2)
        else:
            print(f"Error: Invalid operation '{args.operation}'", file=sys.stderr)
            sys.exit(1)
        
        print(result)
        sys.exit(0)
        
    except ValueError as e:
        print(f"Error: Invalid number format - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

