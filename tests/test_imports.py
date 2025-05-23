from importlib import import_module

MODULES = [
    'aods.ingestion.keyword_api',
    'aods.analytics.anomaly',
    'aods.analytics.hypothesis',
    'aods.models.predictive',
    'aods.optimizer.portfolio',
    'aods.dashboard.api',
    'aods.orchestrator.dags',
    'aods.ingestion.exa_ai',
    'aods.ingestion.tavily',
    'aods.ingestion.apify_connector',
    'aods.ingestion.scrapeowl',
    'aods.storage.astra',
    'aods.dashboard.mcp_server',
]


def test_imports():
    for mod in MODULES:
        import_module(mod)
