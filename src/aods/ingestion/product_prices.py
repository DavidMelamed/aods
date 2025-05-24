from .base import DataConnector
import random

class ProductPriceConnector(DataConnector):
    """Simulated product pricing data."""

    def pull(self):
        skus = ["SKU1", "SKU2", "SKU3", "SKU4"]
        return [
            {
                "sku": sku,
                "site": random.choice(["A", "B", "C"]),
                "price": round(random.uniform(10.0, 100.0), 2),
                "shipping": round(random.uniform(0.0, 10.0), 2),
                "stock": random.randint(0, 100),
            }
            for sku in skus
        ]

    def parse(self, raw):
        return raw

    def upsert(self, records):
        return super().upsert(records)
