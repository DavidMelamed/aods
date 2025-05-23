from .base import DataConnector
import logging

try:
    import tavily
except Exception:  # pragma: no cover - optional
    tavily = None
    logging.warning("tavily library not available; TavilyConnector inactive")


class TavilyConnector(DataConnector):
    """Connector for the Tavily data API."""

    def pull(self):
        if tavily is None:
            return []
        # Placeholder: fetch trending topics
        return tavily.get_trending()

    def parse(self, raw):
        return raw
