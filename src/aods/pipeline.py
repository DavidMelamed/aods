
"""Simple pipeline runner orchestrating connectors and analytics."""

from aods.ingestion.keyword_api import KeywordAPIConnector
from aods.ingestion.product_price import ProductPriceConnector
from aods.ingestion.social_trends import SocialTrendConnector
from aods.ingestion.dataforseo import DataForSEOKeywordsConnector, DataForSEOSerpConnector
from aods.ingestion.crypto_exchange import CryptoExchangeConnector
from aods.ingestion.gift_card_market import GiftCardMarketConnector
from aods.analytics.hypothesis import generate_hypotheses
from aods.analytics.anomaly import detect_anomalies
from aods.analytics.roi import score_opportunity
from aods.analytics.arbitrage import price_arbitrage_opportunities
from aods.models.predictive import ConversionRateModel
from aods.optimizer.portfolio import optimise_portfolio


def run():
    # Pull data from connectors
    connectors = [
        KeywordAPIConnector(),
        DataForSEOKeywordsConnector(),
        DataForSEOSerpConnector(),
        CryptoExchangeConnector(),
        GiftCardMarketConnector(),
    ]
    all_records = []
    for c in connectors:
        raw = c.pull()
        parsed = c.parse(raw)
        all_records.extend(parsed)

    # For keyword-type records, generate hypotheses
    keyword_records = [r for r in all_records if r.get("keyword")]
    hyps = generate_hypotheses(keyword_records)

    # Basic anomaly scores on search volume or price if present
    volumes = [r.get("search_volume", r.get("price", 0)) for r in keyword_records]
    scores = detect_anomalies(volumes)

    # Basic model: train on dummy data
    model = ConversionRateModel()
    model.fit([[r.get("search_volume", 0)] for r in keyword_records], scores)
    preds = model.predict([[r.get("search_volume", 0)] for r in keyword_records])

    # Portfolio selection using costs if available or 1
    costs = [r.get("cpc", 1.0) for r in keyword_records]
    selected_idx = optimise_portfolio(preds, costs, budget=5.0)
    selected = [keyword_records[i] for i in selected_idx]

    # Identify crypto arbitrage
    crypto_records = [r for r in all_records if r.get("asset")]
    crypto_ops = price_arbitrage_opportunities(crypto_records, "asset", "price", "exchange")

    # Show results
    print("Keyword opportunities:", selected)
    print("Crypto arbitrage:", crypto_ops)


if __name__ == "__main__":
    run()
=======
"""End-to-end pipeline runner for the AODS example."""

import random


def run():
    connectors = [KeywordAPIConnector(), ProductPriceConnector(), SocialTrendConnector()]
    all_records = []
    for conn in connectors:
        raw = conn.pull()
        parsed = conn.parse(raw)
        all_records.extend(parsed)

    # Simple numeric metric for anomaly detection
    metrics = [r.get("search_volume", r.get("views", r.get("price", 0))) for r in all_records]
    scores = detect_anomalies(metrics)

    hyps = generate_hypotheses([{**r, "score": s} for r, s in zip(all_records, scores)])

    # Fake features and target for model training
    model = ConversionRateModel()
    X = [[random.random()] for _ in hyps]
    y = [random.random() for _ in hyps]
    model.fit(X, y)
    p_success = model.predict(X)

    costs = [random.uniform(1.0, 10.0) for _ in hyps]
    revenues = [random.uniform(5.0, 20.0) for _ in hyps]
    vols = [random.uniform(0.5, 2.0) for _ in hyps]
    scores = [
        score_opportunity(p, rev, cost, vol, payback_months=6)
        for p, rev, cost, vol in zip(p_success, revenues, costs, vols)
    ]

    selected = optimise_portfolio(scores, costs, budget=15.0)
    opportunities = [hyps[i] | {"score": scores[i], "cost": costs[i]} for i in selected]
    return opportunities


if __name__ == "__main__":
    ops = run()
    for op in ops:
        print(op)

