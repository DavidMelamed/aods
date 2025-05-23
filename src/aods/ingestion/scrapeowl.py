from .base import DataConnector
import logging

try:
    import scrapeowl
except Exception:  # pragma: no cover - optional
    scrapeowl = None
    logging.warning("scrapeowl not available; ScrapeOwlConnector inactive")


class ScrapeOwlConnector(DataConnector):
    """Connector for ScrapeOwl scraping API."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def pull(self):
        if scrapeowl is None or not self.api_key:
            return []
        return scrapeowl.get("https://example.com", self.api_key)

    def parse(self, raw):
        return raw
