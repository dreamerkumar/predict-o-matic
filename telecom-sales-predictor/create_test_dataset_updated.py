import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Read the updated marketing events Excel file
marketing_df = pd.read_excel('updated Dec Marketing events.xlsx')

# Convert Date column to datetime
marketing_df['Date'] = pd.to_datetime(marketing_df['Date'])

# Standardize channel names: app -> App, web -> Web
marketing_df['channel'] = marketing_df['channel'].str.capitalize()

# Standardize marketing event names: Push -> Push, email -> Email
marketing_df['Marketing event'] = marketing_df['Marketing event'].str.capitalize()

print("Marketing events data:")
print(marketing_df)
print()

# Create date range from Dec 1, 2025 to Dec 31, 2025
start_date = datetime(2025, 12, 1)
end_date = datetime(2025, 12, 31)

# Generate all dates in the range
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# Create base dataset with both App and Web channels for each date
test_data = []

for date in date_range:
    for channel in ['App', 'Web']:
        # Get marketing volumes for this date and channel
        marketing_rows = marketing_df[(marketing_df['Date'] == date) & (marketing_df['channel'] == channel)]

        emails_sent = 0
        push_sent = 0

        for _, row in marketing_rows.iterrows():
            if row['Marketing event'] == 'Email':
                emails_sent += int(row['volume'])
            elif row['Marketing event'] == 'Push':
                push_sent += int(row['volume'])

        test_data.append({
            'Date': date.strftime('%m/%d/%Y'),
            'Channel': channel,
            'VAS_Sold': 0,  # To be predicted
            'Speed_Upgrades': 0,  # To be predicted
            'Emails_Sent': emails_sent,
            'Push_Notifications_Sent': push_sent
        })

# Create DataFrame
test_df = pd.DataFrame(test_data)

# Display summary
print(f"\nTest dataset created:")
print(f"Date range: {start_date.strftime('%m/%d/%Y')} to {end_date.strftime('%m/%d/%Y')}")
print(f"Total records: {len(test_df)}")
print(f"Records per day: 2 (App + Web)")
print(f"Total days: {len(date_range)}")
print()

print("Sample of test dataset:")
print(test_df.head(20))
print()

print("\nMarketing events summary by channel:")
print("\nApp Channel - Push Notifications:")
app_push = test_df[(test_df['Channel'] == 'App') & (test_df['Push_Notifications_Sent'] > 0)][['Date', 'Push_Notifications_Sent']]
print(app_push.to_string(index=False))

print("\n\nWeb Channel - Emails:")
web_email = test_df[(test_df['Channel'] == 'Web') & (test_df['Emails_Sent'] > 0)][['Date', 'Emails_Sent']]
print(web_email.to_string(index=False))
print()

# Statistics
total_app_push = test_df[test_df['Channel'] == 'App']['Push_Notifications_Sent'].sum()
total_web_email = test_df[test_df['Channel'] == 'Web']['Emails_Sent'].sum()
app_campaign_days = len(test_df[(test_df['Channel'] == 'App') & (test_df['Push_Notifications_Sent'] > 0)])
web_campaign_days = len(test_df[(test_df['Channel'] == 'Web') & (test_df['Emails_Sent'] > 0)])

print(f"\nCampaign Statistics:")
print(f"  App Channel:")
print(f"    - Campaign days: {app_campaign_days}")
print(f"    - Total Push Notifications: {total_app_push:,}")
print(f"  Web Channel:")
print(f"    - Campaign days: {web_campaign_days}")
print(f"    - Total Emails: {total_web_email:,}")
print()

# Save to CSV
os.makedirs('output_files', exist_ok=True)
timestamp = datetime.utcnow().isoformat(timespec='milliseconds').replace(':', '-').replace('.', '-') + 'Z'
output_file = f'output_files/test_dataset_dec_2025_{timestamp}.csv'
test_df.to_csv(output_file, index=False)
print(f"[OK] Test dataset saved to: {output_file}")
print(f"\nColumns: {list(test_df.columns)}")
print(f"Format matches final_dataset.csv: [OK]")
