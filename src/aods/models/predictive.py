"""Predictive model wrappers."""

import logging
from typing import Iterable, List
import math


try:
    import lightgbm as lgb
except Exception:  # pragma: no cover - optional
    lgb = None

    logging.warning("lightgbm not available; using simple logistic regression")


class ConversionRateModel:
    """Train/predict conversion rates using LightGBM or fallback logistic regression."""

    def __init__(self):
        self.model = lgb.LGBMRegressor() if lgb else None
        self.coefs = []
        self.intercept = 0.0

    def _fit_logistic(self, X: List[List[float]], y: List[int], lr: float = 0.01, epochs: int = 100):
        if not X:
            return
        dim = len(X[0])
        self.coefs = [0.0] * dim
        self.intercept = 0.0
        for _ in range(epochs):
            for xi, yi in zip(X, y):
                z = self.intercept + sum(c*f for c, f in zip(self.coefs, xi))
                z = max(min(z, 20), -20)
                pred = 1/(1 + math.exp(-z))
                err = pred - yi
                self.intercept -= lr * err
                for i in range(dim):
                    self.coefs[i] -= lr * err * xi[i]

    def _predict_logistic(self, X: List[List[float]]) -> List[float]:
        preds = []
        for xi in X:
            z = self.intercept + sum(c*f for c, f in zip(self.coefs, xi))
            z = max(min(z, 20), -20)
            preds.append(1/(1 + math.exp(-z)))
        return preds

    def fit(self, X: Iterable, y: Iterable):
        X_list = [list(x) for x in X]
        y_list = list(y)
        if self.model is None:
            self._fit_logistic(X_list, y_list)
        else:
            self.model.fit(X_list, y_list)
        return self

    def predict(self, X: Iterable) -> List[float]:
        X_list = [list(x) for x in X]
        if self.model is None:
            return self._predict_logistic(X_list)
        return self.model.predict(X_list).tolist()

