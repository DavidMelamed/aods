"""Connectors for DataForSEO APIs."""

from __future__ import annotations

import os
import logging
from typing import Iterable
from .base import DataConnector

try:
    import requests
except Exception:  # pragma: no cover - optional dependency
    requests = None
    logging.warning("requests not available; DataForSEO connectors disabled")


class DataForSEOKeywordsConnector(DataConnector):
    """Retrieve keyword data from DataForSEO's Keywords Data API."""

    endpoint = "https://api.dataforseo.com/v3/keywords_data/google_ads/keywords_for_keywords"  # example

    def __init__(self, api_key: str | None = None, api_secret: str | None = None):
        self.api_key = api_key or os.getenv("DATAFORSEO_KEY")
        self.api_secret = api_secret or os.getenv("DATAFORSEO_SECRET")

    def pull(self) -> Iterable:
        if requests is None or not (self.api_key and self.api_secret):
            logging.error("DataForSEO credentials not configured")
            return []
        try:
            resp = requests.post(
                self.endpoint,
                auth=(self.api_key, self.api_secret),
                json={"keywords": ["ai", "cloud"]},
                timeout=10,
            )
            resp.raise_for_status()
            return resp.json().get("tasks", [])
        except Exception as exc:  # pragma: no cover - network errors
            logging.error("DataForSEO keywords fetch failed: %s", exc)
            return []

    def parse(self, raw: Iterable) -> list[dict]:
        return [dict(r) for r in raw]


class DataForSEOSerpConnector(DataConnector):
    """Retrieve SERP results from DataForSEO SERP API."""

    endpoint = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"  # example

    def __init__(self, api_key: str | None = None, api_secret: str | None = None):
        self.api_key = api_key or os.getenv("DATAFORSEO_KEY")
        self.api_secret = api_secret or os.getenv("DATAFORSEO_SECRET")

    def pull(self) -> Iterable:
        if requests is None or not (self.api_key and self.api_secret):
            logging.error("DataForSEO credentials not configured")
            return []
        try:
            resp = requests.post(
                self.endpoint,
                auth=(self.api_key, self.api_secret),
                json={"keywords": ["ai"]},
                timeout=10,
            )
            resp.raise_for_status()
            return resp.json().get("tasks", [])
        except Exception as exc:  # pragma: no cover - network errors
            logging.error("DataForSEO SERP fetch failed: %s", exc)
            return []

    def parse(self, raw: Iterable) -> list[dict]:
        return [dict(r) for r in raw]
