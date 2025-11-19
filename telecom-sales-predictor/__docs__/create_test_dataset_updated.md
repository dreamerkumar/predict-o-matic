# create_test_dataset_updated.py

## Purpose

This script generates a **test dataset for December 2025** by reading marketing campaign data from an Excel file and creating a properly formatted CSV file with daily records for both App and Web channels. The generated dataset is structured to match the format of `final_dataset.csv` and can be used with prediction models to forecast sales for December 2025.

## What It Does

1. **Reads Marketing Data**: Loads marketing campaign information from `updated Dec Marketing events.xlsx`
2. **Standardizes Data**: 
   - Normalizes channel names (app → App, web → Web)
   - Normalizes marketing event types (Push → Push, email → Email)
3. **Generates Date Range**: Creates a complete calendar for December 2025 (Dec 1-31, 2025)
4. **Creates Channel Records**: Generates two records per day (one for App, one for Web)
5. **Populates Marketing Volumes**: 
   - Maps Push notification volumes to App channel
   - Maps Email volumes to Web channel
   - Sets volumes to 0 for non-campaign days
6. **Outputs Summary**: Displays campaign statistics and saves the test dataset to CSV

## Prerequisites

### Required Files
- **`updated Dec Marketing events.xlsx`**: Excel file containing December 2025 marketing campaigns with columns:
  - `Date`: Date of the marketing event
  - `channel`: Distribution channel (app or web)
  - `Marketing event`: Type of marketing (Push or Email)
  - `volume`: Number of marketing messages sent

### Required Python Packages
```bash
pip install pandas numpy openpyxl
```

**Dependencies:**
- `pandas`: Data manipulation and CSV/Excel processing
- `numpy`: Numerical operations
- `openpyxl`: Excel file reading (required for `.xlsx` files)
- `datetime`: Date handling and manipulation

## How to Run

### Basic Execution
```bash
cd /path/to/telecom-sales-predictor
python create_test_dataset_updated.py
```

### Expected Output
The script will display:
1. **Marketing Events Data**: Shows the loaded marketing campaigns
2. **Dataset Creation Summary**: 
   - Date range covered
   - Total records generated
   - Records per day (always 2: App + Web)
   - Total days (31 for December)
3. **Sample Data**: First 20 rows of the generated dataset
4. **Campaign Details**: 
   - App channel Push notification dates and volumes
   - Web channel Email dates and volumes
5. **Campaign Statistics**:
   - Number of campaign days per channel
   - Total Push notifications sent (App)
   - Total Emails sent (Web)
6. **File Save Confirmation**: Path to the saved CSV file

### Output Files
- **Test Dataset**: `output_files/test_dataset_dec_2025_<timestamp>.csv`
  - 62 rows (31 days × 2 channels)
  - Columns: `Date`, `Channel`, `VAS_Sold`, `Speed_Upgrades`, `Emails_Sent`, `Push_Notifications_Sent`
  - `VAS_Sold` and `Speed_Upgrades` initialized to 0 (to be predicted)

## CSV Structure

### Output Format
```csv
Date,Channel,VAS_Sold,Speed_Upgrades,Emails_Sent,Push_Notifications_Sent
12/01/2025,App,0,0,0,0
12/01/2025,Web,0,0,0,0
12/02/2025,App,0,0,0,150000
12/02/2025,Web,0,0,0,0
...
```

### Field Descriptions
| Column | Type | Description |
|--------|------|-------------|
| `Date` | string | Date in MM/DD/YYYY format |
| `Channel` | string | "App" or "Web" |
| `VAS_Sold` | int | Set to 0 (placeholder for predictions) |
| `Speed_Upgrades` | int | Set to 0 (placeholder for predictions) |
| `Emails_Sent` | int | Number of marketing emails sent (Web channel) |
| `Push_Notifications_Sent` | int | Number of push notifications sent (App channel) |

## Dependencies on Other Files

