from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from app.features.feature_definitions import FEATURE_COLUMNS


@dataclass(frozen=True)
class ModelArtifacts:
    model: IsolationForest
    scaler: StandardScaler
    metadata: dict


def artifacts_exist(artifact_dir: Path) -> bool:
    return (
        (artifact_dir / "isolation_forest.joblib").exists()
        and (artifact_dir / "feature_scaler.joblib").exists()
        and (artifact_dir / "feature_metadata.json").exists()
    )


def save_artifacts(artifact_dir: Path, model: IsolationForest, scaler: StandardScaler, metadata: dict, metrics: dict) -> None:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, artifact_dir / "isolation_forest.joblib")
    joblib.dump(scaler, artifact_dir / "feature_scaler.joblib")
    (artifact_dir / "feature_metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True), encoding="utf-8")
    (artifact_dir / "training_metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")


def load_artifacts(artifact_dir: Path) -> ModelArtifacts:
    model = joblib.load(artifact_dir / "isolation_forest.joblib")
    scaler = joblib.load(artifact_dir / "feature_scaler.joblib")
    metadata = json.loads((artifact_dir / "feature_metadata.json").read_text(encoding="utf-8"))
    if metadata.get("feature_columns") != FEATURE_COLUMNS:
        raise ValueError("Feature metadata does not match current inference feature contract")
    return ModelArtifacts(model=model, scaler=scaler, metadata=metadata)

