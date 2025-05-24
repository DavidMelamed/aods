from importlib import import_module

MODULES = [
    'aods.ingestion.keyword_api',
    'aods.ingestion.ad_auction',
    'aods.ingestion.product_prices',
    'aods.ingestion.product_price',
    'aods.ingestion.social_trends',
    'aods.ingestion.saas_pricing',
    'aods.ingestion.dataforseo',
    'aods.ingestion.crypto_exchange',
    'aods.ingestion.gift_card_market',
    'aods.ingestion.price_api',
    'aods.ingestion.exa_ai',
    'aods.ingestion.tavily',
    'aods.ingestion.apify_connector',
    'aods.ingestion.scrapeowl',
    'aods.ingestion.market_news',
    'aods.ingestion.research_papers',
    'aods.analytics.anomaly',
    'aods.analytics.hypothesis',
    'aods.analytics.arbitrage',
    'aods.analytics.cleaning',
    'aods.analytics.roi',
    'aods.models.predictive',
    'aods.optimizer.portfolio',
    'aods.dashboard.api',
    'aods.dashboard.mcp_server',
    'aods.orchestrator.dags',
    'aods.storage.astra',
    'aods.pipeline',
    'aods.visualization.plots',
]

def test_imports():
    for mod in MODULES:
        import_module(mod)
