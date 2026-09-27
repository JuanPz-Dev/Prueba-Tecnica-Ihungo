import pytest

from sentiment_analysis.paralleldots_provider import ParallelDotsProvider


class FakeProviderError(Exception):
    pass

def test_analyze_returns_sentiment(monkeypatch):
    def fake_sentiment(text):
        return {
            "sentiment": {
                "negative": 0.10,
                "neutral": 0.20,
                "positive": 0.70,
            }
        }

    monkeypatch.setattr(
        "sentiment_analysis.paralleldots_provider.paralleldots.sentiment",
        fake_sentiment,
    )

    provider = ParallelDotsProvider(
        api_key="fake-key",
        max_retries=0,
    )

    result = provider.analyze("Este producto me gustó.")

    assert result.negative == 10.0
    assert result.neutral == 20.0
    assert result.positive == 70.0

def test_analyze_retries_after_provider_error(monkeypatch):
    attempts = 0
    waits = []

    def fake_sentiment(text):
        nonlocal attempts
        attempts += 1

        if attempts < 3:
            raise FakeProviderError("Error temporal del proveedor")

        return {
            "sentiment": {
                "negative": 0.10,
                "neutral": 0.20,
                "positive": 0.70,
            }
        }

    def fake_sleep(seconds):
        waits.append(seconds)

    monkeypatch.setattr(
        "sentiment_analysis.paralleldots_provider.paralleldots.sentiment",
        fake_sentiment,
    )

    monkeypatch.setattr(
        "sentiment_analysis.paralleldots_provider.time.sleep",
        fake_sleep,
    )

    provider = ParallelDotsProvider(
        api_key="fake-key",
        max_retries=2,
        backoff_factor=1,
    )

    result = provider.analyze("Este producto me gustó.")

    assert attempts == 3
    assert waits == [1, 2]

    assert result.negative == 10.0
    assert result.neutral == 20.0
    assert result.positive == 70.0

def test_analyze_raises_error_after_all_retries(monkeypatch):
    attempts = 0
    waits = []

    def fake_sentiment(text):
        nonlocal attempts
        attempts += 1
        raise FakeProviderError("Error del proveedor")

    def fake_sleep(seconds):
        waits.append(seconds)

    monkeypatch.setattr(
        "sentiment_analysis.paralleldots_provider.paralleldots.sentiment",
        fake_sentiment,
    )

    monkeypatch.setattr(
        "sentiment_analysis.paralleldots_provider.time.sleep",
        fake_sleep,
    )

    provider = ParallelDotsProvider(
        api_key="fake-key",
        max_retries=2,
        backoff_factor=1,
    )

    with pytest.raises(Exception, match="Error del proveedor"):
        provider.analyze("Texto de prueba")

    assert attempts == 3
    assert waits == [1, 2]