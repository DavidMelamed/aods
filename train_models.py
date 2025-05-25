import mlflow
import pandas as pd
from aods.features.build_features import FEATURE_PATH
from aods.models import ConversionModel, ProfitModel

mlflow.set_tracking_uri("http://mlflow:5000")


def load_training_matrix():
    if FEATURE_PATH.exists():
        df = pd.read_parquet(FEATURE_PATH)
        X = df[['search_volume', 'avg_cpc', 'engagement_rate']].values
        y = (df['avg_sentiment'] > 0).astype(int).values
        return X, y
    return [], []


def main() -> None:
    with mlflow.start_run(run_name="daily_train"):
        X, y = load_training_matrix()
        clf = ConversionModel()
        clf.fit(X, y)
        mlflow.xgboost.log_model(clf.model, "conversion_model")
        mlflow.log_metric("num_rows", len(X))


if __name__ == "__main__":
    main()
