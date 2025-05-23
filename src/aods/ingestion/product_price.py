from .base import DataConnector
import random

class ProductPriceConnector(DataConnector):
    """Simulated connector for product pricing data."""

    def pull(self):
        products = ["widget", "gadget", "doohickey"]
        return [{"sku": p, "price": round(random.uniform(5.0, 20.0), 2),
                "shipping": round(random.uniform(1.0, 5.0), 2)} for p in products]

    def parse(self, raw):
        return raw
