from importlib import import_module

MODULES = [
    'aods.ingestion.keyword_api',
    'aods.ingestion.ad_auction',
    'aods.ingestion.product_prices',
    'aods.ingestion.social_trends',
    'aods.ingestion.saas_pricing',
    'aods.analytics.anomaly',
    'aods.analytics.hypothesis',
    'aods.analytics.roi',
    'aods.models.predictive',
    'aods.optimizer.portfolio',
    'aods.dashboard.api',
    'aods.orchestrator.dags',
]


def test_imports():
    for mod in MODULES:
        import_module(mod)
