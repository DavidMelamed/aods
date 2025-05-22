from .base import DataConnector
import random

class SocialTrendConnector(DataConnector):
    """Simulated social media trend metrics."""

    def pull(self):
        topics = ["AI", "ML", "Cloud", "Data"]
        return [
            {
                "platform": random.choice(["tw", "yt", "tt"]),
                "topic": t,
                "views": random.randint(1000, 100000),
                "engagement_rate": round(random.uniform(0.01, 0.2), 3),
            }
            for t in topics
        ]

    def parse(self, raw):
        return raw

    def upsert(self, records):
        return super().upsert(records)
