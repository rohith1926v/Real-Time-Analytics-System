import logging
import random
import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def retry_with_backoff(operation: Callable[[], T], logger: logging.Logger, description: str, max_attempts: int = 12) -> T:
    attempt = 0
    while True:
        attempt += 1
        try:
            return operation()
        except Exception as exc:
            if attempt >= max_attempts:
                logger.exception("%s failed after %s attempts", description, attempt)
                raise
            delay = min(30.0, 1.0 * (2 ** (attempt - 1))) + random.uniform(0, 0.4)
            logger.warning("%s failed attempt=%s reason=%s retry_in=%.2fs", description, attempt, exc, delay)
            time.sleep(delay)

