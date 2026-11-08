from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import joblib
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
if __name__=="__main__":
    model=joblib.load(ROOT/"deployment/model.pkl")
    sample=pd.DataFrame([{"line_count":5,"distinct_products":4,"total_quantity":12,"country":"United Kingdom"}])
    a=model.predict(sample); b=model.predict(sample)
    if not (a==b).all(): raise SystemExit("Repeated inference produced different predictions")
    print("Deterministic inference check passed")
