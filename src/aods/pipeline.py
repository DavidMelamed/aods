"""Simple pipeline runner orchestrating connectors and analytics."""

from aods.ingestion.keyword_api import KeywordAPIConnector
from aods.ingestion.dataforseo import DataForSEOKeywordsConnector, DataForSEOSerpConnector
from aods.ingestion.crypto_exchange import CryptoExchangeConnector
from aods.ingestion.gift_card_market import GiftCardMarketConnector
from aods.analytics.hypothesis import generate_hypotheses
from aods.analytics.anomaly import detect_anomalies
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
