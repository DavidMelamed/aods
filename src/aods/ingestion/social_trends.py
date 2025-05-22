from .base import DataConnector
import random

class SocialTrendConnector(DataConnector):
    """Simulated connector for social trend metrics."""

    def pull(self):
        topics = ["AI", "Crypto", "Gaming"]
        return [{"topic": t, "views": random.randint(1000, 10000),
                "engagement_rate": round(random.uniform(0.01, 0.2), 3)} for t in topics]

    def parse(self, raw):
        return raw
