from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from src.monitoring import api_performance,prediction_drift,write_report
if __name__=="__main__":
    write_report("monitoring_summary.json",{"api_performance":api_performance(),"prediction_drift":prediction_drift()})
