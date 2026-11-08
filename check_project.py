from pathlib import Path
ROOT=Path(__file__).resolve().parent
required=["data/raw/online_retail.csv","data/processed/invoices.csv","src/train.py","api/main.py","deployment/model.pkl","deployment/model_metadata.json","README.md"]
missing=[p for p in required if not (ROOT/p).is_file()]
if missing: raise SystemExit(f"Missing required project files: {missing}")
print("Project inputs, trained artifact, and application files are present.")
