from pathlib import Path
p=Path(__file__).parent/"deployment/model_metadata.json"
print(p.read_text() if p.exists() else "Train first: python src/train.py")
