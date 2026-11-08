import pandas as pd

NUMERIC_FEATURES = ["line_count", "distinct_products", "total_quantity"]
CATEGORICAL_FEATURES = ["country"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

def features_frame(rows):
    """Convert validated API dictionaries into the model's ordered input columns."""
    frame = pd.DataFrame(rows, columns=FEATURES)
    for column in NUMERIC_FEATURES:
        frame[column] = pd.to_numeric(frame[column], errors="raise")
    frame["country"] = frame["country"].astype("string").str.strip()
    if frame["country"].isna().any() or frame["country"].eq("").any():
        raise ValueError("country must contain a non-empty value")
    return frame
