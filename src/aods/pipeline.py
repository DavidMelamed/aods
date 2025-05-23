"""Simple pipeline that pulls data, detects anomalies, trains a model and optimises opportunities."""

from .ingestion.keyword_api import KeywordAPIConnector
from .analytics.anomaly import detect_anomalies
from .analytics.hypothesis import generate_hypotheses
from .models.predictive import ConversionRateModel
from .optimizer.portfolio import optimise_portfolio


def run_pipeline(budget: float = 10.0):
    connector = KeywordAPIConnector()
    raw = connector.pull()
    records = connector.parse(raw)

    anomalies = detect_anomalies([r["cpc"] for r in records])
    hyps = generate_hypotheses(records)

    # simple features using search volume and anomaly score
    X = [[r["search_volume"], a] for r, a in zip(records, anomalies)]
    y = [1.0 for _ in records]  # dummy target

    model = ConversionRateModel()
    model.fit(X, y)
    preds = model.predict(X)

    costs = [r["cpc"] for r in records]
    selected_idx = optimise_portfolio(preds, costs, budget)
    selected = [records[i] for i in selected_idx]
    return {
        "records": records,
        "hypotheses": hyps,
        "predictions": preds,
        "selected": selected,
    }


if __name__ == "__main__":
    result = run_pipeline()
    for item in result["selected"]:
        print(item)
