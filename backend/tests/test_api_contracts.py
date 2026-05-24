import importlib
import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient


def load_backend_app(tmp_path: Path):
    for name in list(sys.modules):
        if name == "app" or name.startswith("app."):
            del sys.modules[name]
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{tmp_path / 'test.db'}"
    os.environ["BACKEND_CORS_ORIGINS"] = "http://localhost:5173"
    os.environ["PROMETHEUS_URL"] = "http://localhost:9090"
    return importlib.import_module("app.main").app


def test_health_endpoint_and_security_headers(tmp_path):
    app = load_backend_app(tmp_path)
    with TestClient(app) as client:
        response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"


def test_dashboard_alert_monitoring_and_threat_api_surfaces(tmp_path):
    app = load_backend_app(tmp_path)
    with TestClient(app) as client:
        assert client.get("/api/v1/dashboard/overview").status_code == 200
        assert client.get("/api/v1/alerts/stats").status_code == 200
        assert client.get("/api/v1/incidents/recent").status_code == 200
        assert client.get("/api/v1/monitoring/overview").status_code == 200
        assert client.get("/api/v1/threat-intel/overview").status_code == 200
        assert client.get("/api/v1/mitre/tactics").status_code == 200
        assert client.get("/metrics").status_code == 200
