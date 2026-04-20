# Neighborhood-Disadvantage-Index

Author: Vaibhav Jha 

## 1. Project Description
This project develops a Neighborhood Disadvantage Index using a mixed methods approach combining exploratory factor analysis (EFA) and regression modeling. The goal is to quantify structural disadvantage across U.S. counties and evaluate its relationship with health outcomes such as mental health and obesity.

The pipeline includes:
- Data preprocessing and feature engineering
- Missingness analysis
- Exploratory Factor Analysis (EFA)
- Index construction from factor loadings
- Regression modeling
- Robustness checks

---

## 2. Data Sources
- American Community Survey (ACS) 2015–2019 5-Year Estimates
- CDC PLACES: Local Data for Better Health, Census Tract Data 2021 release

---

## 3. Methodology

### Data Preprocessing
- Handles missing values
- Standardizes variables
- Constructs proportion-based features

### Exploratory Factor Analysis (EFA)
- Implemented using FactorAnalyzer
- Kaiser criterion (eigenvalue > 1)
- Factor loadings threshold ≥ 0.4

### Index Construction
Factors grouped into themes:
- Socioeconomic disadvantage / instability
- Working-class / labor structure
- Severe deprivation / infrastructure deficit

### Regression Model
y = β₀ + β₁ index + β₂ female_prop + β₃ minority_prop + β₄ log(pop)

Outcomes:
- Mental health
- Obesity

---

## 4. Robustness Checks

Model performance comparison:

Mental Health:
- R² (with index): 0.713
- R² (without index): 0.601
- Drop: 0.112

Obesity:
- R² (with index): 0.657
- R² (without index): 0.437
- Drop: 0.220

---

## 5. Environment Setup

Requirements:
- Python 3.x
- pandas, numpy, matplotlib, factor_analyzer, statsmodels

Install environment:
conda env create -f environment.yml
conda activate your_env_name

---

## 6. Usage

Run preprocessing:
python preprocessing.py

Run EFA:
python efa.py

Run regression:
python regression.py

Run robustness checks:
python robustness_checks.py

---

## 7. Outputs
- Plots (histograms, factor visualizations)
- Regression results
- Summary statistics
- Constructed index values

---

## 8. Reproducibility
All analysis is reproducible using the scripts in this repository.  
Data is sourced from publicly available U.S. Census Bureau datasets.

---

## 9. Notes
- Missingness varies across states and features
- Results depend on factor structure and variable construction
- Index interpretation should be done in context of factor loadings
