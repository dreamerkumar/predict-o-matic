# Instructions: Running the Telecom Sales Analysis

This guide walks you through setting up and running the `analyze_data.py` script to perform predictive analytics on telecom sales data.

## Prerequisites

### Required Software
- **Python 3.7+** (Python 3.8 or higher recommended)
- **pip** (Python package installer)

### Check Your Python Installation
```bash
python3 --version
# Should show: Python 3.x.x

pip3 --version
# Should show: pip x.x.x
```

## Setup Instructions

### Step 1: Navigate to the Project Directory

```bash
cd /Users/vishalkumar/code/frontier/predict-o-matic
```

### Step 2: Install Required Dependencies

The script needs these Python packages:
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `scikit-learn` - Machine learning models
- `matplotlib` - Visualization

**Option A: Install directly (quick start)**
```bash
pip3 install pandas numpy scikit-learn matplotlib
```

**Option B: Use a virtual environment (recommended)**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Install packages
pip install pandas numpy scikit-learn matplotlib

# When done, deactivate
deactivate
```

### Step 3: Verify Data File Exists

Make sure `final_dataset.csv` is in the project directory:

```bash
ls -la final_dataset.csv
```

You should see the file listed. If not, you'll need to generate or obtain it first.

## Running the Analysis

### Basic Execution

Simply run the script:

```bash
python3 analyze_data.py
```

**If using a virtual environment:**
```bash
# Activate first
source venv/bin/activate

# Then run
python analyze_data.py

# Deactivate when done
deactivate
```

### Expected Output

The script will display:

1. **Data Loading Confirmation**
   ```
   Loading data from CSV file...
   Successfully loaded XXX records from final_dataset.csv
   ```

2. **Data Overview**
   - Column names and types
   - Missing value counts
   - Basic statistics (mean, std, min, max)

3. **Model Training Progress**
   - Features used for modeling
   - Train/test split details
   - Training and test set sizes

4. **Model Performance Metrics** (for each target)
   - R² scores (training and test)
   - RMSE (Root Mean Squared Error)
   - MAE (Mean Absolute Error)
   - Feature coefficients

5. **Visualization Confirmation**
   ```
   Visualization saved to: model_predictions_test_set.png
   ```

### Execution Time

- Typical runtime: **5-15 seconds** (depends on dataset size)
- Most time spent on data processing and visualization

## Reviewing the Results

### 1. Check Terminal Output

**Look for these key metrics:**

```
Model Performance for VAS_Sold:
  Training Set:
    R² Score: 0.XXXX
    RMSE: XX.XXXX
    MAE: XX.XXXX

  Test Set:
    R² Score: 0.XXXX
    RMSE: XX.XXXX
    MAE: XX.XXXX
```

**What to check:**
- ✅ R² score > 0.6 on test set = Good model
- ✅ Test R² close to Train R² = Not overfitting
- ⚠️ Test R² << Train R² = Overfitting (model too specific)

### 2. View the Visualization

Open the generated PNG file:

```bash
# On macOS
open model_predictions_test_set.png

# On Linux
xdg-open model_predictions_test_set.png

# On Windows
start model_predictions_test_set.png
```

**What to look for in the chart:**
- Blue line (Actual) and Purple line (Predicted) should be close
- Predictions should stay within the confidence interval bands
- Check if patterns are captured (seasonality, trends)

## Troubleshooting

### Problem: "No module named 'pandas'" (or sklearn, numpy, matplotlib)

**Solution:** Install the missing package
```bash
pip3 install pandas numpy scikit-learn matplotlib
```

### Problem: "Error: final_dataset.csv not found!"

**Solution:** Make sure you're in the correct directory
```bash
pwd  # Check current directory
cd /Users/vishalkumar/code/frontier/predict-o-matic
ls final_dataset.csv  # Verify file exists
```

### Problem: Script runs but poor R² scores (< 0.3)

**Possible causes:**
- Insufficient data (need more records)
- Poor feature selection (need different predictors)
- Non-linear relationships (try polynomial features)
- Too much noise in the data

**Solution:** 
- Check data quality
- Add more relevant features
- Try different time periods for train/test split

### Problem: "ValueError" or "KeyError" about missing columns

**Solution:** Verify your CSV has all required columns:
```python
# Run this quick check
import pandas as pd
df = pd.read_csv('final_dataset.csv')
print(df.columns.tolist())
```

Required columns:
- `Date`
- `Channel`
- `Emails_Sent`
- `Push_Notifications_Sent`
- `VAS_Sold`
- `Speed_Upgrades`

### Problem: Visualization doesn't save or looks weird

**Solution:** Make sure matplotlib backend is configured
```bash
# Try installing pillow for better image support
pip3 install pillow
```

## Understanding the Code Flow

If you want to modify the script, here's the execution flow:

1. **Lines 17-25**: Load CSV data
2. **Lines 27-34**: Display data overview
3. **Lines 41-49**: Feature engineering (date features, encoding)
4. **Lines 51-60**: Define features and targets
5. **Lines 62-76**: Create train/test split
6. **Lines 78-133**: Train models and calculate metrics
7. **Lines 139-223**: Create and save visualization
8. **Lines 228-231**: Main execution

## Customization Options

### Change Train/Test Split Date

Edit line 64:
```python
split_date = pd.Timestamp('2025-08-01')  # Change this date
```

### Add More Features

Edit line 52-53:
```python
feature_columns = ['Day_of_Year', 'Day_of_Week', 'Month', 'Channel_Encoded',
                   'Emails_Sent', 'Push_Notifications_Sent', 
                   'Your_New_Feature']  # Add here
```

### Change Prediction Targets

Edit line 54:
```python
target_columns = ['VAS_Sold', 'Speed_Upgrades', 'Your_New_Target']
```

### Modify Visualization Style

Edit lines 149-210 to customize:
- Figure size (line 149)
- Colors (lines 186, 191)
- Markers and line styles (lines 185, 190)
- DPI/resolution (line 216)

## Next Steps After Running

1. **Analyze the coefficients** - Which features are most important?
2. **Review the visualization** - Are predictions accurate?
3. **Check residuals** - Are errors random or systematic?
4. **Experiment with features** - Can you improve R² scores?
5. **Try different models** - Maybe RandomForest or XGBoost?

## Quick Command Reference

```bash
# Full workflow
cd /Users/vishalkumar/code/frontier/predict-o-matic
python3 analyze_data.py
open model_predictions_test_set.png

# With virtual environment
cd /Users/vishalkumar/code/frontier/predict-o-matic
source venv/bin/activate
python analyze_data.py
open model_predictions_test_set.png
deactivate

# Check if file exists
ls -la final_dataset.csv

# Verify Python packages
pip3 list | grep -E "pandas|numpy|scikit-learn|matplotlib"

# Re-run after changes
python3 analyze_data.py
```

## Getting Help

- **Script comments**: Read inline comments in `analyze_data.py`
- **Analysis overview**: See `analysis_overview.md` for conceptual explanation
- **Python docs**: https://docs.python.org/3/
- **Pandas docs**: https://pandas.pydata.org/docs/
- **Scikit-learn docs**: https://scikit-learn.org/stable/documentation.html

## Success Criteria

You'll know everything worked if you see:

✅ Script completes without errors  
✅ R² scores displayed for both models  
✅ `model_predictions_test_set.png` created in the directory  
✅ Visualization shows actual vs predicted lines that roughly align  
✅ Test set R² > 0.5 (indicates useful predictions)

Happy analyzing! 📊🚀

