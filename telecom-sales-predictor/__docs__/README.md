# Telecom Sales Predictor - Documentation Index

Welcome to the comprehensive documentation for the Telecom Sales Predictor project. This folder contains detailed documentation for all Python scripts in the project.

## 📚 Documentation Overview

This documentation provides detailed information about each script including:
- **Purpose**: What the script does and why it exists
- **Prerequisites**: Required files, packages, and setup
- **How to Run**: Step-by-step execution instructions
- **Dependencies**: Relationships with other files and scripts
- **Troubleshooting**: Common issues and solutions
- **Customization**: Options for adapting the scripts

## 🗂️ Quick Navigation

### Main Production Scripts

These are the primary scripts used in the production workflow:

#### 1. [analyze_data_hybrid.md](./analyze_data_hybrid.md)
**Hybrid Machine Learning Model (Final Production Model)**
- Trains Random Forest for VAS_Sold (86.4% accuracy)
- Trains Linear Regression for Speed_Upgrades (80.2% accuracy)
- Generates performance visualizations
- **Use this for**: Training and evaluating the final production models

#### 2. [create_test_dataset_updated.md](./create_test_dataset_updated.md)
**December 2025 Test Dataset Generator**
- Reads marketing campaigns from Excel
- Creates formatted test dataset CSV
- Prepares data for predictions
- **Use this for**: Generating December 2025 test data from marketing plans

#### 3. [predict_december_2025.md](./predict_december_2025.md)
**December 2025 Sales Predictions**
- Applies trained models to December 2025
- Generates detailed predictions and forecasts
- Creates cumulative visualization charts
- **Use this for**: Predicting December 2025 sales based on marketing campaigns

### Experimental Scripts (misc/ folder)

These scripts were used for algorithm comparison and data acquisition:

#### 4. [analyze_data_random_forest.md](./analyze_data_random_forest.md)
**Random Forest Baseline**
- Pure Random Forest implementation for both targets
- ~86% accuracy for VAS_Sold (selected for production)
- ~75% accuracy for Speed_Upgrades
- **Use this for**: Understanding Random Forest performance and comparison

#### 5. [analyze_data_xgboost.md](./analyze_data_xgboost.md)
**XGBoost Implementation**
- Gradient boosting approach
- ~83-85% accuracy for VAS_Sold
- ~78-80% accuracy for Speed_Upgrades
- **Use this for**: Comparing XGBoost against other algorithms

#### 6. [analyze_data.md](./analyze_data.md)
**Linear Regression Baseline**
- Simplest baseline model
- ~73-76% accuracy for VAS_Sold
- ~80% accuracy for Speed_Upgrades (selected for production!)
- **Use this for**: Baseline performance and understanding linear relationships

#### 7. [postgres_connection.md](./postgres_connection.md)
**Database Connection Utility**
- Fetches data from PostgreSQL database
- Loads three tables into Pandas DataFrames
- Initial data acquisition step
- **Use this for**: Retrieving raw data from database

## 🔄 Typical Workflow

### For New Users - Understanding the Project

1. **Start with** [analyze_data_hybrid.md](./analyze_data_hybrid.md) - Understand the final production model
2. **Then read** [analyze_data.md](./analyze_data.md) - Learn about the baseline approach
3. **Compare with** [analyze_data_random_forest.md](./analyze_data_random_forest.md) and [analyze_data_xgboost.md](./analyze_data_xgboost.md)
4. **Understand why** the hybrid approach was chosen

### For Making Predictions

1. **First run** [create_test_dataset_updated.md](./create_test_dataset_updated.md) - Generate test dataset
2. **Then run** [predict_december_2025.md](./predict_december_2025.md) - Make predictions
3. Review the generated charts and CSV files

### For Data Acquisition

1. **Start with** [postgres_connection.md](./postgres_connection.md) - Fetch data from database
2. Process and combine the data
3. Create `final_dataset.csv` for training

## 📊 Model Performance Summary

| Script | VAS_Sold R² | Speed_Upgrades R² | Selected For |
|--------|-------------|-------------------|--------------|
| **Linear Regression** | 0.73-0.76 | **0.80** ✓ | Speed_Upgrades |
| **Random Forest** | **0.86** ✓ | 0.75-0.78 | VAS_Sold |
| **XGBoost** | 0.83-0.85 | 0.78-0.80 | Not selected |
| **Hybrid (Final)** | **0.864** | **0.802** | **Production** |

The hybrid model combines the best algorithm for each target, achieving **83.3% average accuracy**.

## 🎯 Key Files Referenced in Documentation

All scripts reference these key files:

- **`final_dataset.csv`**: Historical training data (Sep 2024 - Oct 2025)
- **`test_dataset_dec_2025.csv`**: December 2025 test data with marketing campaigns
- **`updated Dec Marketing events.xlsx`**: Marketing campaign schedule for December 2025
- **`.env`**: Database credentials (for postgres_connection.py)

