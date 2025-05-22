"""Simple anomaly detection wrapper."""

import logging
import statistics
from typing import Iterable, List

try:
    from pyod.models.iforest import IForest
except Exception:  # pragma: no cover - optional dependency
    IForest = None
    logging.warning("pyod not available; using z-score anomaly detection")


def _zscore_anomaly(data: List[float]) -> List[float]:
    if not data:
        return []
    mean = statistics.mean(data)
    stdev = statistics.stdev(data) or 1.0
    return [(x - mean)/stdev for x in data]


def detect_anomalies(data: Iterable[float]) -> List[float]:
    """Return anomaly scores for numeric records."""
    data = list(data)
    if IForest is None:
        return _zscore_anomaly(data)
    model = IForest()
    model.fit([[x] for x in data])
    scores = model.decision_function([[x] for x in data])
    return scores.tolist()
