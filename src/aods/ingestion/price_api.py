from .base import DataConnector
import random

class PriceAPIConnector(DataConnector):
    """Example connector for product pricing data."""

    def pull(self):
        skus = ["sku1", "sku2", "sku3"]
        return [{"sku": sku, "price": round(random.uniform(5.0, 20.0), 2)} for sku in skus]

    def parse(self, raw):
        return raw

