import json
import logging
import threading
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger("online_retail_api")
logging.basicConfig(level=logging.INFO)
LOG_PATH = Path(__file__).resolve().parents[1] / "reports" / "inference_log.jsonl"
_LOCK = threading.Lock()

def log_event(*, request_id, payload, status, latency_ms, prediction=None, error=None):
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": request_id,
        "status": status,
        "latency_ms": round(float(latency_ms), 3),
        "input": payload,
        "predicted_invoice_revenue": prediction,
        "error": error,
    }
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with _LOCK, LOG_PATH.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
    except OSError:
        logger.exception("Could not append inference log for request %s", request_id)
    if status != "ok":
        logger.warning("prediction request %s failed: %s", request_id, error)
    else:
        logger.info("prediction request %s completed in %.3f ms", request_id, latency_ms)

def log_prediction(payload, prediction, request_id="unknown", latency_ms=0.0):
    log_event(request_id=request_id, payload=payload, status="ok", latency_ms=latency_ms, prediction=prediction)
