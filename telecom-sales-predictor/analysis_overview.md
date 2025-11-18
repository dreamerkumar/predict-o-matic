# Telecom Sales Analysis Overview

## Purpose

This script performs predictive analytics on telecom sales data using linear regression models. It analyzes the relationship between marketing activities (emails, push notifications) and sales outcomes (VAS products sold and speed upgrades) to help forecast future performance.

## What It Does

### 1. Data Loading
- Reads telecom sales data from `final_dataset.csv`
- Validates data integrity and displays summary statistics
- Reports on data types, missing values, and basic distributions

### 2. Feature Engineering
The script transforms raw data into meaningful features for modeling:

**Temporal Features:**
- `Day_of_Year`: Day number in the year (1-365)
- `Day_of_Week`: Day of the week (0=Monday, 6=Sunday)
- `Month`: Month number (1-12)

**Categorical Features:**
- `Channel_Encoded`: Binary encoding of sales channel (0=App, 1=Web)

**Marketing Features:**
- `Emails_Sent`: Number of marketing emails sent
- `Push_Notifications_Sent`: Number of push notifications sent

### 3. Predictive Modeling

The script builds **two separate Linear Regression models** to predict:

1. **VAS_Sold** (Value-Added Services sold)
   - Products like insurance, security, cloud storage, etc.

2. **Speed_Upgrades** (Internet speed tier upgrades)
   - Customers upgrading their internet speed

### 4. Train-Test Split Strategy

**Date-based split** (not random) to simulate real-world forecasting:

- **Training Period**: September 2024 - July 2025 (~11 months)
  - Used to learn patterns and relationships
  
- **Test Period**: August 2025 - October 2025 (last 3 months)
  - Used to evaluate prediction accuracy on "future" unseen data

This approach mirrors actual business use cases where you train on historical data and predict future outcomes.

### 5. Model Evaluation

For each target variable, the script calculates:

- **R² Score**: How well the model explains variance (0 to 1, higher is better)
- **RMSE** (Root Mean Squared Error): Average prediction error magnitude
- **MAE** (Mean Absolute Error): Average absolute prediction error

Metrics are calculated for both training and test sets to detect overfitting.

### 6. Feature Importance Analysis

The script displays the coefficient for each feature, showing:
- Which factors most strongly influence sales
- Whether the relationship is positive or negative
- The magnitude of each feature's impact

### 7. Visualization

Creates a comprehensive visualization (`model_predictions_test_set.png`) showing:

- **Actual vs Predicted values** for the test period (Aug-Oct 2025)
- **95% Confidence Intervals** around predictions
- Daily aggregated trends for both VAS_Sold and Speed_Upgrades
- Model performance metrics (R² scores) on the charts

## Business Value

This analysis helps answer questions like:

- **Forecasting**: What sales can we expect next month?
- **Marketing ROI**: How effective are emails vs push notifications?
- **Channel Performance**: Do App or Web users convert better?
- **Seasonal Trends**: When are sales naturally higher/lower?
- **Resource Planning**: How many staff/inventory needed for forecasted demand?

## Technical Approach

**Algorithm**: Linear Regression
- **Pros**: Simple, interpretable, fast, shows feature relationships clearly
- **Cons**: Assumes linear relationships, sensitive to outliers
- **Best for**: Understanding relationships and baseline predictions

**Why Linear Regression?**
- Provides clear feature coefficients (business insights)
- Fast training and prediction
- Works well when relationships are approximately linear
- Good baseline before trying complex models

## Output Files

1. **model_predictions_test_set.png**
   - Visual comparison of actual vs predicted sales
   - Dual subplot showing both target variables
   - Includes confidence intervals and performance metrics
   - High-resolution (300 DPI) suitable for presentations

## Model Performance Interpretation

**R² Score Guidelines:**
- **0.80-1.00**: Excellent fit (model explains 80%+ of variance)
- **0.60-0.80**: Good fit (useful for forecasting)
- **0.40-0.60**: Moderate fit (some predictive value)
- **0.00-0.40**: Poor fit (consider different features or models)

**RMSE/MAE:**
- Lower values indicate more accurate predictions
- Compare to the average value of the target to assess relative error
- Should be similar between train and test (if much higher on test = overfitting)

## Data Requirements

The script expects `final_dataset.csv` with these columns:
- `Date`: Date of the sales record
- `Channel`: Sales channel (App or Web)
- `Emails_Sent`: Marketing emails sent
- `Push_Notifications_Sent`: Push notifications sent
- `VAS_Sold`: Value-added services sold (target)
- `Speed_Upgrades`: Speed upgrades sold (target)

## Next Steps for Improvement

Potential enhancements to consider:
1. Try polynomial features for non-linear relationships
2. Add more marketing features (SMS, ads, promo codes)
3. Include customer demographics or behavior data
4. Test other algorithms (Random Forest, XGBoost)
5. Implement cross-validation for more robust evaluation
6. Add prediction intervals using bootstrapping
7. Build an API to serve predictions in real-time

