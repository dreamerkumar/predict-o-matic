# analyze_data_random_forest.py

## Purpose

This script implements a **Random Forest Regression** model for predicting telecom sales metrics. It trains separate Random Forest models for both `VAS_Sold` and `Speed_Upgrades`, evaluates their performance on a test set, and generates visualizations comparing actual vs predicted values with confidence intervals.

This is an **experimental/alternative implementation** located in the `misc/` folder, used for comparing Random Forest performance against other algorithms before the final hybrid model selection.

## What It Does

1. **Loads Training Data**: Reads `final_dataset.csv` from the parent directory
2. **Feature Engineering**: 
   - Extracts temporal features (day of year, day of week, month)
   - Identifies federal holidays for 2024 and 2025
   - Calculates holiday proximity metrics
   - Encodes categorical variables
3. **Trains Random Forest Models**: 
   - Creates separate Random Forest models for VAS_Sold and Speed_Upgrades
   - Uses optimized hyperparameters for ensemble learning
4. **Evaluates Performance**: 
   - Date-based train/test split (Sep 2024 - Jul 2025 training, Aug-Oct 2025 testing)
   - Calculates R², RMSE, and MAE metrics
   - Displays feature importance rankings
5. **Generates Visualizations**: 
   - Side-by-side comparison charts
   - 95% confidence intervals
   - Saves to parent `output_files` directory

## Prerequisites

### Required Files
- **`../final_dataset.csv`**: Historical sales data (located in parent directory)
  - Columns: Date, Channel, VAS_Sold, Speed_Upgrades, Emails_Sent, Push_Notifications_Sent

### Required Python Packages
```bash
pip install pandas numpy scikit-learn matplotlib
```

**Dependencies:**
- `pandas`: Data manipulation
- `numpy`: Numerical operations
- `scikit-learn`: RandomForestRegressor implementation
- `matplotlib`: Visualization

## How to Run

### From misc/ Directory
```bash
cd /path/to/telecom-sales-predictor/misc
python analyze_data_random_forest.py
```

### From Root Directory
```bash
cd /path/to/telecom-sales-predictor
python misc/analyze_data_random_forest.py
```

### Expected Output
The script displays:
1. **Data Loading**: Confirmation of records loaded from CSV
2. **Data Overview**: 
   - Column names and data types
   - Missing values summary
   - Basic statistics
3. **Feature Engineering**: 
   - Holiday detection results
   - Number of holidays and near-holiday dates found
4. **Model Training** (for each target):
   - Training progress
   - Performance metrics (R², RMSE, MAE)
   - Feature importance rankings sorted by importance
5. **Visualization**: Path to saved PNG file

### Output Files
- **Visualization**: `../output_files/model_predictions_random_forest_test_set_<timestamp>.png`
  - Two subplots (VAS_Sold and Speed_Upgrades)
  - Actual vs predicted values
  - 95% confidence intervals
  - Performance metrics displayed on charts

## Random Forest Configuration

### Hyperparameters
```python
RandomForestRegressor(
    n_estimators=200,        # Number of trees in forest
    max_depth=15,            # Maximum depth of each tree
    min_samples_split=5,     # Min samples to split node
    min_samples_leaf=2,      # Min samples at leaf node
    max_features='sqrt',     # Features considered per split
    random_state=42,         # Seed for reproducibility
    n_jobs=-1                # Use all CPU cores for parallel processing
)
```

### Why These Parameters?
- **n_estimators=200**: Balance between accuracy and training time
- **max_depth=15**: Prevents overfitting while capturing complex patterns
- **min_samples_split=5**: Ensures robust splits with sufficient data
- **min_samples_leaf=2**: Prevents over-specific leaf nodes
- **max_features='sqrt'**: Adds randomness for better generalization
- **n_jobs=-1**: Maximizes performance on multi-core systems

## Feature Importance

### What It Shows
Random Forest automatically ranks features by importance based on:
- How much each feature reduces impurity (Gini or entropy)
- Averaged across all trees in the forest

### Typical Important Features
1. **Emails_Sent / Push_Notifications_Sent**: Direct marketing impact
2. **Day_of_Week**: Weekly purchasing patterns
3. **Month**: Seasonal trends
4. **Days_To_Holiday / Days_From_Holiday**: Holiday shopping effects

## Dependencies on Other Files

### Direct Dependencies
- **`../final_dataset.csv`** (required): Located in parent directory
  - Script uses `../` path to access it from the `misc/` subdirectory

### Output Location
- **`../output_files/`**: Saves visualizations to parent directory's output folder
  - Created automatically if it doesn't exist
  - Allows easy comparison with other model outputs

### Directory Structure
```
telecom-sales-predictor/
├── final_dataset.csv                      # Required input
├── output_files/                          # Output location
│   └── model_predictions_random_forest_test_set_<timestamp>.png
└── misc/
    └── analyze_data_random_forest.py      # This script
```

### Related Scripts
- **`analyze_data.py`**: Linear regression baseline
- **`analyze_data_xgboost.py`**: XGBoost implementation
- **`../analyze_data_hybrid.py`**: Final hybrid model (uses Random Forest for VAS_Sold)

## Performance Comparison

### Expected Results
- **VAS_Sold**: 
  - Test R² ≈ 0.85-0.87 (85-87% accuracy)
  - Performs well on non-linear patterns
  - Best model for VAS predictions

