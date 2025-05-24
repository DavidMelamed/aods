from importlib import import_module

MODULES = [
    'aods.ingestion.keyword_api',
    'aods.ingestion.ad_auction',
    'aods.ingestion.product_prices',
    'aods.ingestion.social_trends',
    'aods.ingestion.saas_pricing',
    'aods.ingestion.dataforseo',
    'aods.ingestion.crypto_exchange',
    'aods.ingestion.gift_card_market',
    'aods.ingestion.price_api',
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
import os
import sys

root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if root not in sys.path:
    sys.path.insert(0, root)


def test_imports():
    for mod in MODULES:
        import_module(mod)
