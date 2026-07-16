"""Retry helper tests (no network)."""

from wick.ingestion.providers.base import AuthConfigError, ProviderError
from wick.ingestion.providers.retry import retry_call


def test_retries_then_succeeds():
    calls = {"n": 0}
    sleeps: list[float] = []

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ProviderError("temporary", retryable=True)
        return "ok"

    result, retries = retry_call(flaky, max_retries=5, base_seconds=0.01, sleep_fn=sleeps.append)
    assert result == "ok"
    assert retries == 2
    assert len(sleeps) == 2


def test_auth_error_not_retried():
    calls = {"n": 0}

    def boom():
        calls["n"] += 1
        raise AuthConfigError("bad token")

    try:
        retry_call(boom, max_retries=5, sleep_fn=lambda _: None)
        raise AssertionError("expected AuthConfigError")
    except AuthConfigError:
        pass
    assert calls["n"] == 1
