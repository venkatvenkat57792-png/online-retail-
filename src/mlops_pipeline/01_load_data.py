from src.preprocess import load_invoice_data
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
data=load_invoice_data(ROOT / "data/raw/online_retail.csv")
print(data.shape)
