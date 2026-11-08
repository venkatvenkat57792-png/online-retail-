# Runbook

- Train: `python src/train.py`
- Validate data: `python src/validate_data.py`
- Serve locally: `uvicorn api.main:app --host 127.0.0.1 --port 8000`
- Health: `GET /health`; prediction: `POST /predict`
- Logs: `reports/inference_log.jsonl`
- Retrain when input distribution or validated business performance changes; compare the new evaluation report before replacing the serving artifact.