## 📁 Directory Structure

```
telecom-sales-predictor/
├── __docs__/                           # This documentation folder
│   ├── README.md                       # This file
│   ├── analyze_data_hybrid.md
│   ├── create_test_dataset_updated.md
│   ├── predict_december_2025.md
│   ├── analyze_data_random_forest.md
│   ├── analyze_data_xgboost.md
│   ├── analyze_data.md
│   └── postgres_connection.md
├── analyze_data_hybrid.py              # Main production script
├── create_test_dataset_updated.py      # Test data generator
├── predict_december_2025.py            # Prediction script
├── final_dataset.csv                   # Training data
├── test_dataset_dec_2025.csv          # Test data
├── updated Dec Marketing events.xlsx   # Marketing campaigns
├── output_files/                       # Generated outputs
│   ├── *.png                          # Visualization charts
│   └── *.csv                          # Prediction results
└── misc/                               # Experimental scripts
    ├── analyze_data.py
    ├── analyze_data_random_forest.py
    ├── analyze_data_xgboost.py
    └── postgres_connection.py
```

## 🔧 Installation & Setup

### Option 1: Using Virtual Environment (Recommended)

Using a virtual environment isolates project dependencies and prevents conflicts with other Python projects.

#### Step 1: Create Virtual Environment
```bash
# Navigate to project directory
cd /path/to/telecom-sales-predictor

# Create virtual environment
python3 -m venv venv
```

#### Step 2: Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt when activated.

#### Step 3: Install Packages

For main production scripts:
```bash
pip install pandas numpy scikit-learn matplotlib openpyxl
```

For XGBoost (optional):
```bash
pip install xgboost
```

For database connection (optional):
```bash
pip install psycopg2-binary python-dotenv
```

**All-in-One Installation:**
```bash
pip install pandas numpy scikit-learn matplotlib openpyxl xgboost psycopg2-binary python-dotenv
```

#### Step 4: Verify Installation
```bash
python -c "import pandas, numpy, sklearn, matplotlib; print('All packages installed successfully!')"
```

#### Step 5: Deactivate (when done)
```bash
deactivate
```

### Option 2: Global Installation (Not Recommended)

If you prefer to install packages globally (not recommended as it may cause conflicts):

For main production scripts:
```bash
pip install pandas numpy scikit-learn matplotlib openpyxl
```

For XGBoost (optional):
```bash
pip install xgboost
```

For database connection (optional):
```bash
pip install psycopg2-binary python-dotenv
```

### All-in-One Installation (Global)
```bash
pip install pandas numpy scikit-learn matplotlib openpyxl xgboost psycopg2-binary python-dotenv
```

### Package Versions (Tested)

The scripts have been tested with the following versions:
- Python: 3.8+
- pandas: 2.0+
- numpy: 1.24+
- scikit-learn: 1.3+
- matplotlib: 3.7+
- openpyxl: 3.1+
- xgboost: 2.0+ (optional)
- psycopg2-binary: 2.9+ (optional)
- python-dotenv: 1.0+ (optional)

## 💡 Tips for Using This Documentation

1. **Each documentation file is self-contained** - You can read any file independently
2. **Use the "Dependencies" section** in each file to understand relationships
3. **Check "Troubleshooting" sections** for common issues
4. **Review "Customization Options"** to adapt scripts to your needs
5. **Performance metrics** are provided for comparison

## 🤝 Contributing

When adding new scripts, please:
1. Create corresponding `.md` file in `__docs__/`
2. Follow the same structure as existing documentation
3. Update this README with a link to the new documentation
4. Include all sections: Purpose, Prerequisites, How to Run, Dependencies, Troubleshooting

## 📖 Documentation Format

Each documentation file follows this structure:
1. **Purpose**: High-level overview
2. **What It Does**: Detailed functionality breakdown
3. **Prerequisites**: Required files and packages
4. **How to Run**: Execution instructions
5. **Output Files**: Description of generated files
6. **Dependencies on Other Files**: Relationships and requirements
7. **Troubleshooting**: Common issues and solutions
8. **Customization Options**: How to adapt the script
9. **Notes**: Additional context and best practices

## 📞 Getting Help

If you encounter issues not covered in the documentation:
1. Check the **Troubleshooting** section of the relevant documentation
2. Verify all **Prerequisites** are met
3. Ensure **Required Files** exist in correct locations
4. Review **Dependencies** to understand file relationships
5. Check Python package versions are compatible

## 📝 Version History

- **v1.0** (2025-11-18): Initial comprehensive documentation for all scripts
  - 7 Python scripts documented
  - Main production workflow documented
  - Experimental scripts documented
  - Database connection utility documented

---

**Last Updated**: November 18, 2025  
**Documented Scripts**: 7  
**Total Documentation Pages**: 8 (including this README)

