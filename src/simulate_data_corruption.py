from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
if __name__=="__main__":
    raw=pd.read_csv(ROOT/"data/raw/online_retail.csv",encoding="cp1252",nrows=100)
    bad=raw.drop(columns=["Country"])
    out=ROOT/"data/processed/corrupt_sample.csv"
    bad.to_csv(out,index=False)
    print(f"Wrote intentionally invalid sample to {out}")
