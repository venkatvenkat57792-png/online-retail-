import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.preprocess import load_invoice_data

ROOT = Path(__file__).resolve().parents[1]
NUMERIC = ["line_count", "distinct_products", "total_quantity"]
CATEGORICAL = ["country"]
FEATURES = NUMERIC + CATEGORICAL

def train():
    data = load_invoice_data(ROOT / "data/raw/online_retail.csv")
    X, y = data[FEATURES], data["invoice_revenue"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    prep = ColumnTransformer([
        ("numeric", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), NUMERIC),
        ("country", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), CATEGORICAL),
    ])
    model = Pipeline([("preprocessor", prep), ("regressor", RandomForestRegressor(n_estimators=250, min_samples_leaf=2, random_state=42, n_jobs=-1))])
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    metrics = {"mae": float(mean_absolute_error(y_test, pred)), "rmse": float(mean_squared_error(y_test, pred) ** 0.5), "r2": float(r2_score(y_test, pred)), "train_invoices": len(X_train), "test_invoices": len(X_test)}
    (ROOT / "deployment").mkdir(exist_ok=True)
    (ROOT / "reports").mkdir(exist_ok=True)
    joblib.dump(model, ROOT / "deployment/model.pkl")
    joblib.dump(model.named_steps["preprocessor"], ROOT / "deployment/preprocessor.pkl")
    metadata = {"model_version": "local-v1", "problem": "invoice revenue regression", "target": "invoice_revenue", "features": FEATURES, "currency": "GBP", "training_rows": len(data), "random_state": 42}
    (ROOT / "deployment/model_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    (ROOT / "reports/evaluation_report.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    return model, metrics

if __name__ == "__main__":
    train()
