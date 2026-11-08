import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from src.monitoring import feature_drift,write_report
if __name__=="__main__":
    current=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[2]/"data/processed/monitoring_invoices.csv"
    if not current.exists(): raise SystemExit(f"Provide a current invoice aggregate CSV: python {Path(__file__).name} <csv>")
    write_report("data_drift_report.json",feature_drift(current=current))
