# StockSense-Inventory-Prediction
# StockSense: Inventory Shortage Prediction and Product Demand Mining

## Project Overview
StockSense is a Data Warehouse and Data Mining project that analyzes retail sales data, studies product demand patterns, predicts future demand, and identifies products that may require restocking.

## Objectives
- Clean and preprocess retail transaction data.
- Analyze product demand and sales patterns.
- Group products using K-Means clustering.
- Predict product demand using Random Forest regression.
- Generate inventory shortage alerts using simulated stock values.

## Technologies Used
- Python
- Pandas and NumPy
- Matplotlib
- Scikit-learn
- Streamlit
- Google Colab
- GitHub

## Project Files
- `StockSense.ipynb` — Data cleaning, analysis, clustering, and prediction.
- `app.py` — Streamlit web dashboard.
- `requirements.txt` — Required Python libraries.
- `StockSense_Report.csv` — Generated report, if available.

## How to Run
Install the required libraries:

```bash
python -m pip install -r requirements.txt
```

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

## Note
The retail transaction dataset does not provide actual inventory levels. Simulated stock values are used for educational shortage-alert demonstrations.
