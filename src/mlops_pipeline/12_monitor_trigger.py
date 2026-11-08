import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
path=ROOT/"reports/data_drift_report.json"
if not path.exists(): raise SystemExit("Run 12_data_drift.py first")
report=json.loads(path.read_text())
psi=report.get("numeric_psi",{})
trigger=any(value is not None and value>=0.2 for value in psi.values())
result={"trigger_retraining":trigger,"threshold_psi":0.2,"observed_psi":psi}
(ROOT/"reports/monitor_trigger_report.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(result)
