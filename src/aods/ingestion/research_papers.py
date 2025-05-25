from .base import DataConnector
import random


class ResearchPaperConnector(DataConnector):
    """Simulated connector for trending research papers."""

    def pull(self):
        titles = ["AI in Finance", "Quantum Trading", "DeFi Strategies"]
        return [{"title": t, "mentions": random.randint(0, 100)} for t in titles]

    def parse(self, raw):
        return raw

    def upsert(self, records):
        return super().upsert(records)

