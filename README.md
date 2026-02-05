# Automated Sensor Anomaly Detection for Wafer Yield Improvement

**Project Status:** Active | **Role:** Independent Process Data Consultant

## 1. Executive Summary
In semiconductor manufacturing, process excursions can lead to significant yield loss (scrap). This project analyzed the **SECOM dataset** (1567 wafers, 591 sensors) to identify the root cause of a 6.6% yield loss.

**Key Findings:**
* **Data Integrity:** Identified 144 sensors with zero variance or >50% missing data, removing them to reduce noise.
* **Root Cause Analysis:** Using a Random Forest Classifier, **Sensor 59** was identified as the primary driver of failure (Importance Score: 0.030, 2x higher than next feature).
* **Failure Mode:** Distribution analysis reveals a "Right Shift" anomaly. Wafers with higher values on Sensor 59 are significantly more likely to fail.
* **Recommendation:** Implement a tighter Upper Control Limit (UCL) on Sensor 59 based on the "Golden Path" baseline of passing wafers.

> **Note:** GitHub cannot render the interactive HTML report directly. To see the full analysis including visualizations, please view the [Exploratory Analysis Notebook](notebooks/01_exploratory_analysis.ipynb).

## 2. Technical Methodology
* **Data Source:** UCI Machine Learning Repository (SECOM Data).
* **Stack:** Python, Pandas, Scikit-Learn, Matplotlib/Seaborn.
* **Key Techniques:**
    * **Preprocessing:** Variance Thresholding (removing "dead" sensors) and Null Value Imputation.
    * **Feature Engineering:** Boruta / Random Forest Feature Importance to rank sensor impact.
    * **Modeling:** Logistic Regression for baseline classification of Pass/Fail wafers.

## 3. Getting Started
**Note on Data:** The raw data files (`raw_wafer_data.csv`) are not included in this repository to maintain a lightweight footprint.

To generate the data locally:

1. Clone the repository:
   ```bash
   git clone [https://github.com/berlinsudduth/semiconductor-yield-optimization.git](https://github.com/berlinsudduth/semiconductor-yield-optimization.git)
   ```

2. Run the data loader script:
   ```bash
   python src/data_loader.py
   ```

3. The CSV files will appear in the main directory, ready for analysis.

## 4. Project Structure
```text
├── notebooks
│   └── 01_exploratory_analysis.ipynb   <- Main analysis and visualization
├── reports
│   └── 01_exploratory_analysis.html    <- Rendered HTML report
├── src
│   ├── data_loader.py                  <- Script to download and merge web data
│   └── generate_report.py              <- Utility to build the HTML report
├── .gitignore                          <- Standard python ignore file
└── README.md                           <- The top-level documentation
```