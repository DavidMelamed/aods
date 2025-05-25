"""Ranking model using XGBoost."""
from __future__ import annotations

from typing import Iterable, List

try:
    import xgboost as xgb
except Exception:  # pragma: no cover - optional
    xgb = None


class RankModel:
    """Predict rank probability."""

    def __init__(self) -> None:
        self.model = xgb.XGBRegressor() if xgb else None

    def fit(self, X: Iterable, y: Iterable) -> "RankModel":
        if self.model is not None:
            self.model.fit(list(X), list(y))
        return self

    def predict(self, X: Iterable) -> List[float]:
        if self.model is not None:
            return self.model.predict(list(X)).tolist()
        return [0.0 for _ in X]
