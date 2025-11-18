import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_holiday_features(date):
    """
    Determine if a date is a federal holiday or near a federal holiday.
    Returns: (is_holiday, days_to_holiday, days_from_holiday)
    """
    holidays_2025 = [
        pd.Timestamp('2025-01-01'),  # New Year's Day
        pd.Timestamp('2025-01-20'),  # Martin Luther King Jr. Day
        pd.Timestamp('2025-02-17'),  # Presidents' Day
        pd.Timestamp('2025-05-26'),  # Memorial Day
        pd.Timestamp('2025-06-19'),  # Juneteenth
        pd.Timestamp('2025-07-04'),  # Independence Day
        pd.Timestamp('2025-09-01'),  # Labor Day
        pd.Timestamp('2025-10-13'),  # Columbus Day
        pd.Timestamp('2025-11-11'),  # Veterans Day
        pd.Timestamp('2025-11-27'),  # Thanksgiving
        pd.Timestamp('2025-12-25'),  # Christmas
    ]

    all_holidays = holidays_2025

    # Check if current date is a holiday
    is_holiday = 1 if date in all_holidays else 0

    # Calculate days to nearest holiday
    if all_holidays:
        days_diff = [(holiday - date).days for holiday in all_holidays]

        # Days to next holiday (positive values only)
        future_days = [d for d in days_diff if d >= 0]
        days_to_holiday = min(future_days) if future_days else 365

        # Days from previous holiday (negative values, take absolute)
        past_days = [abs(d) for d in days_diff if d < 0]
        days_from_holiday = min(past_days) if past_days else 365
    else:
        days_to_holiday = 365
        days_from_holiday = 365

    return is_holiday, days_to_holiday, days_from_holiday

print("="*80)
print("DECEMBER 2025 SALES PREDICTION")
print("Using Hybrid Model: Random Forest (VAS_Sold) + Linear Regression (Speed_Upgrades)")
print("="*80)

# Load the training data to train the models
print("\n[1/5] Loading training data...")
df_train = pd.read_csv('final_dataset.csv')
df_train['Date'] = pd.to_datetime(df_train['Date'])

# Feature engineering on training data
df_train['Day_of_Year'] = df_train['Date'].dt.dayofyear
df_train['Day_of_Week'] = df_train['Date'].dt.dayofweek
df_train['Month'] = df_train['Date'].dt.month

# Add holiday features
holiday_features = df_train['Date'].apply(get_holiday_features)
df_train['Is_Holiday'] = holiday_features.apply(lambda x: x[0])
df_train['Days_To_Holiday'] = holiday_features.apply(lambda x: x[1])
df_train['Days_From_Holiday'] = holiday_features.apply(lambda x: x[2])
df_train['Near_Holiday'] = ((df_train['Days_To_Holiday'] <= 1) | (df_train['Days_From_Holiday'] <= 1)).astype(int)

# Encode Channel
le = LabelEncoder()
df_train['Channel_Encoded'] = le.fit_transform(df_train['Channel'])

feature_columns = ['Day_of_Year', 'Day_of_Week', 'Month', 'Channel_Encoded',
                   'Emails_Sent', 'Push_Notifications_Sent',
                   'Is_Holiday', 'Days_To_Holiday', 'Days_From_Holiday', 'Near_Holiday']

X_train = df_train[feature_columns]

print(f"  Training records: {len(df_train)}")

# Train Random Forest for VAS_Sold
print("\n[2/5] Training Random Forest for VAS_Sold...")
y_vas = df_train['VAS_Sold']
model_vas = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features='sqrt',
    random_state=42,
    n_jobs=-1
)
model_vas.fit(X_train, y_vas)
print("  [OK] Random Forest trained")

# Train Linear Regression for Speed_Upgrades
print("\n[3/5] Training Linear Regression for Speed_Upgrades...")
y_upgrades = df_train['Speed_Upgrades']
model_upgrades = LinearRegression()
model_upgrades.fit(X_train, y_upgrades)
print("  [OK] Linear Regression trained")

# Load December test data
print("\n[4/5] Loading December 2025 test data...")
df_test = pd.read_csv('test_dataset_dec_2025.csv')
df_test['Date'] = pd.to_datetime(df_test['Date'])

# Feature engineering on test data
df_test['Day_of_Year'] = df_test['Date'].dt.dayofyear
df_test['Day_of_Week'] = df_test['Date'].dt.dayofweek
df_test['Month'] = df_test['Date'].dt.month

# Add holiday features
holiday_features_test = df_test['Date'].apply(get_holiday_features)
df_test['Is_Holiday'] = holiday_features_test.apply(lambda x: x[0])
df_test['Days_To_Holiday'] = holiday_features_test.apply(lambda x: x[1])
df_test['Days_From_Holiday'] = holiday_features_test.apply(lambda x: x[2])
df_test['Near_Holiday'] = ((df_test['Days_To_Holiday'] <= 1) | (df_test['Days_From_Holiday'] <= 1)).astype(int)

