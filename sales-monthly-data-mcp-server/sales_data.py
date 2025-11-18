#!/usr/bin/env python3
"""
Script to retrieve monthly sales data from a CSV file.
Accepts month and year parameters and returns sales data or 'No data exists'.
"""

import argparse
import csv
import sys
from pathlib import Path


def get_sales_data(month, year):
    """
    Retrieve sales data for the specified month and year.
    
    Args:
        month (str): The month to search for (e.g., 'January', 'February')
        year (str): The year to search for (e.g., '2023', '2024')
    
    Returns:
        str: The sales amount if found, or "No data exists" if not found
    """
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    csv_path = script_dir / 'sales_data.csv'
    
    # Validate that the CSV file exists
    if not csv_path.exists():
        print(f"Error: Sales data file not found at {csv_path}", file=sys.stderr)
        return "No data exists"
    
    # Normalize inputs for comparison
    month = month.strip().capitalize()
    year = year.strip()
    
    try:
        # Read the CSV file and look for matching month and year
        with open(csv_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if (row['month'].strip().capitalize() == month and 
                    row['year'].strip() == year):
                    return row['sales']
        
        # If we reach here, no matching data was found
        return "No data exists"
    
    except Exception as e:
        print(f"Error reading sales data: {e}", file=sys.stderr)
        return "No data exists"


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Retrieve sales data for a specific month and year'
    )
    parser.add_argument(
        'month',
        type=str,
        help='Month (e.g., January, February)'
    )
    parser.add_argument(
        'year',
        type=str,
        help='Year (e.g., 2023, 2024)'
    )
    
    try:
        args = parser.parse_args()
        result = get_sales_data(args.month, args.year)
        print(result)
        sys.exit(0)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
