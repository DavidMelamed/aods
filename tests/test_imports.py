from importlib import import_module
import os
import sys

root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if root not in sys.path:
    sys.path.insert(0, root)

MODULES = [
    'aods.ingestion.keyword_api',
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
