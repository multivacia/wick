"""Retry helpers with exponential backoff, jitter, and Retry-After support."""

from __future__ import annotations

import random
import time
from collections.abc import Callable
from typing import TypeVar

from wick.ingestion.providers.base import AuthConfigError, ProviderError

T = TypeVar("T")


def retry_call(
    fn: Callable[[], T],
    *,
    max_retries: int = 5,
    base_seconds: float = 1.0,
    sleep_fn: Callable[[float], None] = time.sleep,
    rng: random.Random | None = None,
) -> tuple[T, int]:
    """Execute fn with retries. Returns (result, retry_count).

    Does not retry AuthConfigError or non-retryable ProviderError.
    """
    rand = rng or random.Random()
    attempts = 0
    last_exc: Exception | None = None

    while attempts <= max_retries:
        try:
            return fn(), attempts
        except AuthConfigError:
            raise
        except ProviderError as exc:
            last_exc = exc
            if not exc.retryable or attempts >= max_retries:
                raise
            delay = _compute_delay(exc, attempts, base_seconds, rand)
            sleep_fn(delay)
            attempts += 1
        except Exception as exc:
            last_exc = exc
            if attempts >= max_retries:
                raise ProviderError(str(exc), retryable=True) from exc
            delay = base_seconds * (2**attempts) + rand.uniform(0, 0.5)
            sleep_fn(delay)
            attempts += 1

    assert last_exc is not None
    raise last_exc


def _compute_delay(
    exc: ProviderError,
    attempt: int,
    base_seconds: float,
    rand: random.Random,
) -> float:
    retry_after = getattr(exc, "retry_after", None)
    if isinstance(retry_after, (int, float)) and retry_after > 0:
        return float(retry_after) + rand.uniform(0, 0.25)
    return base_seconds * (2**attempt) + rand.uniform(0, 0.5)
