from pathlib import Path
import shutil
root = Path(__file__).resolve().parents[1]
model = root / "deployment/model.pkl"
if not model.exists():
    raise SystemExit("Train the model first: python src/train.py")
print(f"Artifact ready for deployment: {model}")
