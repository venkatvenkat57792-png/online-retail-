import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
current=ROOT/"reports/evaluation_report.json"
previous=ROOT/"reports/previous_evaluation_report.json"
if not current.exists(): raise SystemExit("Run training first")
new=json.loads(current.read_text())
old=json.loads(previous.read_text()) if previous.exists() else None
result={"candidate":new,"baseline":old,"comparison":"baseline_missing" if old is None else "compare MAE/RMSE lower is better; R2 higher is better"}
(ROOT/"reports/model_comparison_report.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(result)
