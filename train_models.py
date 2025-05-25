
"""Train and persist predictive models."""

import json
from pathlib import Path

import mlflow
import pandas as pd
import joblib

from aods.feature_store import FEATURE_PATH, build_feature_table
from aods.models import ConversionModel, ProfitModel, RankModel

mlflow.set_tracking_uri("http://mlflow:5000")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)


def load_training_matrix():
    if not FEATURE_PATH.exists():
        build_feature_table()
    if FEATURE_PATH.exists():
        df = pd.read_parquet(FEATURE_PATH)
        X = df[["search_volume", "avg_cpc", "engagement_rate"]].values
        y = (df["avg_sentiment"] > 0).astype(int).values
        return df, X, y
    return pd.DataFrame(), [], []


def main() -> None:
    df, X, y = load_training_matrix()
    with mlflow.start_run(run_name="daily_train"):
        conv = ConversionModel().fit(X, y)
        joblib.dump(conv, MODEL_DIR / "conversion_model.pkl")
        if conv.model is not None:
            mlflow.xgboost.log_model(conv.model, "conversion_model")

        prof = ProfitModel().fit(X, df.get("price", pd.Series(1.0, index=df.index)).values)
        joblib.dump(prof, MODEL_DIR / "profit_model.pkl")
        if prof.model is not None:
            mlflow.catboost.log_model(prof.model, "profit_model")

        rank = RankModel().fit(X, df["search_volume"].rank().values)
        joblib.dump(rank, MODEL_DIR / "rank_model.pkl")
        if rank.model is not None:
            mlflow.xgboost.log_model(rank.model, "rank_model")

        mlflow.log_metric("num_rows", len(X))



if __name__ == "__main__":
    main()

