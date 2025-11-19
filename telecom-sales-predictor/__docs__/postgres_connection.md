# postgres_connection.py

## Purpose

This script establishes a **PostgreSQL database connection** to retrieve telecom sales and marketing data from a cloud database. It connects to a PostgreSQL database, queries three specific tables from the `team_predictomatic` schema, loads them into Pandas DataFrames, and displays basic information about the retrieved data.

This is a **data acquisition utility** located in the `misc/` folder, used for fetching raw data from the database before it's processed into the `final_dataset.csv` training file.

## What It Does

1. **Loads Environment Variables**: Reads database credentials from `.env` file
2. **Connects to PostgreSQL**: Establishes secure connection using psycopg2
3. **Displays Connection Info**: Shows database version and connection parameters
4. **Queries Three Tables**:
   - `telecom_sales_marketing_events_enhanced`: Sales and marketing event data
   - `telecom_logins_engagement_enhanced`: User login and engagement metrics
   - `table1_vas_sales_marketing_events`: VAS (Value-Added Services) sales data
5. **Loads Data into Pandas**: Converts SQL query results to DataFrames
6. **Displays Data Info**: Shows shape, info, and first 5 rows of each DataFrame
7. **Closes Connection**: Properly closes database connection

## Prerequisites

### Required Files
- **`.env`**: Environment file with database credentials (in parent or misc directory)
  ```env
  DB_HOST=your-database-host.com
  DB_DATABASE=your_database_name
  DB_USER=your_username
  DB_PASSWORD=your_password
  DB_PORT=5432
  ```

### Required Python Packages
```bash
pip install psycopg2-binary pandas python-dotenv
```

**Dependencies:**
- `psycopg2` or `psycopg2-binary`: PostgreSQL adapter for Python
- `pandas`: DataFrame operations and SQL query execution
- `python-dotenv`: Load environment variables from `.env` file
- `os`: Standard library for environment variable access

### Database Access
- Valid PostgreSQL database credentials
- Read access to `team_predictomatic` schema
- Network connectivity to database host
- Firewall/VPN configuration (if required)

## How to Run

### From misc/ Directory
```bash
cd /path/to/telecom-sales-predictor/misc
python postgres_connection.py
```

### From Root Directory
```bash
cd /path/to/telecom-sales-predictor
python misc/postgres_connection.py
```

### Expected Output
The script displays:
1. **Connection Confirmation**: Success message with database version
2. **Connection Details**: Host, database name, user, port
3. **Table Loading Progress**: 
   - ✓ telecom_sales_marketing_events_enhanced: X rows, Y columns
   - ✓ telecom_logins_engagement_enhanced: X rows, Y columns
   - ✓ table1_vas_sales_marketing_events: X rows, Y columns
4. **DataFrame Info** (for each table):
   - Column names and data types
   - Non-null counts
   - Memory usage
   - First 5 rows preview
5. **Completion Message**: DataFrames ready to use
6. **Connection Closed**: PostgreSQL connection closed

## Database Schema

### Tables Queried

#### 1. telecom_sales_marketing_events_enhanced
**Purpose**: Main sales and marketing campaign data

**Typical Columns**:
- `date`: Date of record
- `channel`: Distribution channel (App/Web)
- `vas_sold`: Value-added services sold
- `speed_upgrades`: Internet speed upgrades sold
- `emails_sent`: Marketing emails sent
- `push_notifications_sent`: Push notifications sent
- Additional enhanced metrics

#### 2. telecom_logins_engagement_enhanced
**Purpose**: User engagement and login metrics

**Typical Columns**:
- `date`: Date of record
- `channel`: Distribution channel
- `logins`: Number of user logins
- `active_users`: Active user count
- `session_duration`: Average session time
- Engagement metrics

#### 3. table1_vas_sales_marketing_events
**Purpose**: Detailed VAS sales with marketing event correlation

**Typical Columns**:
- `date`: Date of record
- `vas_type`: Type of value-added service
- `sales_count`: Number of sales
- `marketing_event`: Associated marketing campaign
- Campaign details

## Environment Variables

### Required Variables
```env
DB_HOST=hostname.database.com
DB_DATABASE=telecom_analytics
DB_USER=data_analyst
DB_PASSWORD=secure_password_here
DB_PORT=5432
```

### Variable Descriptions
| Variable | Description | Example |
|----------|-------------|---------|
| `DB_HOST` | Database server hostname/IP | `postgres.example.com` |
| `DB_DATABASE` | Database name | `telecom_analytics` |
| `DB_USER` | Database username | `analyst_user` |
| `DB_PASSWORD` | Database password | `Str0ng_P@ssw0rd!` |
| `DB_PORT` | PostgreSQL port (usually 5432) | `5432` |

### Security Best Practices
- **Never commit `.env` to version control**
- Add `.env` to `.gitignore`
- Use strong, unique passwords
- Rotate credentials regularly
- Use read-only database users when possible

## Dependencies on Other Files

### Direct Dependencies
- **`.env`** (required): Database credentials file
  - Should be in parent directory or `misc/` directory
  - Used by `python-dotenv` to load environment variables

