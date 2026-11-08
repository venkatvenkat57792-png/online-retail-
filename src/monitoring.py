"""Shared local monitoring utilities for API events and invoice feature data."""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
DATA = ROOT / "data" / "processed"

def read_events(path=None):
    path = Path(path) if path else REPORTS / "inference_log.jsonl"
    if not path.exists():
        return pd.DataFrame()
    rows=[]
    for line in path.read_text(encoding="utf-8").splitlines():
        try: rows.append(json.loads(line))
        except json.JSONDecodeError: continue
    return pd.DataFrame(rows)

def write_report(name, payload):
    REPORTS.mkdir(parents=True, exist_ok=True)
    target=REPORTS/name
    target.write_text(json.dumps(payload,indent=2,allow_nan=False),encoding="utf-8")
    print(target)
    return payload

def psi(expected, actual, bins=10):
    expected=pd.to_numeric(expected,errors="coerce").dropna().to_numpy()
    actual=pd.to_numeric(actual,errors="coerce").dropna().to_numpy()
    if not len(expected) or not len(actual): return None
    edges=np.unique(np.quantile(expected,np.linspace(0,1,bins+1)))
    if len(edges)<2: return 0.0
    edges[0],edges[-1]=-np.inf,np.inf
    e=np.histogram(expected,bins=edges)[0].astype(float); a=np.histogram(actual,bins=edges)[0].astype(float)
    e=np.clip(e/e.sum(),1e-6,None); a=np.clip(a/a.sum(),1e-6,None)
    return float(np.sum((a-e)*np.log(a/e)))

def feature_drift(baseline=None,current=None):
    baseline=pd.read_csv(baseline or DATA/"invoices.csv")
    current=pd.read_csv(current or DATA/"monitoring_invoices.csv")
    report={"baseline_rows":len(baseline),"current_rows":len(current),"numeric_psi":{},"categorical_distribution_changed":{}}
    for col in ["line_count","distinct_products","total_quantity","invoice_revenue"]:
        if col in baseline and col in current: report["numeric_psi"][col]=psi(baseline[col],current[col])
    if "country" in baseline and "country" in current:
        base=baseline.country.value_counts(normalize=True); now=current.country.value_counts(normalize=True)
        report["categorical_distribution_changed"]=bool(not base.index.equals(now.index) or not base.reindex(base.index.union(now.index),fill_value=0).equals(now.reindex(base.index.union(now.index),fill_value=0)))
    return report

def api_performance(path=None):
    events=read_events(path)
    if events.empty: return {"requests":0,"message":"No inference events recorded yet."}
    latency=pd.to_numeric(events.get("latency_ms"),errors="coerce").dropna()
    return {"requests":int(len(events)),"successes":int((events.status=="ok").sum()) if "status" in events else 0,"errors":int((events.status!="ok").sum()) if "status" in events else 0,"latency_ms":{"p50":float(latency.quantile(.5)) if len(latency) else None,"p95":float(latency.quantile(.95)) if len(latency) else None,"max":float(latency.max()) if len(latency) else None}}

def prediction_drift(path=None):
    events=read_events(path)
    if events.empty or "predicted_invoice_revenue" not in events: return {"requests":0,"message":"No prediction events recorded yet."}
    values=pd.to_numeric(events.predicted_invoice_revenue,errors="coerce").dropna()
    return {"requests":int(len(values)),"mean":float(values.mean()),"median":float(values.median()),"std":float(values.std(ddof=0)),"min":float(values.min()),"max":float(values.max())}
