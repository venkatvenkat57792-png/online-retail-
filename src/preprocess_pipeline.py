import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.preprocess import load_invoice_data
ROOT=Path(__file__).resolve().parents[1]
if __name__=="__main__":
    output=ROOT/"data/processed/invoices.csv"
    output.parent.mkdir(parents=True,exist_ok=True)
    data=load_invoice_data(ROOT/"data/raw/online_retail.csv")
    data.to_csv(output,index=False)
    print(f"Wrote {len(data)} invoice rows to {output}")
