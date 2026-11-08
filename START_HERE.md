# Start here

1. Install `requirements-api.txt` in a Python 3.10+ environment.
2. Keep the provided file at `data/raw/online_retail.csv`.
3. Run `python src/train.py` to validate, split by invoice, fit a random-forest regressor, and write model/preprocessor artifacts and reports.
4. Start the API with `uvicorn api.main:app --reload`; open `/docs` for the interactive schema.
5. Try `POST /predict` with `{"line_count": 5, "distinct_products": 4, "total_quantity": 12, "country": "United Kingdom"}`.

The target is invoice revenue, aggregated from valid positive-quantity transaction lines. Random invoice split is for a reproducible lab exercise; it does not establish future-time performance.
