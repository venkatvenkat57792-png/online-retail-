import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from src.monitoring import read_events,write_report
if __name__=="__main__":
    events=read_events()
    rows=events.tail(1000).to_dict(orient="records") if not events.empty else []
    write_report("request_history_report.json",{"count":len(rows),"events":rows})