# Encode Channel using the same encoder
df_test['Channel_Encoded'] = le.transform(df_test['Channel'])

# Prepare features for prediction
X_test = df_test[feature_columns]

print(f"  Test records: {len(df_test)}")
print(f"  Date range: {df_test['Date'].min().strftime('%m/%d/%Y')} to {df_test['Date'].max().strftime('%m/%d/%Y')}")

# Make predictions
print("\n[5/5] Generating predictions...")
df_test['VAS_Sold_Predicted'] = model_vas.predict(X_test)
df_test['Speed_Upgrades_Predicted'] = model_upgrades.predict(X_test)

# Round predictions to nearest integer (can't sell fractional items)
df_test['VAS_Sold_Predicted'] = df_test['VAS_Sold_Predicted'].round().astype(int)
df_test['Speed_Upgrades_Predicted'] = df_test['Speed_Upgrades_Predicted'].round().astype(int)

print("  [OK] Predictions complete")

# Aggregate daily totals
daily_predictions = df_test.groupby('Date').agg({
    'VAS_Sold_Predicted': 'sum',
    'Speed_Upgrades_Predicted': 'sum',
    'Emails_Sent': 'sum',
    'Push_Notifications_Sent': 'sum'
}).reset_index()

# Calculate cumulative sums for visualization
daily_predictions['VAS_Sold_Cumulative'] = daily_predictions['VAS_Sold_Predicted'].cumsum()
daily_predictions['Speed_Upgrades_Cumulative'] = daily_predictions['Speed_Upgrades_Predicted'].cumsum()

# Summary statistics
print("\n" + "="*80)
print("DECEMBER 2025 PREDICTIONS SUMMARY")
print("="*80)

total_vas = daily_predictions['VAS_Sold_Predicted'].sum()
total_upgrades = daily_predictions['Speed_Upgrades_Predicted'].sum()
avg_vas = daily_predictions['VAS_Sold_Predicted'].mean()
avg_upgrades = daily_predictions['Speed_Upgrades_Predicted'].mean()

print(f"\nVAS_Sold:")
print(f"  Total for December: {total_vas:,}")
print(f"  Daily Average: {avg_vas:.1f}")
print(f"  Min Daily: {daily_predictions['VAS_Sold_Predicted'].min()}")
print(f"  Max Daily: {daily_predictions['VAS_Sold_Predicted'].max()}")

print(f"\nSpeed_Upgrades:")
print(f"  Total for December: {total_upgrades:,}")
print(f"  Daily Average: {avg_upgrades:.1f}")
print(f"  Min Daily: {daily_predictions['Speed_Upgrades_Predicted'].min()}")
print(f"  Max Daily: {daily_predictions['Speed_Upgrades_Predicted'].max()}")

# Top 5 days for each metric
print("\n" + "-"*80)
print("TOP 5 DAYS BY VAS_SOLD:")
top_vas = daily_predictions.nlargest(5, 'VAS_Sold_Predicted')[['Date', 'VAS_Sold_Predicted', 'Push_Notifications_Sent']]
for idx, row in top_vas.iterrows():
    print(f"  {row['Date'].strftime('%m/%d/%Y')}: {row['VAS_Sold_Predicted']:,} VAS (Push: {row['Push_Notifications_Sent']:,})")

print("\nTOP 5 DAYS BY SPEED_UPGRADES:")
top_upgrades = daily_predictions.nlargest(5, 'Speed_Upgrades_Predicted')[['Date', 'Speed_Upgrades_Predicted', 'Emails_Sent']]
for idx, row in top_upgrades.iterrows():
    print(f"  {row['Date'].strftime('%m/%d/%Y')}: {row['Speed_Upgrades_Predicted']:,} Upgrades (Emails: {row['Emails_Sent']:,})")

# Save predictions to CSV
output_file = 'december_2025_predictions.csv'
df_test_output = df_test[['Date', 'Channel', 'VAS_Sold_Predicted', 'Speed_Upgrades_Predicted',
                          'Emails_Sent', 'Push_Notifications_Sent']].copy()
df_test_output['Date'] = df_test_output['Date'].dt.strftime('%m/%d/%Y')
df_test_output.to_csv(output_file, index=False)
print(f"\n[OK] Detailed predictions saved to: {output_file}")

# Create visualization
print("\n" + "="*80)
print("GENERATING VISUALIZATION")
print("="*80)

fig, axes = plt.subplots(2, 1, figsize=(16, 12))
fig.suptitle('December 2025 Sales Predictions - Cumulative Day-Over-Day\nHybrid Model: Random Forest (VAS) + Linear Regression (Upgrades)',
             fontsize=16, fontweight='bold', y=0.995)

# Plot 1: VAS_Sold Cumulative
ax1 = axes[0]
ax1.plot(daily_predictions['Date'], daily_predictions['VAS_Sold_Cumulative'],
         marker='o', linestyle='-', linewidth=3, markersize=8,
         color='#2E86AB', label='VAS Sold (Cumulative)', alpha=0.9)

