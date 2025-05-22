from importlib import import_module

MODULES = [
    'aods.ingestion.keyword_api',
    'aods.analytics.anomaly',
    'aods.analytics.hypothesis',
    'aods.models.predictive',
    'aods.optimizer.portfolio',
    'aods.dashboard.api',
    'aods.orchestrator.dags',
]


def test_imports():
    for mod in MODULES:
        import_module(mod)
