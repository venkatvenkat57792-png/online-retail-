import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
if __name__=="__main__":
    path=ROOT/"data/processed/invoices.csv"
    if not path.exists(): raise SystemExit("Processed invoices missing; run python src/preprocess.py")
    frame=pd.read_csv(path)
    required={"line_count","distinct_products","total_quantity","country","invoice_revenue"}
    missing=required-set(frame.columns)
    if missing: raise SystemExit(f"Processed output missing columns: {sorted(missing)}")
    if frame.empty or frame[list(required)].isna().any().any(): raise SystemExit("Processed output is empty or has nulls")
    print(f"Validated {len(frame)} processed invoices")
