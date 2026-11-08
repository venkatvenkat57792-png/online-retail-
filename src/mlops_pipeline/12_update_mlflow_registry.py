"""Optional registry update. Without MLflow, train_registry creates a local version."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).resolve().parents[2]/"src/train_registry.py"),run_name="__main__")
