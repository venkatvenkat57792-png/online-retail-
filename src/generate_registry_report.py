import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
registry=ROOT/"deployment/registry"
versions=[]
if registry.exists():
    for metadata in registry.glob("*/model_metadata.json"):
        versions.append({"path":str(metadata.parent.relative_to(ROOT)),**json.loads(metadata.read_text(encoding="utf-8"))})
report={"registry":"local file-based","versions":versions}
out=ROOT/"reports/registry_report.json"
out.write_text(json.dumps(report,indent=2),encoding="utf-8")
print(out)
