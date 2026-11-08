from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
source=ROOT/"data/raw/online_retail.csv"
raw=pd.read_csv(source,encoding="cp1252",parse_dates=["InvoiceDate"],date_format="mixed",low_memory=False)
cut=raw.InvoiceDate.max()-pd.Timedelta(days=90)
out=ROOT/"data/processed/recent_90_day_transactions.csv"
raw[raw.InvoiceDate>=cut].to_csv(out,index=False)
print(f"Wrote recent transaction window to {out}")
