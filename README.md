# Online Retail MLOps Project

An end-to-end regression example using the supplied Online Retail transaction dataset. The pipeline aggregates valid transaction lines into invoices and estimates invoice revenue from invoice line count, product variety, total quantity, and country. The target is the sum of `Quantity * UnitPrice`; cancellation invoices and invalid or nonpositive lines are excluded.

## Quick start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-api.txt
python src/train.py
uvicorn api.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the API. `POST /predict` accepts `line_count`, `distinct_products`, `total_quantity`, and `country`. `GET /health` reports model readiness. Inference events, including request IDs and latency, are appended to `reports/inference_log.jsonl`.

The model output is an estimate, not an accounting value. The supplied transactions are from 2010?2011; random invoice holdout metrics are a historical demonstration, not evidence of future-time performance. See [START_HERE.md](START_HERE.md), [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), and [docs/RUNBOOK.md](docs/RUNBOOK.md).

## Pipeline entry points

- `python src/preprocess.py` builds invoice aggregates.
- `python src/train.py` trains and evaluates the model, then writes deployment artifacts.
- `python src/evaluate.py` evaluates the saved model.
- `python src/train_registry.py` creates a local versioned copy.
- `python src/automate_lifecycle.py` trains, applies the basic quality gate, and promotes locally.
- `python src/mlops_pipeline/12_api_performance_monitoring.py` summarizes request outcomes and latency.
- `python src/mlops_pipeline/12_data_drift.py <current_invoice_csv>` compares current data with the training aggregates.

MLflow is optional; the local workflow does not require an MLflow server.
