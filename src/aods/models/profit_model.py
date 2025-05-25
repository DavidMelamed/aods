"""CatBoost regressor wrapper."""
from __future__ import annotations


from typing import Iterable, List

try:
    from catboost import CatBoostRegressor
except Exception:  # pragma: no cover - optional
    CatBoostRegressor = None



class ProfitModel:
    def __init__(self):

        self.model = CatBoostRegressor(verbose=False) if CatBoostRegressor else None
        self.mean_profit = 0.0

    def fit(self, X: Iterable, y: Iterable) -> 'ProfitModel':
        X_list, y_list = list(X), list(y)
        if self.model is not None:
            self.model.fit(X_list, y_list)
        if y_list:
            self.mean_profit = sum(y_list) / len(y_list)
        return self

    def predict(self, X: Iterable) -> List[float]:
        X_list = list(X)
        if self.model is not None:
            return self.model.predict(X_list).tolist()
        return [self.mean_profit for _ in X_list]
