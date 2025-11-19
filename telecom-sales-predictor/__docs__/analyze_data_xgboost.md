# analyze_data_xgboost.py

## Purpose

This script implements an **XGBoost (Extreme Gradient Boosting)** regression model for predicting telecom sales metrics. It trains separate XGBoost models for both `VAS_Sold` and `Speed_Upgrades`, evaluates their performance, and generates visualizations with confidence intervals.

This is an **experimental/alternative implementation** located in the `misc/` folder, used for comparing XGBoost performance against Random Forest and Linear Regression before selecting the final hybrid model approach.

## What It Does

1. **Loads Training Data**: Reads `final_dataset.csv` from the parent directory
2. **Feature Engineering**: 
   - Extracts temporal features
   - Identifies federal holidays
   - Calculates holiday proximity
   - Encodes categorical variables
3. **Trains XGBoost Models**: 
   - Creates gradient boosting models for both targets
   - Uses optimized hyperparameters
   - Leverages boosting for sequential error correction
4. **Evaluates Performance**: 
   - Date-based train/test split
   - Calculates R², RMSE, and MAE
   - Displays feature importance scores
5. **Generates Visualizations**: 
   - Actual vs predicted comparisons
   - 95% confidence intervals
   - Optimized output charts (~200-400 KB for efficient transmission)

## Prerequisites

### Required Files
- **`../final_dataset.csv`**: Historical sales data in parent directory
  - Must contain: Date, Channel, VAS_Sold, Speed_Upgrades, Emails_Sent, Push_Notifications_Sent

### Required Python Packages
```bash
pip install pandas numpy scikit-learn xgboost matplotlib
```

**Dependencies:**
- `pandas`: Data manipulation
- `numpy`: Numerical operations
- `scikit-learn`: Evaluation metrics
- `xgboost`: XGBoost algorithm implementation
- `matplotlib`: Visualization

## How to Run

### From misc/ Directory
```bash
cd /path/to/telecom-sales-predictor/misc
python analyze_data_xgboost.py
```

### From Root Directory
```bash
cd /path/to/telecom-sales-predictor
python misc/analyze_data_xgboost.py
```

### Expected Output
1. **Data Loading**: Confirmation with record count
2. **Data Overview**: Columns, types, missing values, statistics
3. **Feature Engineering**: Holiday detection summary
4. **Model Training** (per target):
   - XGBoost training progress
   - Performance metrics (training and test sets)
   - Feature importance rankings
5. **Visualization**: Path to saved chart

### Output Files
- **Visualization**: `../output_files/model_predictions_xgboost_test_set_<timestamp>.png`
  - Two subplots for VAS_Sold and Speed_Upgrades
  - Actual vs predicted values with confidence bands
  - Performance metrics displayed on charts

## XGBoost Configuration

### Hyperparameters
```python
xgb.XGBRegressor(
    n_estimators=200,         # Number of boosting rounds
    learning_rate=0.05,       # Step size shrinkage (eta)
    max_depth=6,              # Maximum tree depth
    min_child_weight=3,       # Minimum sum of instance weight in child
    subsample=0.8,            # Subsample ratio of training data
    colsample_bytree=0.8,     # Subsample ratio of columns per tree
    random_state=42,          # Reproducibility seed
    n_jobs=-1                 # Use all CPU cores
)
```

### Parameter Explanation

#### n_estimators=200
- Number of sequential trees built
- More trees = better fit but slower training
- 200 provides good balance

#### learning_rate=0.05
- Controls how much each tree contributes
- Lower = more conservative, needs more trees
- 0.05 is conservative to prevent overfitting

#### max_depth=6
- Maximum depth of each tree
- Deeper = more complex patterns but risk overfitting
- 6 is a good default for most problems

#### min_child_weight=3
- Minimum sum of weights needed in child node
- Higher = more conservative (prevents overfitting)
- Useful for imbalanced data

#### subsample=0.8
- Fraction of data used per tree
- 0.8 means each tree uses 80% of data
- Adds randomness to prevent overfitting

#### colsample_bytree=0.8
- Fraction of features used per tree
- Similar to Random Forest's max_features
- Increases model diversity

## XGBoost vs Other Algorithms

### vs Random Forest
**XGBoost Advantages:**
- Sequential learning (each tree corrects previous errors)
- Often better accuracy with same number of trees
- More memory efficient
- Better handling of missing values
- Built-in regularization

**Random Forest Advantages:**
- Parallel tree building (faster training)
- Less hyperparameter tuning needed
- More robust with default settings
- Less prone to overfitting

### vs Linear Regression
**XGBoost Advantages:**
- Captures non-linear relationships
- Handles feature interactions automatically
- More flexible for complex patterns

**Linear Regression Advantages:**
- Much faster training and prediction
- Better interpretability (coefficients)
- Works better when relationships are truly linear
- No hyperparameter tuning needed

### Performance Comparison
Based on testing:
- **VAS_Sold**: 
  - XGBoost: ~83-85% R²
  - Random Forest: ~86% R² ✓ (winner)
  - Linear Regression: ~75% R²

- **Speed_Upgrades**:
  - XGBoost: ~78-80% R²
  - Random Forest: ~75% R²
  - Linear Regression: ~80% R² ✓ (winner)

## Dependencies on Other Files

### Direct Dependencies
- **`../final_dataset.csv`** (required): Training data in parent directory
  - Script uses relative path `../` to access from `misc/` folder

