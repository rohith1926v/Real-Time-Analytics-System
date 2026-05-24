from prometheus_client import Counter, Gauge, Histogram, start_http_server

ML_PREDICTIONS_TOTAL = Counter("ml_predictions_total", "Total ML predictions published")
ML_ANOMALIES_TOTAL = Counter("ml_anomalies_total", "Total ML anomaly predictions")
ML_PREDICTION_ERRORS_TOTAL = Counter("ml_prediction_errors_total", "Total ML prediction errors")
ML_INFERENCE_LATENCY_SECONDS = Histogram("ml_inference_latency_seconds", "ML inference latency")
ML_MODEL_LOADED_STATUS = Gauge("ml_model_loaded_status", "ML model loaded status")


def start_metrics_server(port: int) -> None:
    start_http_server(port)
