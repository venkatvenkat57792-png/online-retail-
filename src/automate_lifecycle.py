import json
import shutil
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.train import train, ROOT

def run():
    _, metrics=train()
    # Local promotion gate: candidate must have finite metrics and positive R?.
    passed=all(float(v)==float(v) for v in metrics.values() if isinstance(v,(int,float))) and metrics["r2"]>0
    decision={"candidate_metrics":metrics,"promoted":bool(passed),"decision":"promote" if passed else "reject","registry":"local file-based"}
    report=ROOT/"reports/lifecycle_report.json"
    report.write_text(json.dumps(decision,indent=2),encoding="utf-8")
    if passed:
        registry=ROOT/"deployment/registry"/"online-retail-v1"
        registry.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/"deployment/model.pkl",registry/"model.pkl")
        shutil.copy2(ROOT/"deployment/model_metadata.json",registry/"model_metadata.json")
    print(json.dumps(decision,indent=2))
    return decision
if __name__=="__main__": run()
