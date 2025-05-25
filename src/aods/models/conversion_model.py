"""XGBoost classifier wrapper."""
from __future__ import annotations

try:
    import xgboost as xgb
except Exception:  # pragma: no cover
    xgb = None


class ConversionModel:
    def __init__(self):
        self.model = xgb.XGBClassifier() if xgb else None

    def fit(self, X, y):
        if self.model:
            self.model.fit(X, y)
        return self

    def predict(self, X):
        if self.model:
            return self.model.predict_proba(X)[:, 1].tolist()
        return [0.0 for _ in range(len(X))]