# Fill area under the curve
ax1.fill_between(daily_predictions['Date'], 0, daily_predictions['VAS_Sold_Cumulative'],
                 alpha=0.2, color='#2E86AB')

# Highlight marketing campaign days on the cumulative line
campaign_days = daily_predictions[daily_predictions['Push_Notifications_Sent'] > 0]
ax1.scatter(campaign_days['Date'], campaign_days['VAS_Sold_Cumulative'],
           s=200, color='#F18F01', marker='*', label='Campaign Day (Push Notifications)',
           zorder=5, edgecolors='black', linewidths=1.5)

ax1.set_xlabel('Date', fontsize=12, fontweight='bold')
ax1.set_ylabel('Cumulative VAS Sold', fontsize=12, fontweight='bold')
ax1.set_title(f'VAS Sold (Cumulative) - Month Total: {total_vas:,} | Daily Avg: {avg_vas:.1f}',
             fontsize=14, fontweight='bold', pad=15)
ax1.legend(loc='upper left', fontsize=11, framealpha=0.95)
ax1.grid(True, alpha=0.3, linestyle='--', linewidth=0.8)

# Format x-axis
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=2))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Add milestone labels (every 5 days)
for i in range(0, len(daily_predictions), 5):
    row = daily_predictions.iloc[i]
    ax1.annotate(f'{int(row["VAS_Sold_Cumulative"]):,}',
                xy=(row['Date'], row['VAS_Sold_Cumulative']),
                xytext=(0, 10), textcoords='offset points',
                ha='center', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7))

# Add final total at the end
final_row = daily_predictions.iloc[-1]
ax1.annotate(f'Final: {int(final_row["VAS_Sold_Cumulative"]):,}',
            xy=(final_row['Date'], final_row['VAS_Sold_Cumulative']),
            xytext=(10, 10), textcoords='offset points',
            ha='left', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#F18F01', alpha=0.9))

# Plot 2: Speed_Upgrades Cumulative
ax2 = axes[1]
ax2.plot(daily_predictions['Date'], daily_predictions['Speed_Upgrades_Cumulative'],
         marker='s', linestyle='-', linewidth=3, markersize=8,
         color='#A23B72', label='Speed Upgrades (Cumulative)', alpha=0.9)

# Fill area under the curve
ax2.fill_between(daily_predictions['Date'], 0, daily_predictions['Speed_Upgrades_Cumulative'],
                 alpha=0.2, color='#A23B72')

# Highlight marketing campaign days on the cumulative line
campaign_days_email = daily_predictions[daily_predictions['Emails_Sent'] > 0]
ax2.scatter(campaign_days_email['Date'], campaign_days_email['Speed_Upgrades_Cumulative'],
           s=200, color='#C73E1D', marker='*', label='Campaign Day (Emails)',
           zorder=5, edgecolors='black', linewidths=1.5)

ax2.set_xlabel('Date', fontsize=12, fontweight='bold')
ax2.set_ylabel('Cumulative Speed Upgrades', fontsize=12, fontweight='bold')
ax2.set_title(f'Speed Upgrades (Cumulative) - Month Total: {total_upgrades:,} | Daily Avg: {avg_upgrades:.1f}',
             fontsize=14, fontweight='bold', pad=15)
ax2.legend(loc='upper left', fontsize=11, framealpha=0.95)
ax2.grid(True, alpha=0.3, linestyle='--', linewidth=0.8)

# Format x-axis
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
ax2.xaxis.set_major_locator(mdates.DayLocator(interval=2))
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Add milestone labels (every 5 days)
for i in range(0, len(daily_predictions), 5):
    row = daily_predictions.iloc[i]
    ax2.annotate(f'{int(row["Speed_Upgrades_Cumulative"]):,}',
                xy=(row['Date'], row['Speed_Upgrades_Cumulative']),
                xytext=(0, 10), textcoords='offset points',
                ha='center', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightpink', alpha=0.7))

# Add final total at the end
final_row = daily_predictions.iloc[-1]
ax2.annotate(f'Final: {int(final_row["Speed_Upgrades_Cumulative"]):,}',
            xy=(final_row['Date'], final_row['Speed_Upgrades_Cumulative']),
            xytext=(10, 10), textcoords='offset points',
            ha='left', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#C73E1D', alpha=0.9))

plt.tight_layout()

# Save the figure
output_chart = 'december_2025_predictions_chart.png'
plt.savefig(output_chart, dpi=300, bbox_inches='tight')
print(f"[OK] Chart saved to: {output_chart}")

plt.close()

print("\n" + "="*80)
print("PREDICTION COMPLETE!")
print("="*80)
print(f"\nFiles created:")
print(f"  1. {output_file} - Detailed predictions by date and channel")
print(f"  2. {output_chart} - Line chart visualization")
print("\n" + "="*80)
