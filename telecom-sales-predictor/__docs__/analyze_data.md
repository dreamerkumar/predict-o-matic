# analyze_data.py

## Purpose

This script implements a **Linear Regression** baseline model for predicting telecom sales metrics. It serves as the simplest machine learning approach, training separate linear regression models for both `VAS_Sold` and `Speed_Upgrades` targets. This baseline is useful for comparison against more complex algorithms (Random Forest, XGBoost) to determine if added complexity provides meaningful accuracy improvements.

This is an **experimental/baseline implementation** located in the `misc/` folder, used for establishing performance benchmarks before evaluating more sophisticated models.

## What It Does

1. **Loads Training Data**: Reads `final_dataset.csv` from parent directory
2. **Feature Engineering**: 
   - Extracts temporal features (day of year, week, month)
   - Identifies federal holidays for 2024-2025
   - Calculates holiday proximity metrics
   - Encodes categorical variables (Channel)
3. **Trains Linear Models**: 
   - Creates separate LinearRegression models for each target
   - Fits linear relationships between features and targets
   - No hyperparameters to tune (uses defaults)
4. **Evaluates Performance**: 
   - Date-based train/test split
   - Calculates R², RMSE, and MAE metrics
   - Displays coefficient values for interpretability
5. **Generates Visualizations**: 
   - Actual vs predicted comparison charts
   - 95% confidence intervals based on residual standard error
   - Saves to parent output directory

## Prerequisites

### Required Files
- **`../final_dataset.csv`**: Historical sales data in parent directory
  - Required columns: Date, Channel, VAS_Sold, Speed_Upgrades, Emails_Sent, Push_Notifications_Sent

### Required Python Packages
```bash
pip install pandas numpy scikit-learn matplotlib
```

**Dependencies:**
- `pandas`: Data manipulation and CSV processing
- `numpy`: Numerical operations
- `scikit-learn`: LinearRegression model and metrics
- `matplotlib`: Visualization

## How to Run

### From misc/ Directory
```bash
cd /path/to/telecom-sales-predictor/misc
python analyze_data.py
```

### From Root Directory
```bash
cd /path/to/telecom-sales-predictor
python misc/analyze_data.py
```

### Expected Output
1. **Data Loading**: Shows number of records loaded
2. **Data Overview**: 
   - Column names and data types
   - Missing values check
   - Basic statistics (mean, std, min, max)
3. **Feature Engineering**: 
   - Holiday feature confirmation
   - Count of holidays and near-holiday dates
4. **Model Training** (for each target):
   - Training completion
   - Performance metrics (R², RMSE, MAE)
   - Feature coefficients with intercept
5. **Visualization**: Path to saved chart

### Output Files
- **Visualization**: `../output_files/model_predictions_test_set_<timestamp>.png`
  - Two subplots (VAS_Sold and Speed_Upgrades)
  - Actual vs predicted values on test set
  - 95% confidence intervals
  - Performance metrics displayed

## Linear Regression Overview

### Algorithm
Linear Regression models the relationship between features and target as:
```
y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ
```

Where:
- `y` = predicted target (VAS_Sold or Speed_Upgrades)
- `β₀` = intercept (baseline value)
- `βᵢ` = coefficient for feature i
- `xᵢ` = feature value i

### Advantages
1. **Fast Training**: Closed-form solution (no iterations needed)
2. **Fast Prediction**: Simple arithmetic operations
3. **Interpretable**: Coefficients show feature impact directly
4. **No Hyperparameters**: No tuning required
5. **Low Memory**: Small model size

### Limitations
1. **Assumes Linearity**: Cannot capture non-linear relationships
2. **No Feature Interactions**: Doesn't automatically learn interactions
3. **Sensitive to Outliers**: Extreme values can skew the model
4. **Multicollinearity**: Correlated features can affect stability

## Model Configuration

### Parameters
```python
LinearRegression()  # Uses default parameters
```

**Default Settings:**
- `fit_intercept=True`: Calculates intercept term
- `normalize=False`: No feature normalization (deprecated)
- `copy_X=True`: Copies feature matrix
- `n_jobs=None`: Single-threaded (fast enough for small data)

### No Hyperparameters
Unlike Random Forest or XGBoost, Linear Regression has no hyperparameters to tune, making it:
- Easy to use (no tuning needed)
- Consistent across runs
- Fast to train

## Feature Coefficients

### Interpretation
The model displays coefficients for all features:

```
Feature Coefficients:
  Day_of_Year: 0.0234        # +2.34 per day increase in year
  Day_of_Week: -1.2345       # -1.23 on each day of week
  Month: 3.4567              # +3.46 per month
  Channel_Encoded: 8.9012    # +8.90 for Web vs App
  Emails_Sent: 0.000123      # +0.000123 per email
  Push_Notifications_Sent: 0.000456  # +0.000456 per push
  Is_Holiday: -5.6789        # -5.68 on holidays
  Days_To_Holiday: 0.0987    # +0.10 per day to holiday
  Days_From_Holiday: -0.0654 # -0.07 per day from holiday
  Near_Holiday: 2.3456       # +2.35 near holidays
Intercept: 45.6789           # Baseline value
```

### Coefficient Meaning
- **Positive coefficient**: Feature increase leads to target increase
- **Negative coefficient**: Feature increase leads to target decrease
- **Large absolute value**: Feature has strong impact
- **Near zero**: Feature has weak impact

## Performance Comparison

### Expected Results

**VAS_Sold (Value-Added Services):**
- Test R² ≈ 0.73-0.76 (73-76% accuracy)
- Performance: Good but not optimal
- Limitation: VAS sales have non-linear patterns

