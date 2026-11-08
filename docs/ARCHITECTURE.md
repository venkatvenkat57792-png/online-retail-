# Architecture

The CSV contains transaction lines. `src/preprocess.py` removes cancellations, invalid values, and nonpositive quantities/prices, then groups valid lines by invoice. Revenue is summed from quantity times unit price. The model estimates that target from line count, product variety, total quantity, and country using a sklearn pipeline. FastAPI loads the pipeline and appends requests/results to a JSONL log.

This is a demonstration baseline. A random invoice split can put invoices from the same customer in both sets, and historical data is old; production evaluation should use a time-based and customer-aware design.
