# analyze_data_hybrid.py

## Purpose

This script implements a **Hybrid Machine Learning Model** for predicting telecom sales data. It uses a "best-of-breed" approach by combining two different machine learning algorithms:
- **Random Forest Regressor** for predicting `VAS_Sold` (Value-Added Services sales) with 86.4% accuracy
- **Linear Regression** for predicting `Speed_Upgrades` with 80.2% accuracy

The script analyzes historical telecom sales data, trains separate optimized models for each target metric, evaluates their performance, and generates comprehensive visualizations with confidence intervals.

## What It Does

1. **Loads Training Data**: Reads the `final_dataset.csv` file containing historical sales and marketing data
2. **Feature Engineering**: 
   - Extracts temporal features (day of year, day of week, month)
   - Identifies federal holidays for 2024 and 2025
   - Calculates proximity to holidays (days before/after)
   - Encodes categorical variables (App/Web channels)
3. **Hybrid Model Training**:
   - Trains a Random Forest model specifically for VAS_Sold predictions
   - Trains a Linear Regression model specifically for Speed_Upgrades predictions
4. **Model Evaluation**: 
   - Uses date-based train/test split (training: Sep 2024 - Jul 2025, testing: Aug-Oct 2025)
   - Calculates R² score, RMSE, and MAE metrics
   - Displays feature importance/coefficients
5. **Visualization**: 
   - Creates side-by-side comparison charts showing actual vs predicted values
   - Includes 95% confidence intervals for predictions
   - Saves optimized charts (~200-400 KB) to the `output_files` directory with timestamps

## Prerequisites

### Required Files
- **`final_dataset.csv`**: Historical sales data with columns:
  - `Date`: Date of the record
  - `Channel`: Distribution channel (App or Web)
  - `VAS_Sold`: Number of value-added services sold
  - `Speed_Upgrades`: Number of speed upgrades sold
  - `Emails_Sent`: Marketing emails sent that day
  - `Push_Notifications_Sent`: Push notifications sent that day

### Required Python Packages
```bash
pip install pandas numpy scikit-learn matplotlib
```

**Dependencies:**
- `pandas`: Data manipulation and CSV processing
- `numpy`: Numerical computations
- `scikit-learn`: Machine learning algorithms (RandomForestRegressor, LinearRegression)
- `matplotlib`: Visualization and chart generation

## How to Run

### Basic Execution
```bash
cd /path/to/telecom-sales-predictor
python analyze_data_hybrid.py
```

### Expected Output
The script will display:
1. Data loading confirmation with record count
2. Data overview (columns, data types, missing values, statistics)
3. Holiday feature engineering summary
4. Model training progress for each target
5. Performance metrics (R², RMSE, MAE) for training and test sets
6. Feature importance rankings
7. Path to generated visualization file

### Output Files
- **Visualization**: `output_files/model_predictions_hybrid_final_<timestamp>.png`
  - Two subplots showing VAS_Sold and Speed_Upgrades predictions
  - Actual vs predicted values with 95% confidence intervals
  - Test set performance metrics displayed on charts

## Key Features

### Holiday Detection
The script includes a comprehensive `get_holiday_features()` function that identifies:
- 11 federal holidays for 2024 and 2025
- Distance to nearest holiday (days before/after)
- "Near holiday" flag for dates within 1 day of a holiday

### Model Selection Strategy
- **VAS_Sold**: Uses Random Forest (best R² = 0.864) due to non-linear patterns in value-added service sales
- **Speed_Upgrades**: Uses Linear Regression (best R² = 0.802) as it captures linear relationships effectively

### Feature Set
```python
features = [
    'Day_of_Year',              # Seasonal patterns
    'Day_of_Week',              # Weekly cycles
    'Month',                    # Monthly trends
    'Channel_Encoded',          # App vs Web (0/1)
    'Emails_Sent',              # Marketing activity
    'Push_Notifications_Sent',  # Marketing activity
    'Is_Holiday',               # Holiday flag
    'Days_To_Holiday',          # Days until next holiday
    'Days_From_Holiday',        # Days since last holiday
    'Near_Holiday'              # Within 1 day of holiday
]
```

## Dependencies on Other Files

### Direct Dependencies
- **`final_dataset.csv`** (required): Must exist in the same directory

### Directory Structure Requirements
```
telecom-sales-predictor/
├── analyze_data_hybrid.py       # This script
├── final_dataset.csv            # Required input data
└── output_files/                # Created automatically if missing
    └── model_predictions_hybrid_final_<timestamp>.png
```

### No Dependencies On
- Does not depend on `test_dataset_dec_2025.csv`
- Does not require database connections
- Independent of other Python scripts in the project

## Performance Metrics

### Expected Results (Based on Test Set Aug-Oct 2025)
- **VAS_Sold Model (Random Forest)**:
  - Test R² Score: 0.8640 (86.4% accuracy)
  - Typical RMSE: ~2-3 units
  - Typical MAE: ~1-2 units

- **Speed_Upgrades Model (Linear Regression)**:
  - Test R² Score: 0.8020 (80.2% accuracy)
  - Typical RMSE: ~3-4 units
  - Typical MAE: ~2-3 units

- **Overall Average R²**: 0.833 (83.3% accuracy)

## Troubleshooting

### Common Issues

1. **FileNotFoundError: final_dataset.csv not found**
   - Ensure `final_dataset.csv` exists in the same directory
   - Check file name spelling and case sensitivity

2. **ModuleNotFoundError: No module named 'sklearn'**
   ```bash
   pip install scikit-learn
   ```

3. **Low Memory Warning**
   - The script processes data efficiently but may require 500MB+ RAM for large datasets
   - Close other applications if memory issues occur

4. **Visualization Not Saving**
   - Check write permissions in the `output_files` directory
   - Ensure sufficient disk space (charts are ~200-400 KB each)

## Model Configuration

### Random Forest Hyperparameters
```python
RandomForestRegressor(
    n_estimators=200,        # 200 decision trees
    max_depth=15,            # Maximum tree depth
    min_samples_split=5,     # Min samples to split node
    min_samples_leaf=2,      # Min samples at leaf
    max_features='sqrt',     # Features per split
    random_state=42,         # Reproducibility
    n_jobs=-1                # Use all CPU cores
)
```

### Linear Regression Configuration
```python
LinearRegression()  # Default parameters, no regularization
```

## Notes

- The script uses **date-based splitting** (not random) to simulate real-world time-series prediction
- Training uses 11 months of data, testing uses the last 3 months
- Confidence intervals are calculated using residual standard error (±1.96 * std)
- All visualizations include timestamp in filename for version tracking
- The hybrid approach yields better overall accuracy than using a single algorithm for both targets
- **Images are optimized at 100 DPI** (down from 300 DPI) to keep file sizes ~200-400 KB for efficient MCP transmission and Cloud Desktop compatibility (< 1 MB limit)

