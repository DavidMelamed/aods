from .base import DataConnector
import random


class MarketNewsConnector(DataConnector):
    """Simulated connector for market news sentiment."""

    def pull(self):
        topics = ["AI", "crypto", "retail", "energy"]
        return [{"topic": t, "sentiment": random.uniform(-1, 1)} for t in topics]

    def parse(self, raw):
        return raw

    def upsert(self, records):
        return super().upsert(records)

