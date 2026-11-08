import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import json
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from src.preprocess import load_invoice_data

ROOT=Path(__file__).resolve().parents[1]
FEATURES=["line_count","distinct_products","total_quantity","country"]
def evaluate():
    model_path=ROOT/"deployment/model.pkl"
    if not model_path.exists(): raise SystemExit("Model not found; run python src/train.py first")
    data=load_invoice_data(ROOT/"data/raw/online_retail.csv")
    X=data[FEATURES]; y=data["invoice_revenue"]
    _,X_test,_,y_test=train_test_split(X,y,test_size=.2,random_state=42)
    model=joblib.load(model_path); pred=model.predict(X_test)
    metrics={"mae":float(mean_absolute_error(y_test,pred)),"rmse":float(mean_squared_error(y_test,pred)**.5),"r2":float(r2_score(y_test,pred)),"test_invoices":int(len(y_test))}
    (ROOT/"reports/evaluation_report.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8")
    print(json.dumps(metrics,indent=2)); return metrics
if __name__=="__main__": evaluate()
