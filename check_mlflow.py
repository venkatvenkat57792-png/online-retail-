try:
    import mlflow
except ImportError:
    raise SystemExit("MLflow is not installed. Install requirements-mlflow.txt to enable tracking.")
print(f"MLflow {mlflow.__version__} is importable; tracking URI: {mlflow.get_tracking_uri()}")
