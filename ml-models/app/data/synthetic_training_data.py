from __future__ import annotations

import numpy as np
import pandas as pd

from app.features.feature_definitions import FEATURE_COLUMNS


def generate_synthetic_training_data(sample_size: int, anomaly_rate: float, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)
    anomaly_count = max(1, int(sample_size * anomaly_rate))
    normal_count = sample_size - anomaly_count

    normal = pd.DataFrame(
        {
            "failed_login_rate": rng.beta(1.2, 18, normal_count),
            "requests_per_minute": rng.gamma(4.0, 6.0, normal_count),
            "avg_api_response_time": rng.normal(220, 55, normal_count),
            "endpoint_error_rate": rng.beta(1.1, 30, normal_count),
            "suspicious_ip_frequency": rng.poisson(0.8, normal_count),
            "avg_network_bytes": rng.lognormal(9.2, 0.55, normal_count),
            "anomaly_rate": rng.beta(0.8, 45, normal_count),
            "risk_score_moving_average": rng.normal(28, 12, normal_count),
            "geo_login_variance": rng.poisson(1.2, normal_count),
            "high_risk_event_count": rng.poisson(0.7, normal_count),
            "failed_auth_count": rng.poisson(1.0, normal_count),
            "api_5xx_rate": rng.beta(1.0, 45, normal_count),
            "network_bytes_spike_score": rng.gamma(1.5, 0.7, normal_count),
            "unique_ip_count": rng.poisson(2.0, normal_count) + 1,
            "session_activity_score": rng.normal(42, 11, normal_count),
            "label": np.zeros(normal_count, dtype=int),
        }
    )

    anomalies = pd.DataFrame(
        {
            "failed_login_rate": rng.beta(8, 2.2, anomaly_count),
            "requests_per_minute": rng.gamma(11.0, 11.0, anomaly_count),
            "avg_api_response_time": rng.normal(1100, 350, anomaly_count),
            "endpoint_error_rate": rng.beta(6.0, 4.0, anomaly_count),
            "suspicious_ip_frequency": rng.poisson(18.0, anomaly_count),
            "avg_network_bytes": rng.lognormal(11.3, 0.9, anomaly_count),
            "anomaly_rate": rng.beta(7.0, 3.0, anomaly_count),
            "risk_score_moving_average": rng.normal(82, 10, anomaly_count),
            "geo_login_variance": rng.poisson(8.0, anomaly_count) + 2,
            "high_risk_event_count": rng.poisson(9.0, anomaly_count),
            "failed_auth_count": rng.poisson(14.0, anomaly_count),
            "api_5xx_rate": rng.beta(5.5, 4.5, anomaly_count),
            "network_bytes_spike_score": rng.gamma(7.0, 1.4, anomaly_count),
            "unique_ip_count": rng.poisson(20.0, anomaly_count) + 3,
            "session_activity_score": rng.normal(88, 16, anomaly_count),
            "label": np.ones(anomaly_count, dtype=int),
        }
    )

    dataset = pd.concat([normal, anomalies], ignore_index=True)
    dataset[FEATURE_COLUMNS] = dataset[FEATURE_COLUMNS].clip(lower=0)
    return dataset.sample(frac=1.0, random_state=random_state).reset_index(drop=True)