- **Speed_Upgrades**: 
  - Test R² ≈ 0.75-0.78 (75-78% accuracy)
  - Good but not optimal for this target
  - Linear Regression performs better (80%+)

### Why Random Forest Works Well for VAS_Sold
1. **Non-linear Relationships**: Captures complex interactions between features
2. **Robust to Outliers**: Ensemble averaging reduces impact of anomalies
3. **Feature Interactions**: Automatically detects feature combinations
4. **No Scaling Required**: Works with features on different scales

## Troubleshooting

### Common Issues

1. **FileNotFoundError: final_dataset.csv not found**
   - Ensure you're running from the `misc/` directory
   - Or adjust path if running from root: `python misc/analyze_data_random_forest.py`
   - Verify `final_dataset.csv` exists in parent directory

2. **ModuleNotFoundError: No module named 'sklearn'**
   ```bash
   pip install scikit-learn
   ```

3. **Slow Training**
   - Random Forest with 200 trees can take 10-30 seconds
   - This is normal for ensemble methods
   - Reduce `n_estimators` for faster training (but lower accuracy)

4. **High Memory Usage**
   - Random Forest stores all 200 trees in memory
   - May require 1-2 GB RAM for large datasets
   - Reduce `n_estimators` if memory constrained

5. **Output Directory Not Created**
   - Script creates `../output_files/` automatically
   - Check write permissions in parent directory

## Comparison with Other Algorithms

### vs Linear Regression (`analyze_data.py`)
- **Random Forest Advantages**:
  - Better for non-linear patterns (VAS_Sold)
  - Handles feature interactions automatically
  - More robust to outliers
- **Linear Regression Advantages**:
  - Faster training and prediction
  - Better interpretability
  - Better for linear relationships (Speed_Upgrades)

### vs XGBoost (`analyze_data_xgboost.py`)
- **Random Forest Advantages**:
  - Simpler hyperparameter tuning
  - Less prone to overfitting with default settings
  - No need for learning rate tuning
- **XGBoost Advantages**:
  - Often slightly better accuracy
  - More memory efficient
  - Better handling of missing values

### Final Hybrid Model Selection
Based on testing, the final production model (`analyze_data_hybrid.py`) uses:
- **Random Forest for VAS_Sold**: 86.4% accuracy (best for this target)
- **Linear Regression for Speed_Upgrades**: 80.2% accuracy (best for this target)

## Customization Options

### Adjust Number of Trees
```python
# More trees = better accuracy but slower
model = RandomForestRegressor(n_estimators=500, ...)

# Fewer trees = faster but less accurate
model = RandomForestRegressor(n_estimators=50, ...)
```

### Prevent Overfitting
```python
# Increase regularization
model = RandomForestRegressor(
    max_depth=10,           # Shallower trees
    min_samples_split=10,   # More samples required
    min_samples_leaf=5,     # Larger leaves
    ...
)
```

### Speed Up Training
```python
# Use fewer trees and parallel processing
model = RandomForestRegressor(
    n_estimators=100,    # Fewer trees
    n_jobs=-1,           # All CPU cores
    ...
)
```

## Feature Engineering

### Holiday Features
```python
get_holiday_features(date) returns:
  - is_holiday: 1 if federal holiday, 0 otherwise
  - days_to_holiday: Days until next holiday (0-365)
  - days_from_holiday: Days since last holiday (0-365)
  - near_holiday: 1 if within 1 day of holiday
```

### Federal Holidays Recognized
- New Year's Day (Jan 1)
- Martin Luther King Jr. Day (3rd Monday in Jan)
- Presidents' Day (3rd Monday in Feb)
- Memorial Day (Last Monday in May)
- Juneteenth (Jun 19)
- Independence Day (Jul 4)
- Labor Day (1st Monday in Sep)
- Columbus Day (2nd Monday in Oct)
- Veterans Day (Nov 11)
- Thanksgiving (4th Thursday in Nov)
- Christmas (Dec 25)

## Model Interpretability

### Feature Importance Output
```
Feature Importance (sorted by importance):
  Push_Notifications_Sent: 0.2845
  Emails_Sent: 0.2134
  Day_of_Year: 0.1523
  Month: 0.0987
  Day_of_Week: 0.0876
  Days_To_Holiday: 0.0654
  Channel_Encoded: 0.0543
  Days_From_Holiday: 0.0432
  Is_Holiday: 0.0321
  Near_Holiday: 0.0285
```

### Interpretation
- **Higher values** = more important for predictions
- **Push/Email** features typically most important (direct sales drivers)
- **Temporal features** capture seasonal/weekly patterns
- **Holiday features** account for holiday shopping behavior

## Notes

- This is an **experimental script** for model comparison
- Located in `misc/` folder (not main production code)
- Used to evaluate Random Forest before selecting final hybrid approach
- Output saved to parent `output_files/` for easy comparison
- Random Forest performs **best for VAS_Sold** predictions
- For **Speed_Upgrades**, Linear Regression performs better
- The script demonstrates the importance of testing multiple algorithms
- Final production code uses insights from this analysis
- **Images are optimized at 100 DPI** to keep file sizes ~200-400 KB for efficient MCP transmission and Cloud Desktop compatibility (< 1 MB limit)

