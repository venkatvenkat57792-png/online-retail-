"""Optional MLflow wrapper; local training remains usable without MLflow installed."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.train import train
if __name__=="__main__":
    try:
        import mlflow
    except ImportError as exc:
        raise SystemExit("MLflow is optional. Install mlflow to use this entry point, or run python src/train.py.") from exc
    with mlflow.start_run():
        model,metrics=train()
        mlflow.log_metrics({k:v for k,v in metrics.items() if isinstance(v,(int,float))})
        mlflow.log_param("target","invoice_revenue")
        mlflow.sklearn.log_model(model,"model")
