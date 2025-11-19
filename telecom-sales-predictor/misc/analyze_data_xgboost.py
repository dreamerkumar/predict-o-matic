import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import xgboost as xgb
import os
from datetime import datetime

def get_holiday_features(date):
    """
    Determine if a date is a federal holiday or near a federal holiday.
    Returns: (is_holiday, days_to_holiday, days_from_holiday)

    Federal holidays included:
    - New Year's Day (Jan 1)
    - Martin Luther King Jr. Day (3rd Monday in January)
    - Presidents' Day (3rd Monday in February)
    - Memorial Day (last Monday in May)
    - Juneteenth (June 19)
    - Independence Day (July 4)
    - Labor Day (1st Monday in September)
    - Columbus Day (2nd Monday in October)
    - Veterans Day (Nov 11)
    - Thanksgiving (4th Thursday in November)
    - Christmas (Dec 25)
    """
    holidays_2024 = [
        pd.Timestamp('2024-01-01'),  # New Year's Day
        pd.Timestamp('2024-01-15'),  # Martin Luther King Jr. Day
        pd.Timestamp('2024-02-19'),  # Presidents' Day
        pd.Timestamp('2024-05-27'),  # Memorial Day
        pd.Timestamp('2024-06-19'),  # Juneteenth
        pd.Timestamp('2024-07-04'),  # Independence Day
        pd.Timestamp('2024-09-02'),  # Labor Day
        pd.Timestamp('2024-10-14'),  # Columbus Day
        pd.Timestamp('2024-11-11'),  # Veterans Day
        pd.Timestamp('2024-11-28'),  # Thanksgiving
        pd.Timestamp('2024-12-25'),  # Christmas
    ]

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

    all_holidays = holidays_2024 + holidays_2025

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

