"""CatBoost regressor wrapper."""
from __future__ import annotations

try:
    import catboost as cb
except Exception:  # pragma: no cover
    cb = None


class ProfitModel:
    def __init__(self):
        self.model = cb.CatBoostRegressor(verbose=False) if cb else None
        self.mean = 0.0

    def fit(self, X, y):
        if self.model:
            self.model.fit(X, y)
        if len(y):
            self.mean = sum(y) / len(y)
        return self

    def predict(self, X):
        if self.model:
            return self.model.predict(X).tolist()
        return [self.mean for _ in range(len(X))]
