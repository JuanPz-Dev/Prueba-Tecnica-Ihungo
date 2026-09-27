from typing import Protocol

from .models import SentimentResult


class SentimentProvider(Protocol):
    def analyze(self, text: str) -> SentimentResult:
        ...