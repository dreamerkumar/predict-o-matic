import pandas as pd
from postgres_connection import connect_to_postgres

def main():
    """
    Analyze telecom data from PostgreSQL database
    """
    print("Loading data from PostgreSQL database...")
    print("="*60)

    # Get DataFrames from database
    result = connect_to_postgres()

    if not result:
        print("Failed to load data from database")
        return

    df_sales_marketing, df_logins_engagement, df_vas_sales_marketing = result

    # Now you can work with the DataFrames
    print("\n" + "="*60)
    print("DATA ANALYSIS")
    print("="*60)

    # Sales & Marketing Events Analysis
    print("\n1. SALES & MARKETING EVENTS SUMMARY:")
    print(f"   Total records: {len(df_sales_marketing)}")
    print(f"   Columns: {list(df_sales_marketing.columns)}")
    print(f"\n   Data types:\n{df_sales_marketing.dtypes}")
    print(f"\n   Missing values:\n{df_sales_marketing.isnull().sum()}")

    # Logins & Engagement Analysis
    print("\n2. LOGINS & ENGAGEMENT SUMMARY:")
    print(f"   Total records: {len(df_logins_engagement)}")
    print(f"   Columns: {list(df_logins_engagement.columns)}")
    print(f"\n   Data types:\n{df_logins_engagement.dtypes}")
    print(f"\n   Missing values:\n{df_logins_engagement.isnull().sum()}")

    # VAS Sales & Marketing Events Analysis
    print("\n3. VAS SALES & MARKETING EVENTS SUMMARY:")
    print(f"   Total records: {len(df_vas_sales_marketing)}")
    print(f"   Columns: {list(df_vas_sales_marketing.columns)}")
    print(f"\n   Data types:\n{df_vas_sales_marketing.dtypes}")
    print(f"\n   Missing values:\n{df_vas_sales_marketing.isnull().sum()}")

    # Basic statistics
    print("\n4. BASIC STATISTICS:")
    print("\n   Sales & Marketing Events - Numeric columns:")
    print(df_sales_marketing.describe())

    print("\n   Logins & Engagement - Numeric columns:")
    print(df_logins_engagement.describe())

    print("\n   VAS Sales & Marketing Events - Numeric columns:")
    print(df_vas_sales_marketing.describe())

    # You can perform additional analysis here
    # Example: df_sales_marketing['column_name'].value_counts()
    # Example: df_logins_engagement.groupby('column_name').size()
    # Example: df_vas_sales_marketing['column_name'].value_counts()

    return df_sales_marketing, df_logins_engagement, df_vas_sales_marketing

if __name__ == "__main__":
    df_sales_marketing, df_logins_engagement, df_vas_sales_marketing = main()
    print("\n" + "="*60)
    print("DataFrames are ready for further analysis!")
    print("="*60)
