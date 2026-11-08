import time
import joblib
import pandas as pd
from pathlib import Path

def test_local_prediction_latency_under_two_seconds():
    root=Path(__file__).resolve().parents[1]
    model=joblib.load(root/"deployment/model.pkl")
    row=pd.DataFrame([{"line_count":5,"distinct_products":4,"total_quantity":12,"country":"United Kingdom"}])
    start=time.perf_counter(); model.predict(row); elapsed=time.perf_counter()-start
    assert elapsed<2.0
