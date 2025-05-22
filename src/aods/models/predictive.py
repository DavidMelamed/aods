"""Predictive model wrappers."""

import logging
from typing import Iterable, List

try:
    import lightgbm as lgb
except Exception:  # pragma: no cover - optional
    lgb = None
    logging.warning("lightgbm not available; using dummy model")


class ConversionRateModel:
    """Train/predict conversion rates using LightGBM if available."""

    def __init__(self):
        self.model = lgb.LGBMRegressor() if lgb else None

    def fit(self, X: Iterable, y: Iterable):
        if self.model is None:
            return None
        self.model.fit(list(X), list(y))
        return self

    def predict(self, X: Iterable) -> List[float]:
        if self.model is None:
            return [0.0 for _ in X]
        return self.model.predict(list(X)).tolist()
