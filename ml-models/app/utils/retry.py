import logging
import random
import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def retry_with_backoff(
    operation: Callable[[], T],
    logger: logging.Logger,
    description: str,
    max_attempts: int = 12,
    base_delay_seconds: float = 1.0,
    max_delay_seconds: float = 30.0,
) -> T:
    attempt = 0
    while True:
        attempt += 1
        try:
            return operation()
        except Exception as exc:
            if attempt >= max_attempts:
                logger.exception("%s failed after %s attempts", description, attempt)
                raise

            delay = min(max_delay_seconds, base_delay_seconds * (2 ** (attempt - 1)))
            delay += random.uniform(0, min(0.5, delay * 0.1))
            logger.warning("%s failed on attempt %s: %s. Retrying in %.2fs", description, attempt, exc, delay)
            time.sleep(delay)