### Direct Dependencies
- **`updated Dec Marketing events.xlsx`** (required): Must exist in the same directory
  - Contains marketing campaign schedule for December 2025
  - Used to populate `Emails_Sent` and `Push_Notifications_Sent` columns

### Output Used By
- **`predict_december_2025.py`**: Uses the generated test dataset for making predictions
- Prediction models expect this exact format and column structure

### Directory Structure Requirements
```
telecom-sales-predictor/
├── create_test_dataset_updated.py          # This script
├── updated Dec Marketing events.xlsx       # Required input file
└── output_files/                           # Created automatically
    └── test_dataset_dec_2025_<timestamp>.csv
```

## Marketing Data Format

### Expected Excel Structure
```
Date        | channel | Marketing event | volume
------------|---------|----------------|--------
12/2/2025   | app     | Push           | 150000
12/5/2025   | web     | email          | 200000
12/10/2025  | app     | Push           | 175000
...
```

### Notes on Marketing Data
- **Case Insensitive**: The script automatically capitalizes channel and event names
- **Multiple Events**: Same date/channel can have multiple events (volumes will be summed)
- **Missing Days**: Days without marketing campaigns will have 0 volumes
- **Channel Specificity**: 
  - Push notifications are only recorded for App channel
  - Emails are only recorded for Web channel

## Example Usage Workflow

### Step 1: Prepare Marketing Data
Create or update `updated Dec Marketing events.xlsx` with your December 2025 campaigns.

### Step 2: Run Script
```bash
python create_test_dataset_updated.py
```

### Step 3: Verify Output
Check the console output for:
- Correct date range (Dec 1-31, 2025)
- Expected number of campaign days
- Total marketing volumes match your planning

### Step 4: Use for Predictions
The generated CSV can now be used by `predict_december_2025.py`:
```bash
python predict_december_2025.py
```

## Troubleshooting

### Common Issues

1. **FileNotFoundError: updated Dec Marketing events.xlsx not found**
   - Ensure the Excel file exists in the same directory
   - Check file name exactly matches (including spaces and case)

2. **ModuleNotFoundError: No module named 'openpyxl'**
   ```bash
   pip install openpyxl
   ```
   This module is required for reading `.xlsx` files

3. **Date Parsing Errors**
   - Ensure dates in Excel file are in proper date format (not text)
   - Excel should recognize them as dates, not strings

4. **Volume Not Appearing**
   - Check channel names match: "app" or "web" (case insensitive)
   - Check event types match: "Push" or "Email" (case insensitive)
   - Verify dates are within December 2025

5. **Wrong Number of Records**
   - Should always be 62 records (31 days × 2 channels)
   - If different, check date range generation logic

## Customization

### To Change Date Range
```python
# Modify these lines:
start_date = datetime(2025, 12, 1)  # Start date
end_date = datetime(2025, 12, 31)   # End date
```

### To Add More Channels
```python
# Modify this line:
for channel in ['App', 'Web', 'NewChannel']:
```

### To Add More Marketing Event Types
```python
# Add logic for new event types:
elif row['Marketing event'] == 'SMS':
    sms_sent += int(row['volume'])
```

## Output Statistics Example

```
Campaign Statistics:
  App Channel:
    - Campaign days: 15
    - Total Push Notifications: 2,250,000
  Web Channel:
    - Campaign days: 12
    - Total Emails: 1,800,000
```

## Notes

- **All Days Included**: Even non-campaign days are included with 0 marketing volumes
- **Two-Channel Structure**: Every day has exactly 2 records (App and Web)
- **Format Consistency**: Output matches `final_dataset.csv` format for model compatibility
- **Timestamp in Filename**: Each run creates a new file to track versions
- **Ready for Prediction**: The generated CSV can be directly used for forecasting without modifications
- **Zero Sales Values**: `VAS_Sold` and `Speed_Upgrades` are set to 0 as placeholders for predictions

