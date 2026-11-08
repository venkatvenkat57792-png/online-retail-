import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
files=["data_drift_report.json","prediction_drift_report.json","concept_drift_report.json"]
reports={name:json.loads((ROOT/"reports"/name).read_text()) for name in files if (ROOT/"reports"/name).exists()}
out={"available_reports":reports,"summary":"Review feature PSI, prediction summaries, and labeled performance together."}
(ROOT/"reports/drift_analysis_report.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(out)
