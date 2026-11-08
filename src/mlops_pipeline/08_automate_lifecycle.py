import runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
runpy.run_path(str(ROOT/"src/automate_lifecycle.py"),run_name="__main__")
