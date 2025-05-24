from .base import DataConnector
import random

class AdAuctionConnector(DataConnector):
    """Simulated ad auction metrics."""

    def pull(self):
        keywords = ["ai", "ml", "cloud", "data"]
        return [
            {
                "keyword": kw,
                "avg_cpc": round(random.uniform(0.3, 6.0), 2),
                "ctr": round(random.uniform(0.01, 0.2), 3),
                "conv_rate": round(random.uniform(0.01, 0.1), 3),
            }
            for kw in keywords
        ]

    def parse(self, raw):
        return raw

    def upsert(self, records):
        return super().upsert(records)
