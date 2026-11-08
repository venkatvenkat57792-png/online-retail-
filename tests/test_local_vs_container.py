import joblib
import pandas as pd
from pathlib import Path

def test_serialized_pipeline_prediction_is_finite():
    root=Path(__file__).resolve().parents[1]
    model=joblib.load(root/"deployment/model.pkl")
    row=pd.DataFrame([{"line_count":5,"distinct_products":4,"total_quantity":12,"country":"United Kingdom"}])
    prediction=float(model.predict(row)[0])
    assert prediction==prediction and abs(prediction)<float("inf")
