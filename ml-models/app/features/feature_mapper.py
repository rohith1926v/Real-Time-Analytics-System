from __future__ import annotations

from typing import Any

from app.features.feature_definitions import FEATURE_COLUMNS, FEATURE_DEFAULTS


class FeatureMapper:
    def to_feature_vector(self, payload: dict[str, Any]) -> dict[str, float]:
        features = dict(FEATURE_DEFAULTS)

        if payload.get("feature_name") and "feature_value" in payload:
            self._map_feature_engineering_event(payload, features)
        else:
            self._map_analytics_event(payload, features)

        return {name: self._safe_float(features.get(name, FEATURE_DEFAULTS[name])) for name in FEATURE_COLUMNS}

    def entity_id(self, payload: dict[str, Any]) -> str:
        for key in ("entity_id", "user_id", "source_ip", "endpoint", "event_type"):
            value = payload.get(key)
            if value:
                return str(value)
        return "unknown"

    def source_event_id(self, payload: dict[str, Any]) -> str | None:
        value = payload.get("event_id") or payload.get("source_event_id")
        return str(value) if value else None

    def event_type(self, payload: dict[str, Any], source_topic: str) -> str:
        return str(payload.get("event_type") or payload.get("metric_type") or payload.get("feature_name") or source_topic)

    @staticmethod
    def _map_feature_engineering_event(payload: dict[str, Any], features: dict[str, float]) -> None:
        feature_name = str(payload.get("feature_name", ""))
        if feature_name in features:
            features[feature_name] = payload.get("feature_value", features[feature_name])

        event_count = payload.get("event_count")
        if feature_name == "user_failed_login_rate":
            features["failed_auth_count"] = event_count or 0.0
        if feature_name == "endpoint_error_rate":
            features["api_5xx_rate"] = payload.get("feature_value", 0.0)
        if feature_name == "suspicious_ip_frequency":
            features["unique_ip_count"] = max(float(event_count or 1.0), 1.0)

    @staticmethod
    def _map_analytics_event(payload: dict[str, Any], features: dict[str, float]) -> None:
        event_type = payload.get("event_type")
        risk_score = payload.get("risk_score") or payload.get("risk_score_moving_average") or 0.0
        features["risk_score_moving_average"] = risk_score
        features["high_risk_event_count"] = payload.get("high_risk_event_count", 1.0 if float(risk_score or 0.0) >= 70 else 0.0)

        if event_type == "login":
            login_success = payload.get("login_success", True)
            features["failed_login_rate"] = 0.0 if login_success else 1.0
            features["failed_auth_count"] = 0.0 if login_success else 1.0
            features["geo_login_variance"] = 1.0 if payload.get("country") else 0.0
            features["session_activity_score"] = risk_score
        elif event_type == "api":
            status_code = int(payload.get("status_code") or 200)
            features["avg_api_response_time"] = payload.get("response_time_ms", 0.0)
            features["requests_per_minute"] = payload.get("event_count", 1.0)
            features["endpoint_error_rate"] = 1.0 if status_code >= 400 else 0.0
            features["api_5xx_rate"] = 1.0 if status_code >= 500 else 0.0
        elif event_type == "network":
            bytes_sent = payload.get("bytes_sent") or 0.0
            bytes_received = payload.get("bytes_received") or 0.0
            avg_bytes = float(bytes_sent) + float(bytes_received)
            features["avg_network_bytes"] = avg_bytes
            features["network_bytes_spike_score"] = avg_bytes / 100000.0
            features["unique_ip_count"] = 1.0
        elif event_type == "anomaly":
            features["anomaly_rate"] = 1.0
            features["suspicious_ip_frequency"] = 1.0

        for key in ("rolling_event_count", "event_count"):
            if key in payload:
                features["requests_per_minute"] = max(features["requests_per_minute"], payload[key] or 0.0)

        for key in ("avg_api_response_time", "endpoint_error_rate", "avg_network_bytes", "anomaly_rate", "geo_login_variance"):
            if key in payload and payload[key] is not None:
                features[key] = payload[key]

    @staticmethod
    def _safe_float(value: Any) -> float:
        try:
            if value is None:
                return 0.0
            return float(value)
        except (TypeError, ValueError):
            return 0.0

