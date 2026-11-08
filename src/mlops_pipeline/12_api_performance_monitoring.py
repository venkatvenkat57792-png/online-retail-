from src.monitoring import api_performance,write_report
if __name__=="__main__": write_report("api_performance_report.json",api_performance())