### Output Location
- **`../output_files/`**: Charts saved to parent directory
  - Created automatically if missing
  - Allows comparison with other model outputs

### Directory Structure
```
telecom-sales-predictor/
├── final_dataset.csv                       # Required input
├── output_files/                           # Output location
│   └── model_predictions_xgboost_test_set_<timestamp>.png
└── misc/
    └── analyze_data_xgboost.py            # This script
```

### Related Scripts
- **`analyze_data.py`**: Linear regression baseline
- **`analyze_data_random_forest.py`**: Random Forest implementation
- **`../analyze_data_hybrid.py`**: Final production model

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'xgboost'**
   ```bash
   pip install xgboost
   ```
   Note: XGBoost requires compilation, may take a few minutes to install

2. **ImportError: DLL load failed (Windows)**
   - XGBoost requires Visual C++ Redistributable
   - Download from: https://aka.ms/vs/16/release/vc_redist.x64.exe
   - Or use conda: `conda install -c conda-forge xgboost`

3. **FileNotFoundError: final_dataset.csv not found**
   - Ensure running from `misc/` directory
   - Or adjust path if running from root
   - Verify CSV exists in parent directory

4. **Slow Training**
   - XGBoost with 200 rounds can take 15-45 seconds
   - Reduce `n_estimators` for faster training
   - Ensure `n_jobs=-1` to use all cores

5. **Overfitting (high training R², low test R²)**
   - Decrease `max_depth` (try 4 or 5)
   - Increase `learning_rate` slightly (0.1)
   - Increase `min_child_weight` (5 or 10)
   - Decrease `n_estimators`

6. **Underfitting (low training and test R²)**
   - Increase `max_depth` (try 8 or 10)
   - Decrease `learning_rate` and increase `n_estimators`
   - Decrease `min_child_weight`

## Feature Importance

### XGBoost Importance Types
XGBoost provides multiple importance metrics:
- **Weight**: Number of times feature appears in trees
- **Gain**: Average gain when feature is used (most meaningful)
- **Cover**: Average coverage of feature when used

This script uses **Gain** (average improvement in loss).

### Typical Output
```
Feature Importance (sorted by importance):
  Push_Notifications_Sent: 0.3012
  Emails_Sent: 0.2456
  Day_of_Year: 0.1289
  Month: 0.0987
  Day_of_Week: 0.0854
  Days_To_Holiday: 0.0598
  Channel_Encoded: 0.0432
  Days_From_Holiday: 0.0321
  Is_Holiday: 0.0287
  Near_Holiday: 0.0264
```

## Customization Options

### Speed vs Accuracy Trade-off

**Faster Training (Lower Accuracy):**
```python
xgb.XGBRegressor(
    n_estimators=100,        # Fewer rounds
    learning_rate=0.1,       # Larger steps
    max_depth=5,             # Shallower trees
    ...
)
```

**Better Accuracy (Slower Training):**
```python
xgb.XGBRegressor(
    n_estimators=500,        # More rounds
    learning_rate=0.01,      # Smaller steps
    max_depth=8,             # Deeper trees
    ...
)
```

### Prevent Overfitting
```python
xgb.XGBRegressor(
    max_depth=4,             # Shallower trees
    min_child_weight=5,      # More regularization
    subsample=0.7,           # Less data per tree
    colsample_bytree=0.7,    # Fewer features per tree
    reg_alpha=0.5,           # L1 regularization
    reg_lambda=1.0,          # L2 regularization
    ...
)
```

## Advanced Features

### Early Stopping (Not Used by Default)
Can be enabled to stop when validation score stops improving:
```python
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    early_stopping_rounds=10,
    verbose=False
)
```

### GPU Acceleration (If Available)
```python
xgb.XGBRegressor(
    tree_method='gpu_hist',  # Use GPU
    predictor='gpu_predictor',
    ...
)
```

### Custom Objectives
XGBoost supports custom loss functions for specialized problems.

## Model Evaluation Metrics

### R² Score (Coefficient of Determination)
- Range: -∞ to 1.0
- 1.0 = perfect predictions
- 0.0 = as good as predicting mean
- Negative = worse than predicting mean

### RMSE (Root Mean Squared Error)
- Same units as target variable
- Penalizes large errors more than MAE
- Lower is better

### MAE (Mean Absolute Error)
- Average absolute difference
- More robust to outliers than RMSE
- Lower is better

## Why XGBoost Not Selected for Final Model

While XGBoost is a powerful algorithm, the final production model uses:
- **Random Forest for VAS_Sold**: 2-3% better accuracy (86% vs 83-85%)
- **Linear Regression for Speed_Upgrades**: Simpler, same accuracy (80%)

XGBoost is kept in `misc/` for:
- Future experimentation
- Performance benchmarking
- Alternative implementation if requirements change

## Notes

- This is an **experimental/comparison script**
- Located in `misc/` folder (not production code)
- Used to evaluate XGBoost performance
- Results informed final hybrid model selection
- XGBoost trains sequentially (each tree corrects previous errors)
- Typically achieves 83-85% accuracy for VAS_Sold
- Good alternative if Random Forest has memory constraints
- More hyperparameters to tune than Random Forest
- Requires separate XGBoost library installation
- **Images are optimized at 100 DPI** to keep file sizes ~200-400 KB for efficient MCP transmission and Cloud Desktop compatibility (< 1 MB limit)