**Speed_Upgrades:**
- Test R² ≈ 0.78-0.82 (78-82% accuracy)
- Performance: Excellent (best algorithm for this target!)
- Reason: Speed upgrades follow linear patterns

### Comparison with Other Algorithms

| Algorithm | VAS_Sold R² | Speed_Upgrades R² | Training Time |
|-----------|-------------|-------------------|---------------|
| Linear Regression | 0.73-0.76 | **0.80** ✓ | < 1 second |
| Random Forest | **0.86** ✓ | 0.75-0.78 | 10-30 seconds |
| XGBoost | 0.83-0.85 | 0.78-0.80 | 15-45 seconds |

**Key Insights:**
- Linear Regression **wins for Speed_Upgrades** (selected for final hybrid model)
- Random Forest wins for VAS_Sold (non-linear patterns)
- Linear Regression is **fastest** by far

## Dependencies on Other Files

### Direct Dependencies
- **`../final_dataset.csv`** (required): Training data in parent directory
  - Script uses `../` relative path from `misc/` folder

### Output Location
- **`../output_files/`**: Saves visualizations to parent directory
  - Created automatically if doesn't exist
  - Enables comparison with other model outputs

### Directory Structure
```
telecom-sales-predictor/
├── final_dataset.csv                        # Required input
├── output_files/                            # Output location
│   └── model_predictions_test_set_<timestamp>.png
└── misc/
    └── analyze_data.py                      # This script
```

### Related Scripts
- **`analyze_data_random_forest.py`**: Random Forest comparison
- **`analyze_data_xgboost.py`**: XGBoost comparison
- **`../analyze_data_hybrid.py`**: Final production model (uses Linear Regression for Speed_Upgrades)

## Troubleshooting

### Common Issues

1. **FileNotFoundError: final_dataset.csv not found**
   - Ensure running from `misc/` directory
   - Or run with: `python misc/analyze_data.py` from root
   - Verify CSV exists in parent directory

2. **ModuleNotFoundError: No module named 'sklearn'**
   ```bash
   pip install scikit-learn
   ```

3. **Poor Performance (Low R²)**
   - Linear Regression assumes linear relationships
   - Some targets (like VAS_Sold) may have non-linear patterns
   - Consider Random Forest or XGBoost for better accuracy
   - This is expected behavior for baseline model

4. **Output Directory Error**
   - Script creates `../output_files/` automatically
   - Check write permissions in parent directory

5. **Visualization Issues**
   - Ensure matplotlib backend supports file saving
   - Check disk space for PNG output

## When to Use Linear Regression

### Use Linear Regression When:
1. **Speed is Critical**: Fastest training and prediction
2. **Interpretability Needed**: Coefficients are easy to explain to stakeholders
3. **Data is Linear**: Relationships are approximately linear
4. **Simple Baseline**: Need quick performance benchmark
5. **Production Constraints**: Limited memory or compute resources

### Consider Other Algorithms When:
1. **Non-linear Patterns**: Data shows curves or complex interactions
2. **High Accuracy Required**: Need every percentage point of improvement
3. **Feature Interactions**: Important interactions between features
4. **Sufficient Resources**: Have time and compute for complex models

## Customization Options

### Add Regularization (Ridge/Lasso)
To prevent overfitting with many features:
```python
from sklearn.linear_model import Ridge, Lasso

# Ridge Regression (L2 regularization)
model = Ridge(alpha=1.0)

# Lasso Regression (L1 regularization, feature selection)
model = Lasso(alpha=1.0)
```

### Polynomial Features
To capture non-linear relationships:
```python
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)
model.fit(X_poly, y)
```

### Feature Scaling
Normalize features for better coefficient comparison:
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
model.fit(X_scaled, y)
```

## Model Evaluation Metrics

### R² Score (Coefficient of Determination)
- **Range**: -∞ to 1.0
- **1.0**: Perfect predictions
- **0.0**: As good as predicting mean
- **Negative**: Worse than predicting mean
- **Interpretation**: Percentage of variance explained

### RMSE (Root Mean Squared Error)
- Same units as target
- Penalizes large errors heavily
- Lower is better
- Sensitive to outliers

### MAE (Mean Absolute Error)
- Average absolute difference
- Same units as target
- More robust to outliers than RMSE
- Lower is better

## Why Linear Regression Selected for Speed_Upgrades

Despite being the simplest algorithm, Linear Regression was selected for the final hybrid model's Speed_Upgrades predictions because:

1. **Best Accuracy**: 80% R² (better than Random Forest's 75%)
2. **Fastest**: < 1 second training vs 10-30 seconds for Random Forest
3. **Simplest**: No hyperparameters to tune
4. **Interpretable**: Easy to explain coefficient impacts
5. **Reliable**: Consistent performance across runs

This demonstrates that **simpler is sometimes better** when:
- Data relationships are approximately linear
- Speed and interpretability matter
- Complex models don't add value

## Notes

- This is a **baseline/comparison script** in `misc/` folder
- Not production code but informed final model selection
- Linear Regression **selected for Speed_Upgrades** in production
- Fastest algorithm tested (< 1 second training)
- Best interpretability (clear coefficient values)
- Limited by assumption of linear relationships
- Cannot capture complex feature interactions
- Excellent baseline for evaluating more complex models
- Proves that simpler models can outperform complex ones for certain targets
- **Images are optimized at 100 DPI** to keep file sizes ~200-400 KB for efficient MCP transmission and Cloud Desktop compatibility (< 1 MB limit)

