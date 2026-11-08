from functools import lru_cache
from pathlib import Path
import json
import joblib

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "deployment" / "model.pkl"
METADATA_PATH = ROOT / "deployment" / "model_metadata.json"

@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(f"Model artifact missing: {MODEL_PATH}. Run python src/train.py first.")
    if not METADATA_PATH.is_file():
        raise FileNotFoundError(f"Model metadata missing: {METADATA_PATH}. Run python src/train.py first.")
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    if metadata.get("target") != "invoice_revenue":
        raise ValueError("The deployed model is not an invoice revenue model.")
    model = joblib.load(MODEL_PATH)
    if not callable(getattr(model, "predict", None)):
        raise TypeError("Loaded model artifact does not provide predict().")
    return model

def load_metadata():
    if not METADATA_PATH.is_file():
        raise FileNotFoundError(f"Model metadata missing: {METADATA_PATH}")
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))
