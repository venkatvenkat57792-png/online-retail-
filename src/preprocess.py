from pathlib import Path
import pandas as pd

REQUIRED = {"InvoiceNo", "StockCode", "Quantity", "UnitPrice", "Country"}

def load_invoice_data(path):
    frame = pd.read_csv(path, dtype={"InvoiceNo": str, "StockCode": str}, low_memory=False, encoding="cp1252")
    missing = REQUIRED - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    frame["Quantity"] = pd.to_numeric(frame["Quantity"], errors="coerce")
    frame["UnitPrice"] = pd.to_numeric(frame["UnitPrice"], errors="coerce")
    frame = frame.dropna(subset=["InvoiceNo", "StockCode", "Quantity", "UnitPrice", "Country"])
    frame = frame[~frame["InvoiceNo"].str.startswith("C", na=False)]
    frame = frame[(frame["Quantity"] > 0) & (frame["UnitPrice"] > 0)].copy()
    frame["line_revenue"] = frame["Quantity"] * frame["UnitPrice"]
    invoices = frame.groupby("InvoiceNo", as_index=False).agg(
        line_count=("StockCode", "size"), distinct_products=("StockCode", "nunique"),
        total_quantity=("Quantity", "sum"), country=("Country", "first"),
        invoice_revenue=("line_revenue", "sum"))
    return invoices

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    data = load_invoice_data(root / "data/raw/online_retail.csv")
    out = root / "data/processed/invoices.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(out, index=False)
    print(f"Wrote {len(data)} invoices to {out}")

