import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
path=ROOT/"reports/performance_report.json"
report=json.loads(path.read_text()) if path.exists() else {"status":"no performance history"}
(ROOT/"reports/performance_trend_report.json").write_text(json.dumps({"history":[report]},indent=2),encoding="utf-8")
print("Wrote one-run performance trend report")
