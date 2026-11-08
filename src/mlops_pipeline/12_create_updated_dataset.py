import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from src.preprocess import load_invoice_data
ROOT=Path(__file__).resolve().parents[2]
if __name__=="__main__":
    rows=load_invoice_data(ROOT/"data/raw/online_retail.csv")
    out=ROOT/"data/processed/updated_invoices.csv"
    rows.to_csv(out,index=False)
    print(f"Wrote {len(rows)} refreshed invoices to {out}")
