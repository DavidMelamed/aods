"""Simple anomaly detection wrapper."""

import logging

try:
    from pyod.models.iforest import IForest
except Exception:  # pragma: no cover - optional dependency
    IForest = None
    logging.warning("pyod not available; anomaly detection disabled")


def detect_anomalies(data):
    """Return anomaly scores for a list of numeric records."""
    if IForest is None:
        # Fallback: mark no anomalies
        return [0.0 for _ in data]
    model = IForest()
    model.fit([[x] for x in data])
    scores = model.decision_function([[x] for x in data])
    return scores.tolist()
