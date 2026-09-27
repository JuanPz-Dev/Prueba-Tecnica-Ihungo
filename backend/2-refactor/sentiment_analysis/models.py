from dataclasses import dataclass


@dataclass(frozen=True)
class SentimentResult:
    negative: float
    neutral: float
    positive: float