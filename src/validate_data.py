import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pathlib import Path
from src.preprocess import load_invoice_data

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    invoices = load_invoice_data(root / "data/raw/online_retail.csv")
    assert len(invoices) > 0 and invoices.notna().all().all()
    assert (invoices["invoice_revenue"] > 0).all()
    print(f"Validated {len(invoices)} usable invoices")
