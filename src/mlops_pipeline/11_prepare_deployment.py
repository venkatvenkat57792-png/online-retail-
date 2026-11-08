import runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
runpy.run_path(str(ROOT/"deployment/deploy_production.py"),run_name="__main__")
