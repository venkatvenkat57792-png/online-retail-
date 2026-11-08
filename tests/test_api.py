from fastapi.testclient import TestClient
from api.main import app

def test_health_reports_loaded_model():
    with TestClient(app) as client:
        response=client.get("/health")
        assert response.status_code==200
        assert response.json()["model_loaded"] is True

def test_prediction_returns_nonnegative_gbp_estimate():
    with TestClient(app) as client:
        response=client.post("/predict",json={"line_count":5,"distinct_products":4,"total_quantity":12,"country":"United Kingdom"})
    assert response.status_code==200
    result=response.json()
    assert result["predicted_invoice_revenue"]>=0
    assert result["currency"]=="GBP"
    assert result["request_id"]
