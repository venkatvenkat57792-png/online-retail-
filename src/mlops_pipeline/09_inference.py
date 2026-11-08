import joblib
import pandas as pd
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
model=joblib.load(ROOT/"deployment/model.pkl")
row=pd.DataFrame([{"line_count":5,"distinct_products":4,"total_quantity":12,"country":"United Kingdom"}])
print({"sample_predicted_invoice_revenue":float(model.predict(row)[0]),"currency":"GBP"})
