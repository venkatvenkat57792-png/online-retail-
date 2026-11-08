import json
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
metrics_path=ROOT/"reports/evaluation_report.json"
if not metrics_path.exists(): raise SystemExit("Run evaluation first")
metrics=json.loads(metrics_path.read_text())
passed=all(math.isfinite(float(metrics[k])) for k in ("mae","rmse","r2")) and metrics["mae"]>=0 and metrics["rmse"]>=0 and metrics["r2"]>0
report={"status":"passed" if passed else "failed","criteria":{"finite_metrics":True,"r2_positive":metrics["r2"]>0},"metrics":metrics}
(ROOT/"reports/quality_gate_report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
if not passed: raise SystemExit(1)
