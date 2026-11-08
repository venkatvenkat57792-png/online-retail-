"""Train and persist a local versioned model artifact."""
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.train import train, ROOT
if __name__=="__main__":
    _,metrics=train()
    registry=ROOT/"deployment/registry/online-retail-v1"
    registry.mkdir(parents=True,exist_ok=True)
    import shutil
    shutil.copy2(ROOT/"deployment/model.pkl",registry/"model.pkl")
    metadata=json.loads((ROOT/"deployment/model_metadata.json").read_text())
    metadata["metrics"]=metrics
    (registry/"model_metadata.json").write_text(json.dumps(metadata,indent=2))
    print(f"Registered local model at {registry}")
