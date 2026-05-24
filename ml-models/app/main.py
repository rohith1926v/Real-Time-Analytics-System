import argparse
import logging

from app.config.settings import get_settings
from app.consumers.inference_consumer import MLInferenceConsumer
from app.inference.predictor import AnomalyPredictor
from app.models.artifact_store import artifacts_exist, load_artifacts
from app.training.train_model import train_and_save
from app.utils.logging import configure_logging

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ML anomaly detection runtime")
    parser.add_argument("mode", choices=["inference", "train"], nargs="?", default="inference")
    return parser.parse_args()


def ensure_model_artifacts() -> None:
    settings = get_settings()
    if artifacts_exist(settings.artifact_dir):
        logger.info("model_artifacts_found artifact_dir=%s", settings.artifact_dir)
        return
    if not settings.auto_bootstrap_model:
        raise FileNotFoundError(
            f"Missing ML model artifacts in {settings.artifact_dir}. "
            "Run: docker compose run --rm ml-inference python -m app.training.train_model"
        )

    logger.warning("model_artifacts_missing action=auto_bootstrap artifact_dir=%s", settings.artifact_dir)
    train_and_save(settings)


def main() -> None:
    args = parse_args()
    settings = get_settings()
    configure_logging(settings.inference_log_level)
    logger.info("starting_ml_runtime mode=%s", args.mode)

    if args.mode == "train":
        train_and_save(settings)
        return

    ensure_model_artifacts()
    artifacts = load_artifacts(settings.artifact_dir)
    logger.info(
        "model_artifacts_loaded model_name=%s model_version=%s features=%s",
        artifacts.metadata.get("model_name"),
        artifacts.metadata.get("model_version"),
        len(artifacts.metadata.get("feature_columns", [])),
    )
    predictor = AnomalyPredictor(settings=settings, artifacts=artifacts)
    MLInferenceConsumer(settings=settings, predictor=predictor).run()


if __name__ == "__main__":
    main()

