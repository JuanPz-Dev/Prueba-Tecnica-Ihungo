import logging
import time

import paralleldots  # type: ignore[import-untyped]

from .models import SentimentResult

logger = logging.getLogger(__name__)

class ParallelDotsProvider:
    def __init__(self, api_key: str, max_retries: int = 3,backoff_factor: float = 1.0) -> None:
        self.api_key = api_key
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        paralleldots.set_api_key(self.api_key)

    def analyze(self, text: str) -> SentimentResult:
        for attempt in range(self.max_retries + 1):
            try:
                response = paralleldots.sentiment(text)
                sentiment = response.get("sentiment")
                if not sentiment:
                    raise ValueError(
                        "La respuesta del proveedor no contiene sentimiento."
                    )
                return SentimentResult(
                    negative=float(sentiment.get("negative", 0)) * 100,
                    neutral=float(sentiment.get("neutral", 0)) * 100,
                    positive=float(sentiment.get("positive", 0)) * 100,
                )

            except Exception:
                if attempt == self.max_retries:
                    raise
                wait_time = self.backoff_factor * (2**attempt)
                logger.warning(
                    "Error al consultar el proveedor. "
                    "Reintentando en %.1f segundos.",
                    wait_time,
                )
                time.sleep(wait_time)
        raise RuntimeError("No se pudo obtener el análisis de sentimiento.")