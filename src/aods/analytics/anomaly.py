"""Simple anomaly detection wrapper."""

import logging
import statistics
from typing import Iterable, List

try:
    from pyod.models.iforest import IForest
except Exception:  # pragma: no cover - optional dependency
    IForest = None

    logging.warning("pyod not available; anomaly detection disabled")

try:
    from sklearn.neighbors import LocalOutlierFactor
except Exception:  # pragma: no cover - optional dependency
    LocalOutlierFactor = None


def detect_anomalies(data):
    """Return anomaly scores for a list of numeric records."""
    if IForest is not None:
        model = IForest()
        model.fit([[x] for x in data])
        scores = model.decision_function([[x] for x in data])
        return scores.tolist()

    if LocalOutlierFactor is not None:
        lof = LocalOutlierFactor(novelty=True)
        lof.fit([[x] for x in data])
        scores = -lof.decision_function([[x] for x in data])
        return scores.tolist()

    mean = statistics.mean(data) if data else 0.0
    stdev = statistics.stdev(data) if len(data) > 1 else 1.0
    return [abs(x - mean) / stdev for x in data]
