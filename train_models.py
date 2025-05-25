"""Train ML models and log to MLflow."""
from __future__ import annotations

import pandas as pd

try:
    import mlflow
    import xgboost as xgb
    import catboost as cb
except Exception:  # pragma: no cover - optional
    mlflow = None
    xgb = None
    cb = None

from src.aods.models.conversion_model import ConversionModel
from src.aods.models.profit_model import ProfitModel


def load_training_matrix():
    return pd.DataFrame({"x": [0], "y": [0]}), [0]


def main() -> None:
    if mlflow is None:
        print("mlflow not available")
        return
    mlflow.set_tracking_uri("http://mlflow:5000")
    with mlflow.start_run(run_name="daily_train"):
        X, y = load_training_matrix()
        clf = xgb.XGBClassifier() if xgb else None
        if clf:
            clf.fit(X, y)
            mlflow.xgboost.log_model(clf, "conversion_model")
        reg = cb.CatBoostRegressor(verbose=False) if cb else None
        if reg:
            reg.fit(X, y)
            mlflow.catboost.log_model(reg, "profit_model")


if __name__ == "__main__":
    main()
