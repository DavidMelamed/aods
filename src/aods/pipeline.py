
"""End-to-end pipeline orchestrating ingestion, modelling and optimisation."""

from typing import List
import logging
from .ingestion import (
    KeywordAPIConnector,
    AdAuctionConnector,
    ProductPriceConnector,
    SocialTrendConnector,
    SaaSPricingConnector,
    MarketNewsConnector,
    ResearchPaperConnector,
)
from .analytics.hypothesis import generate_hypotheses
from .analytics.anomaly import detect_anomalies
from .analytics.cleaning import deduplicate_records
from .models.predictive import ConversionRateModel, ProfitModel
from .analytics.roi import compute_scores
from .optimizer.portfolio import optimise_portfolio


logging.basicConfig(level=logging.INFO)


class Pipeline:
    def __init__(self, budget: float = 100.0):
        self.connectors = [
            KeywordAPIConnector(),
            AdAuctionConnector(),
            ProductPriceConnector(),
            SocialTrendConnector(),
            SaaSPricingConnector(),
            MarketNewsConnector(),
            ResearchPaperConnector(),
        ]
        self.model = ConversionRateModel()
        self.profit_model = ProfitModel()
        self.budget = budget

    def run(self) -> List[dict]:
        records: List[dict] = []
        for c in self.connectors:
            raw = c.pull()
            parsed = c.parse(raw)
            records.extend(parsed)
        records = deduplicate_records(records)
        logging.info("pulled %d records", len(records))

        hyps = generate_hypotheses(records)
        logging.info("generated %d hypotheses", len(hyps))

        metrics = [r.get("cpc", 1.0) for r in records]
        detect_anomalies(metrics)  # side effect only

        X = [[r.get("search_volume", 1000), r.get("cpc", 1.0)] for r in records]
        y = [r.get("conv_rate", 0.05) for r in records]
        self.model.fit(X, y)
        preds = self.model.predict(X)
        profit_features = [[r.get("price", 1.0), r.get("cpc", 1.0)] for r in records]
        self.profit_model.fit(profit_features, [0.0 for _ in profit_features])
        profit_preds = self.profit_model.predict(profit_features)

        revenues = [p * 10 + prof for p, prof in zip(preds, profit_preds)]
        costs = [r.get("cpc", 1.0) for r in records]
        std_devs = [0.1 for _ in preds]
        scores = compute_scores(preds, revenues, costs, std_devs)

        selected_idx = optimise_portfolio(scores, costs, self.budget)
        opps = [records[i] for i in selected_idx]
        for i, op in zip(selected_idx, opps):
            op["score"] = scores[i]
        return opps


def main():
    pipe = Pipeline()
    opps = pipe.run()
    for o in opps:
        print(o)


if __name__ == "__main__":
    main()

