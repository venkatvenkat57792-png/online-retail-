import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import json
from src.preprocess import load_invoice_data
ROOT=Path(__file__).resolve().parents[2]
corrupt=ROOT/"data/processed/corrupt_sample.csv"
if not corrupt.exists():
    import runpy; runpy.run_path(str(ROOT/"src/simulate_data_corruption.py"),run_name="__main__")
try:
    load_invoice_data(corrupt)
except ValueError as exc:
    result={"status":"expected_failure_caught","error":str(exc)}
else:
    raise SystemExit("Corrupted sample unexpectedly passed validation")
(ROOT/"reports/failure_report.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(result)
