import logging
import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def retry_with_backoff(fn: Callable[[], T], logger: logging.Logger, description: str, attempts: int = 8) -> T:
    delay = 1.0
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except Exception as exc:
            if attempt == attempts:
                raise
            logger.warning("%s failed attempt=%s error=%s retry_in=%ss", description, attempt, exc, delay)
            time.sleep(delay)
            delay = min(delay * 2, 30)
    raise RuntimeError(f"{description} failed")
