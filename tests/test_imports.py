from importlib import import_module

MODULES = [
    'aods.ingestion.keyword_api',
    'aods.ingestion.dataforseo',
    'aods.ingestion.crypto_exchange',
    'aods.ingestion.gift_card_market',
    'aods.analytics.arbitrage',
    'aods.ingestion.product_price',
    'aods.ingestion.social_trends',
    'aods.analytics.anomaly',
    'aods.analytics.hypothesis',
    'aods.analytics.roi',
    'aods.models.predictive',
    'aods.optimizer.portfolio',
    'aods.dashboard.api',
    'aods.orchestrator.dags',
    'aods.pipeline',
    'aods.visualization.plots',
]


def test_imports():
    for mod in MODULES:
        import_module(mod)

