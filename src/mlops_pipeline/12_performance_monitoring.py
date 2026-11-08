import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from src.monitoring import read_events,write_report
import pandas as pd
if __name__=="__main__":
    events=read_events()
    valid=events[events.get("status",pd.Series(dtype=str)).eq("ok")] if not events.empty else events
    result={"status":"no_labeled_outcomes","requests":int(len(valid)),"message":"Join predictions with actual invoice revenue before computing MAE/RMSE."}
    write_report("performance_monitoring_report.json",result)
