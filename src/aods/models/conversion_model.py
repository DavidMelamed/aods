"""XGBoost classifier wrapper."""
from __future__ import annotations

from typing import Iterable, List

try:
    import xgboost as xgb
except Exception:  # pragma: no cover - optional

    xgb = None


class ConversionModel:
    def __init__(self):
        self.model = xgb.XGBClassifier() if xgb else None

    def fit(self, X: Iterable, y: Iterable) -> 'ConversionModel':
        if self.model is not None:
            self.model.fit(list(X), list(y))
        return self

    def predict(self, X: Iterable) -> List[float]:
        if self.model is not None:
            return self.model.predict_proba(list(X))[:, 1].tolist()
        return [0.0 for _ in X]