def main():
    """
    Analyze telecom data from CSV file and build XGBoost regression models
    """
    print("Loading data from CSV file...")
    print("="*60)

    # Load data from CSV
    try:
        df = pd.read_csv('final_dataset.csv')
        print(f"Successfully loaded {len(df)} records from final_dataset.csv")
    except FileNotFoundError:
        print("Error: final_dataset.csv not found!")
        return
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # Display basic information
    print("\n" + "="*60)
    print("DATA OVERVIEW")
    print("="*60)
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nData types:\n{df.dtypes}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    print(f"\nBasic statistics:\n{df.describe()}")

    # Prepare data for modeling
    print("\n" + "="*60)
    print("PREPARING DATA FOR XGBOOST REGRESSION")
    print("="*60)

    # Convert Date to datetime and extract features
    df['Date'] = pd.to_datetime(df['Date'])
    df['Day_of_Year'] = df['Date'].dt.dayofyear
    df['Day_of_Week'] = df['Date'].dt.dayofweek
    df['Month'] = df['Date'].dt.month

    # Add holiday features
    print("\nAdding holiday features...")
    holiday_features = df['Date'].apply(get_holiday_features)
    df['Is_Holiday'] = holiday_features.apply(lambda x: x[0])
    df['Days_To_Holiday'] = holiday_features.apply(lambda x: x[1])
    df['Days_From_Holiday'] = holiday_features.apply(lambda x: x[2])

    # Create a "near holiday" indicator (within 1 day before or after)
    df['Near_Holiday'] = ((df['Days_To_Holiday'] <= 1) | (df['Days_From_Holiday'] <= 1)).astype(int)

    print(f"  Found {df['Is_Holiday'].sum()} holiday dates in dataset")
    print(f"  Found {df['Near_Holiday'].sum()} dates near holidays (within 1 day)")

    # Encode Channel (App=0, Web=1)
    le = LabelEncoder()
    df['Channel_Encoded'] = le.fit_transform(df['Channel'])

    # Define features and targets
    feature_columns = ['Day_of_Year', 'Day_of_Week', 'Month', 'Channel_Encoded',
                       'Emails_Sent', 'Push_Notifications_Sent',
                       'Is_Holiday', 'Days_To_Holiday', 'Days_From_Holiday', 'Near_Holiday']
    target_columns = ['VAS_Sold', 'Speed_Upgrades']

    X = df[feature_columns]

    print(f"\nFeatures used: {feature_columns}")
    print(f"Targets to predict: {target_columns}")

    # Date-based train-test split
    # Training: Sep 2024 to July 2025
    # Testing: Last 3 months (Aug 2025 to Oct 2025)
    split_date = pd.Timestamp('2025-08-01')

    train_mask = df['Date'] < split_date
    test_mask = df['Date'] >= split_date

    X_train = X[train_mask]
    X_test = X[test_mask]

    print(f"\nDate-based split:")
    print(f"  Training set: {df[train_mask]['Date'].min()} to {df[train_mask]['Date'].max()}")
    print(f"  Training records: {len(X_train)}")
    print(f"  Test set: {df[test_mask]['Date'].min()} to {df[test_mask]['Date'].max()}")
    print(f"  Test records: {len(X_test)}")

    # Build models for each target
    models = {}
    results = {}

    for target in target_columns:
        print("\n" + "="*60)
        print(f"BUILDING XGBOOST MODEL FOR: {target}")
        print("="*60)

        y = df[target]
        y_train = y[train_mask]
        y_test = y[test_mask]

        # Create and train the XGBoost model
        model = xgb.XGBRegressor(
            n_estimators=200,          # Number of boosting rounds
            learning_rate=0.05,        # Step size shrinkage
            max_depth=6,               # Maximum tree depth
            min_child_weight=3,        # Minimum sum of instance weight needed in a child
            subsample=0.8,             # Subsample ratio of training instances
            colsample_bytree=0.8,      # Subsample ratio of columns when constructing each tree
            random_state=42,           # For reproducibility
            n_jobs=-1                  # Use all CPU cores
        )
        model.fit(X_train, y_train, verbose=False)

        # Make predictions
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        # Calculate metrics
        train_r2 = r2_score(y_train, y_pred_train)
        test_r2 = r2_score(y_test, y_pred_test)
        train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
        test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
        train_mae = mean_absolute_error(y_train, y_pred_train)
        test_mae = mean_absolute_error(y_test, y_pred_test)

        # Store model and results
        models[target] = model
        results[target] = {
            'train_r2': train_r2,
            'test_r2': test_r2,
            'train_rmse': train_rmse,
            'test_rmse': test_rmse,
            'train_mae': train_mae,
            'test_mae': test_mae
        }

        # Display results
        print(f"\nModel Performance for {target}:")
        print(f"  Training Set:")
        print(f"    R² Score: {train_r2:.4f}")
        print(f"    RMSE: {train_rmse:.4f}")
        print(f"    MAE: {train_mae:.4f}")
        print(f"\n  Test Set:")
        print(f"    R² Score: {test_r2:.4f}")
        print(f"    RMSE: {test_rmse:.4f}")
        print(f"    MAE: {test_mae:.4f}")

        # Display feature importance
        print(f"\n  Feature Importance (sorted by importance):")
        feature_importance = model.feature_importances_
        importance_df = pd.DataFrame({
            'feature': feature_columns,
            'importance': feature_importance
        }).sort_values('importance', ascending=False)

        for idx, row in importance_df.iterrows():
            print(f"    {row['feature']}: {row['importance']:.4f}")

    print("\n" + "="*60)
    print("MODEL TRAINING COMPLETE")
    print("="*60)

    # Create visualizations for test set predictions
    print("\n" + "="*60)
    print("GENERATING VISUALIZATIONS")
    print("="*60)

    # Prepare test set data with predictions
    test_df = df[test_mask].copy()
    test_df = test_df.sort_values('Date')

    # Create a figure with 2 subplots (one for each target)
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle('XGBoost: Actual vs Predicted Values on Test Set (Aug-Oct 2025)',
                 fontsize=16, fontweight='bold')

    for idx, target in enumerate(target_columns):
        ax = axes[idx]
        model = models[target]

        # Get predictions for test set
        y_pred = model.predict(X_test)
        y_actual = y_test.values

        # Calculate prediction intervals (95% confidence)
        # Using residual standard error approach
        residuals = y_actual - y_pred
        residual_std = np.std(residuals)
        confidence_interval = 1.96 * residual_std  # 95% CI

        upper_bound = y_pred + confidence_interval
        lower_bound = y_pred - confidence_interval

        # Add predictions to test dataframe
        test_df[f'{target}_Predicted'] = y_pred
        test_df[f'{target}_Upper'] = upper_bound
        test_df[f'{target}_Lower'] = lower_bound

        # Aggregate by date for cleaner visualization
        daily_data = test_df.groupby('Date').agg({
            target: 'sum',
            f'{target}_Predicted': 'sum',
            f'{target}_Upper': 'sum',
            f'{target}_Lower': 'sum'
        }).reset_index()

        # Plot actual values
        ax.plot(daily_data['Date'], daily_data[target],
                marker='o', linestyle='-', linewidth=2, markersize=6,
                label='Actual', color='#2E86AB', alpha=0.8)

        # Plot predicted values
        ax.plot(daily_data['Date'], daily_data[f'{target}_Predicted'],
                marker='s', linestyle='--', linewidth=2, markersize=6,
                label='Predicted', color='#A23B72', alpha=0.8)

        # Plot confidence interval
        ax.fill_between(daily_data['Date'],
                        daily_data[f'{target}_Lower'],
                        daily_data[f'{target}_Upper'],
                        alpha=0.2, color='#A23B72', label='95% Confidence Interval')

        # Formatting
        ax.set_xlabel('Date', fontsize=11, fontweight='bold')
        ax.set_ylabel(target, fontsize=11, fontweight='bold')
        ax.set_title(f'{target} - XGBoost Test Set Performance (R² = {results[target]["test_r2"]:.4f})',
                    fontsize=13, fontweight='bold', pad=10)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--')

        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

    plt.tight_layout()

    # Save the figure
    os.makedirs('../output_files', exist_ok=True)
    timestamp = datetime.utcnow().isoformat(timespec='milliseconds').replace(':', '-').replace('.', '-') + 'Z'
    output_file = f'../output_files/model_predictions_xgboost_test_set_{timestamp}.png'
    plt.savefig(output_file, dpi=100, bbox_inches='tight')
    print(f"\nVisualization saved to: {output_file}")

    # Close the plot to free memory
    plt.close()

    print("\n" + "="*60)
    print("VISUALIZATION COMPLETE")
    print("="*60)

    return df, models, results, test_df

if __name__ == "__main__":
    df, models, results, test_df = main()
    print("\nXGBoost models are ready for predictions!")
    print("="*60)
