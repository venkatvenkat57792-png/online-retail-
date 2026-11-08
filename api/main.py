from contextlib import asynccontextmanager
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from api.model_loader import load_metadata, load_model
from api.monitoring_logger import log_event
from api.preprocessing import FEATURES, features_frame
from api.schemas import InvoiceFeatures, Prediction

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load on startup where possible; missing artifacts leave health available for diagnosis.
    try:
        app.state.model = load_model()
        app.state.model_error = None
    except (FileNotFoundError, ValueError, TypeError) as exc:
        app.state.model = None
        app.state.model_error = str(exc)
    yield

app = FastAPI(title="Online Retail Invoice Revenue Prediction API", description="Estimate GBP invoice revenue from online retail basket features. This service uses the Online Retail transaction dataset; it does not perform churn prediction.", version="1.0.0", lifespan=lifespan)

def get_model():
    model = getattr(app.state, "model", None)
    if model is None:
        try:
            model = load_model()
            app.state.model = model
            app.state.model_error = None
        except (FileNotFoundError, ValueError, TypeError) as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
    return model

@app.get("/health")
def health():
    ready = getattr(app.state, "model", None) is not None
    return JSONResponse(status_code=200 if ready else 503, content={"status": "ready" if ready else "model_unavailable", "model_loaded": ready, "detail": getattr(app.state, "model_error", None)})

@app.get("/model")
def model_info():
    try:
        return load_metadata()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

@app.post("/predict", response_model=Prediction)
def predict(request: InvoiceFeatures, http_request: Request):
    request_id = http_request.headers.get("x-request-id", str(uuid4()))
    started = perf_counter()
    payload = request.model_dump()
    try:
        model = get_model()
        frame = features_frame([{key: payload[key] for key in FEATURES}])
        raw_value = float(model.predict(frame)[0])
        if not (raw_value == raw_value and abs(raw_value) != float("inf")):
            raise ValueError("Model returned a non-finite prediction")
        value = max(0.0, raw_value)
        metadata = load_metadata()
        elapsed_ms = (perf_counter() - started) * 1000
        log_event(request_id=request_id, payload=payload, status="ok", latency_ms=elapsed_ms, prediction=value)
        return Prediction(predicted_invoice_revenue=value, model_version=str(metadata.get("model_version", "local")), request_id=request_id)
    except HTTPException as exc:
        log_event(request_id=request_id, payload=payload, status="error", latency_ms=(perf_counter()-started)*1000, error=str(exc.detail))
        raise
    except Exception as exc:
        log_event(request_id=request_id, payload=payload, status="error", latency_ms=(perf_counter()-started)*1000, error=type(exc).__name__)
        raise HTTPException(status_code=500, detail="Prediction failed; check service logs.") from exc

