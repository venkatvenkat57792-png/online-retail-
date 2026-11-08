from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
raw=pd.read_csv(ROOT/"data/raw/online_retail.csv",encoding="cp1252",parse_dates=["InvoiceDate"],date_format="mixed",low_memory=False)
cut=raw.InvoiceDate.max()-pd.Timedelta(days=90)
out=ROOT/"data/processed/evolved_transactions.csv"
raw.loc[raw.InvoiceDate>=cut].to_csv(out,index=False)
print(f"Wrote evolved transaction batch to {out}")
