from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
actual=ROOT/"data/processed/actual_predictions.csv"
report={"status":"not_evaluated","reason":"Concept drift requires labeled actual revenue paired with predictions.","expected_file":str(actual.relative_to(ROOT))}
if actual.exists(): report.update({"status":"labels_available","rows":sum(1 for _ in actual.open(encoding="utf-8"))-1})
(ROOT/"reports/concept_drift_report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(report)
