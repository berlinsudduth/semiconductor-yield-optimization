"""
Module: Data Loader for SECOM Dataset
Author: Berlin Sudduth
Role: Independent Consultant / Process Data Analyst

Description:
    This script handles the extraction of raw semiconductor process data from the
    UCI Machine Learning Repository. It is designed to be robust (handling
    connection errors) and reproducible.

    It fetches two separate files (Sensor Data + Pass/Fail Labels), merges them
    into a single Analytics Table, and saves a local CSV backup.
"""

import pandas as pd  # The standard library for tabular data manipulation
import requests  # Library for making HTTP requests (checking internet connection)
import io  # Library for handling byte streams (inputs/outputs)


def load_process_data():
    """
    Fetches and merges the SECOM dataset directly from the UCI Archive URLs.

    The SECOM dataset consists of:
    1. 590 Process Sensor measurements (Features).
    2. A simple Pass/Fail classification (Target).

    Returns:
        pd.DataFrame: A combined DataFrame containing 591 columns (Sensors + Target).
                      Returns None if the download fails.
    """
    print("🔌 Connecting to Fab Database (Direct Server)...")

    # Raw data URLs from the UCI Machine Learning Repository
    # We use the direct .data file links to avoid API dependencies
    url_sensors = "https://archive.ics.uci.edu/ml/machine-learning-databases/secom/secom.data"
    url_labels = "https://archive.ics.uci.edu/ml/machine-learning-databases/secom/secom_labels.data"

    try:
        # --- STEP 1: LOAD SENSOR DATA ---
        print("   - Downloading Sensor Data (590 signals)...")

        # pd.read_csv parameters explained:
        # sep=r"\s+": The raw data is separated by spaces, not commas.
        #             The 'r' denotes a 'raw string' for the Regex pattern \s+ (one or more spaces).
        # header=None: The raw text file does not have column names (Row 0 is data, not headers).
        X = pd.read_csv(url_sensors, sep=r"\s+", header=None)

        # --- STEP 2: LOAD LABELS (YIELD DATA) ---
        print("   - Downloading Label Data (Pass/Fail)...")
        y = pd.read_csv(url_labels, sep=r"\s+", header=None)

        # The label file contains two columns: [1. Pass/Fail, 2. Timestamp].
        # We only need the first column (Pass/Fail status).
        # .iloc[:, [0]] means: "Select all rows (:), and only the column at index 0 ([0])"
        y = y.iloc[:, [0]]

        # Rename the column to 'Target' for clarity in downstream analysis
        # (In this dataset: -1 = Pass, 1 = Fail)
        y.columns = ['Target']

        # --- STEP 3: MERGE ---
        # We concatenate (glue) the Sensors (X) and Labels (y) side-by-side.
        # axis=1 means "glue them horizontally" (add columns, not rows).
        df = pd.concat([X, y], axis=1)

        print(f"✅ Data Loaded Successfully.")
        print(f"   - Total Wafers (Rows): {df.shape[0]}")
        print(f"   - Total Sensors (Columns): {df.shape[1] - 1}")  # Subtract 1 for Target

        return df

    except Exception as e:
        # If the internet is down or the URL changes, this block catches the crash.
        print(f"❌ Error downloading data: {e}")
        return None


# --- THE "GATEKEEPER" BLOCK ---
# This block only runs if you execute this file directly (e.g., 'python data_loader.py').
# If you import this file into a Notebook, this block is ignored.
if __name__ == "__main__":

    # Execute the load function
    df = load_process_data()

    if df is not None:
        # Define the output path. ".." means "go up one directory level" to the main folder.
        output_filename = "../raw_wafer_data.csv"

        # Save to CSV for offline usage.
        # index=False: Do not save the row numbers (0, 1, 2...) as a column in the file.
        df.to_csv(output_filename, index=False)
        print(f"💾 Local backup saved to: {output_filename}")