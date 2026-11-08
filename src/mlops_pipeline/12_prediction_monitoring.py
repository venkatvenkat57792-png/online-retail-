import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from src.monitoring import prediction_drift,api_performance,write_report
if __name__=="__main__": write_report("prediction_monitoring_report.json",{"predictions":prediction_drift(),"api":api_performance()})
