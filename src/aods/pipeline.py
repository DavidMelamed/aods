"""Simple pipeline runner pulling data, modelling and optimising."""

from typing import List, Dict
from .ingestion.keyword_api import KeywordAPIConnector
from .analytics.anomaly import detect_anomalies
from .analytics.hypothesis import generate_hypotheses
from .models.predictive import ConversionRateModel
from .optimizer.portfolio import optimise_portfolio


def run_pipeline() -> List[Dict]:
    connector = KeywordAPIConnector()
    records = connector.parse(connector.pull())

    # anomaly scores
    cpcs = [r.get("cpc", 0.0) for r in records]
    scores = detect_anomalies(cpcs)
    for rec, sc in zip(records, scores):
        rec["anomaly"] = sc

    # hypotheses
    hyps = generate_hypotheses(records)

    # simple synthetic labels: high anomaly -> positive conversion
    X = [[r["search_volume"], r["cpc"]] for r in records]
    y = [1 if r["cpc"] < 2 else 0 for r in records]
    model = ConversionRateModel().fit(X, y)
    preds = model.predict(X)

    costs = [r["cpc"] for r in records]
    roi_scores = [p * r["search_volume"] - c for p, r, c in zip(preds, records, costs)]

    selected_idx = optimise_portfolio(roi_scores, costs, budget=10.0)
    selected = [records[i] for i in selected_idx]
    for rec in selected:
        rec["pred_conv"] = preds[records.index(rec)]
    return selected


if __name__ == "__main__":
    results = run_pipeline()
    for r in results:
        print(r)
