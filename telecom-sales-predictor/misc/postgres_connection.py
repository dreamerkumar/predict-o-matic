import psycopg2
from psycopg2 import Error
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def connect_to_postgres():
    """
    Connect to PostgreSQL database and perform basic operations
    """
    connection = None
    cursor = None

    try:
        # Connect to PostgreSQL database using environment variables
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_DATABASE'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT')
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Print PostgreSQL connection properties
        print("Connected to PostgreSQL database successfully!")

        # Execute a test query to get database version
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"Database version: {db_version[0]}")

        # Show connection info
        dsn_params = connection.get_dsn_parameters()
        print(f"\nConnection details:")
        print(f"  Host: {dsn_params.get('host', 'N/A')}")
        print(f"  Database: {dsn_params.get('dbname', 'N/A')}")
        print(f"  User: {dsn_params.get('user', 'N/A')}")
        print(f"  Port: {dsn_params.get('port', 'N/A')}")

        # Read tables into pandas DataFrames
        print("\nReading tables into DataFrames...")

        # Read telecom_sales_marketing_events_enhanced
        sales_marketing_query = "SELECT * FROM team_predictomatic.telecom_sales_marketing_events_enhanced"
        df_sales_marketing = pd.read_sql_query(sales_marketing_query, connection)
        print(f"\n✓ Loaded telecom_sales_marketing_events_enhanced: {df_sales_marketing.shape[0]} rows, {df_sales_marketing.shape[1]} columns")

        # Read telecom_logins_engagement_enhanced
        logins_engagement_query = "SELECT * FROM team_predictomatic.telecom_logins_engagement_enhanced"
        df_logins_engagement = pd.read_sql_query(logins_engagement_query, connection)
        print(f"✓ Loaded telecom_logins_engagement_enhanced: {df_logins_engagement.shape[0]} rows, {df_logins_engagement.shape[1]} columns")

        # Read table1_vas_sales_marketing_events
        vas_sales_marketing_query = "SELECT * FROM team_predictomatic.table1_vas_sales_marketing_events"
        df_vas_sales_marketing = pd.read_sql_query(vas_sales_marketing_query, connection)
        print(f"✓ Loaded table1_vas_sales_marketing_events: {df_vas_sales_marketing.shape[0]} rows, {df_vas_sales_marketing.shape[1]} columns")

        # Display basic information about the DataFrames
        print("\n" + "="*60)
        print("SALES & MARKETING EVENTS DataFrame Info:")
        print("="*60)
        print(df_sales_marketing.info())
        print("\nFirst 5 rows:")
        print(df_sales_marketing.head())

        print("\n" + "="*60)
        print("LOGINS & ENGAGEMENT DataFrame Info:")
        print("="*60)
        print(df_logins_engagement.info())
        print("\nFirst 5 rows:")
        print(df_logins_engagement.head())

        print("\n" + "="*60)
        print("VAS SALES & MARKETING EVENTS DataFrame Info:")
        print("="*60)
        print(df_vas_sales_marketing.info())
        print("\nFirst 5 rows:")
        print(df_vas_sales_marketing.head())

        # Return the DataFrames
        return df_sales_marketing, df_logins_engagement, df_vas_sales_marketing

    except (Exception, Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")

    finally:
        # Close database connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("PostgreSQL connection closed")

if __name__ == "__main__":
    result = connect_to_postgres()
    if result:
        df_sales_marketing, df_logins_engagement, df_vas_sales_marketing = result
        print("\n" + "="*60)
        print("DataFrames successfully loaded and ready to use!")
        print("="*60)
