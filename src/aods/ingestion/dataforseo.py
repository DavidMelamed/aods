"""Connectors for DataForSEO APIs."""

import logging
from .base import DataConnector

try:
    import requests
except Exception:  # pragma: no cover - optional dependency
    requests = None
    logging.warning("requests not available; DataForSEO connectors disabled")


class DataForSEOKeywordsConnector(DataConnector):
    """Retrieve keyword data from DataForSEO's Keywords Data API."""

    endpoint = "https://api.dataforseo.com/v3/keywords_data/google_ads/keywords_for_keywords"  # example

    def __init__(self, api_key: str = "demo", api_secret: str = "demo"):
        self.api_key = api_key
        self.api_secret = api_secret

    def pull(self):
        if requests is None:
            return []
        # This is a placeholder since network is disabled.
        # Normally would send a POST request with credentials.
        logging.info("Simulating DataForSEO keywords fetch")
        return [
            {"keyword": "ai tools", "search_volume": 1200, "cpc": 2.5},
            {"keyword": "cheap hosting", "search_volume": 950, "cpc": 1.2},
        ]

    def parse(self, raw):
        return raw


class DataForSEOSerpConnector(DataConnector):
    """Retrieve SERP results from DataForSEO SERP API."""

    endpoint = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"  # example

    def __init__(self, api_key: str = "demo", api_secret: str = "demo"):
        self.api_key = api_key
        self.api_secret = api_secret

    def pull(self):
        if requests is None:
            return []
        logging.info("Simulating DataForSEO SERP fetch")
        return [
            {"keyword": "ai tools", "position": 1, "title": "Best AI Tools"},
            {"keyword": "cheap hosting", "position": 2, "title": "Affordable Hosting"},
        ]

    def parse(self, raw):
        return raw
