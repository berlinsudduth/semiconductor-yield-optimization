"""
Utility Script: Report Generator
Description: Converts the Analysis Notebook into a clean HTML report.
             It executes the notebook first to ensure all graphs are fresh.
"""
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
import os


def generate_html_report():
    # Define paths relative to this script
    # We are in 'src/', so we go up one level (..) then into 'notebooks/'
    notebook_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'notebooks', '01_exploratory_analysis.ipynb'))
    output_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'reports', '01_exploratory_analysis.html'))

    print(f"📖 Reading Notebook: {notebook_path}")

    # 1. Read the Notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # 2. Execute the Notebook (Re-run all cells to get fresh graphs)
    print("⚙️  Executing Notebook (Training Models... please wait)...")
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

    try:
        # Check if the notebook is actually pointing to the right raw data file path
        # The notebook expects "../raw_wafer_data.csv" relative to ITSELF.
        # When we run it programmatically, the working directory matters.
        ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path)}})
    except Exception as e:
        print(f"❌ Error executing notebook: {e}")
        return

    # 3. Convert to HTML
    print("📝 Converting to HTML...")
    html_exporter = HTMLExporter()
    # Exclude code cells if you want a cleaner report (optional)
    # html_exporter.exclude_input = True
    (body, resources) = html_exporter.from_notebook_node(nb)

    # 4. Save the file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure 'reports' folder exists
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(body)

    print(f"✅ Report generated successfully!")
    print(f"📂 Location: {output_path}")


if __name__ == "__main__":
    generate_html_report()