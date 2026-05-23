import random
from ipaddress import IPv4Address

from app.schemas.events import AnomalyEvent, ApiEvent, LoginEvent, NetworkEvent, TelemetryEvent


class SyntheticTelemetryGenerator:
    def __init__(self, anomaly_rate: float) -> None:
        self._anomaly_rate = anomaly_rate
        self._users = [
            ("u-1001", "alex.chen"),
            ("u-1002", "maya.singh"),
            ("u-1003", "nora.patel"),
            ("u-1004", "sam.roberts"),
            ("u-1005", "lina.garcia"),
        ]
        self._countries = ["US", "IN", "DE", "GB", "SG", "BR", "NL"]
        self._devices = ["windows-laptop", "macbook", "linux-workstation", "ios", "android"]
        self._endpoints = ["/api/v1/accounts", "/api/v1/payments", "/api/v1/admin/users", "/api/v1/reports"]
        self._anomaly_types = ["credential_stuffing", "data_exfiltration", "impossible_travel", "api_abuse"]

    def next_event(self) -> TelemetryEvent:
        if random.random() < self._anomaly_rate:
            return self._anomaly_event()

        event_factory = random.choice([self._login_event, self._api_event, self._network_event])
        return event_factory()

    def _login_event(self) -> LoginEvent:
        user_id, username = random.choice(self._users)
        login_success = random.random() > 0.18
        risk_score = random.uniform(3.0, 35.0) if login_success else random.uniform(35.0, 90.0)
        return LoginEvent(
            user_id=user_id,
            username=username,
            source_ip=self._public_ip(),
            country=random.choice(self._countries),
            device_type=random.choice(self._devices),
            login_success=login_success,
            failure_reason=None if login_success else random.choice(["invalid_password", "mfa_failed", "account_locked"]),
            risk_score=round(risk_score, 2),
        )

    def _api_event(self) -> ApiEvent:
        user_id, _ = random.choice(self._users)
        status_code = random.choices([200, 201, 204, 400, 401, 403, 404, 429, 500], weights=[45, 6, 8, 5, 5, 4, 4, 4, 2])[0]
        return ApiEvent(
            user_id=user_id,
            endpoint=random.choice(self._endpoints),
            method=random.choice(["GET", "POST", "PUT", "PATCH", "DELETE"]),
            status_code=status_code,
            response_time_ms=random.randint(20, 2500),
            source_ip=self._public_ip(),
            request_size=random.randint(256, 250_000),
            risk_score=round(random.uniform(5.0, 95.0 if status_code >= 400 else 45.0), 2),
        )

    def _network_event(self) -> NetworkEvent:
        port = random.choice([22, 53, 80, 123, 443, 5432, 6379, 8080, 9200])
        packet_count = random.randint(1, 5000)
        return NetworkEvent(
            source_ip=self._private_ip(),
            destination_ip=self._public_ip(),
            protocol=random.choice(["TCP", "UDP", "ICMP"]),
            bytes_sent=random.randint(128, 4_000_000),
            bytes_received=random.randint(128, 6_000_000),
            port=port,
            packet_count=packet_count,
            risk_score=round(random.uniform(5.0, 88.0 if port in [22, 5432, 6379, 9200] else 50.0), 2),
        )

    def _anomaly_event(self) -> AnomalyEvent:
        user_id, _ = random.choice(self._users)
        anomaly_type = random.choice(self._anomaly_types)
        severity = random.choices(["low", "medium", "high", "critical"], weights=[3, 5, 4, 1])[0]
        descriptions = {
            "credential_stuffing": "Elevated login failures observed across user identities.",
            "data_exfiltration": "Outbound transfer volume exceeded baseline threshold.",
            "impossible_travel": "User activity observed from geographically distant regions.",
            "api_abuse": "Sustained high-volume API access pattern detected.",
        }
        return AnomalyEvent(
            anomaly_type=anomaly_type,
            severity=severity,
            source_ip=self._public_ip(),
            user_id=user_id,
            description=descriptions[anomaly_type],
            risk_score=round(random.uniform(70.0, 99.5), 2),
        )

    @staticmethod
    def _public_ip() -> str:
        return str(IPv4Address(random.randint(int(IPv4Address("23.0.0.1")), int(IPv4Address("223.255.255.254")))))

    @staticmethod
    def _private_ip() -> str:
        return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