### Output
- Returns three Pandas DataFrames (in-memory only)
- Does NOT save to files by default
- Used for exploratory data analysis

### Related Scripts
- This is typically the **first step** in data pipeline
- Data from these tables would be processed/combined
- Eventually transformed into `final_dataset.csv`
- No direct dependencies on other Python scripts

### Directory Structure
```
telecom-sales-predictor/
├── .env                                    # Database credentials (required)
└── misc/
    └── postgres_connection.py             # This script
```

## Return Values

When run as a module (not `__main__`):
```python
from misc.postgres_connection import connect_to_postgres

result = connect_to_postgres()
if result:
    df_sales_marketing, df_logins_engagement, df_vas_sales_marketing = result
    
    # Now you can use the DataFrames
    print(df_sales_marketing.head())
```

Returns `None` if connection fails.

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'psycopg2'**
   ```bash
   pip install psycopg2-binary
   ```
   Note: Use `psycopg2-binary` for easier installation (no compilation required)

2. **ModuleNotFoundError: No module named 'dotenv'**
   ```bash
   pip install python-dotenv
   ```

3. **FileNotFoundError: .env file not found**
   - Create `.env` file in project root or `misc/` directory
   - Ensure it contains all required variables
   - Check file name (exactly `.env`, not `env.txt` or `.env.txt`)

4. **psycopg2.OperationalError: could not connect to server**
   - Verify `DB_HOST` is correct and accessible
   - Check firewall/VPN requirements
   - Verify port 5432 is not blocked
   - Test with `telnet DB_HOST 5432`

5. **psycopg2.OperationalError: FATAL: password authentication failed**
   - Verify `DB_USER` and `DB_PASSWORD` are correct
   - Check for extra spaces in `.env` file
   - Ensure user has database access permissions

6. **psycopg2.Error: relation "table_name" does not exist**
   - Verify schema name (`team_predictomatic`)
   - Check table names are correct
   - Ensure user has read permissions on schema

7. **Connection timeout**
   - Check network connectivity
   - Verify VPN connection (if required)
   - Increase connection timeout in psycopg2.connect()

## Customization Options

### Add Connection Timeout
```python
connection = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_DATABASE'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT'),
    connect_timeout=10  # 10 seconds
)
```

### Query with Date Filters
```python
query = """
    SELECT * 
    FROM team_predictomatic.telecom_sales_marketing_events_enhanced
    WHERE date >= '2024-01-01' AND date <= '2024-12-31'
"""
df = pd.read_sql_query(query, connection)
```

### Save DataFrames to CSV
```python
df_sales_marketing.to_csv('sales_marketing_data.csv', index=False)
df_logins_engagement.to_csv('logins_engagement_data.csv', index=False)
df_vas_sales_marketing.to_csv('vas_sales_data.csv', index=False)
```

### Use Connection Pooling (for multiple queries)
```python
from psycopg2 import pool

connection_pool = pool.SimpleConnectionPool(
    1, 20,  # min and max connections
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_DATABASE'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT')
)
```

## Security Considerations

### Never Hard-Code Credentials
❌ **Bad:**
```python
connection = psycopg2.connect(
    host="postgres.example.com",
    user="admin",
    password="password123"  # NEVER DO THIS!
)
```

✅ **Good:**
```python
connection = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
```

### Use SSL Connections (Production)
```python
connection = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_DATABASE'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT'),
    sslmode='require'  # Force SSL
)
```

### Principle of Least Privilege
- Use database users with **read-only** permissions
- Restrict access to only required tables
- Use role-based access control

## Example .env File

```env
# PostgreSQL Database Configuration
# DO NOT COMMIT THIS FILE TO VERSION CONTROL!

DB_HOST=postgres.company.com
DB_DATABASE=telecom_analytics
DB_USER=readonly_analyst
DB_PASSWORD=Str0ng_S3cur3_P@ssw0rd!
DB_PORT=5432
```

## Data Pipeline Context

This script is typically used in the following workflow:

1. **Run postgres_connection.py** → Fetch raw data from database
2. **Explore/Clean Data** → Pandas operations to prepare data
3. **Feature Engineering** → Create derived features
4. **Combine Tables** → Join/merge multiple sources
5. **Save to CSV** → Create `final_dataset.csv`
6. **Run analyze_data_hybrid.py** → Train models on prepared data

## Notes

- This is a **data acquisition utility** in `misc/` folder
- Used for initial data exploration and extraction
- Does **not** save data to files automatically
- Requires **active database connection** and credentials
- Uses `psycopg2` for PostgreSQL-specific optimizations
- Properly closes connections in `finally` block
- Returns DataFrames for further processing
- Displays comprehensive data info for debugging
- Schema is `team_predictomatic` (specific to this project)
- Three tables represent different data aspects:
  - Sales & marketing events (main data)
  - User engagement (context)
  - VAS-specific sales (detail)
- Connection details are displayed but password is hidden
- Memory-efficient with `pd.read_sql_query()` for large result sets
- Script is **read-only** (no INSERT/UPDATE/DELETE operations)

