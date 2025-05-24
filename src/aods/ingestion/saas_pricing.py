from .base import DataConnector
import random

class SaaSPricingConnector(DataConnector):
    """Simulated SaaS pricing data."""

    def pull(self):
        plans = ["basic", "pro", "enterprise"]
        return [
            {
                "plan": p,
                "price": round(random.uniform(5.0, 200.0), 2),
                "users": random.randint(1, 100),
            }
            for p in plans
        ]

    def parse(self, raw):
        return raw

    def upsert(self, records):
        return super().upsert(records)
