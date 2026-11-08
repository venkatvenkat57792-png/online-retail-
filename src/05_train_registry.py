from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).parent / "mlops_pipeline" / "05_train_registry.py"), run_name="__main__")
