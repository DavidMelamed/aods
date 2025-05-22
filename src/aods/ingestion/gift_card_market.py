"""Connector for gift card market prices (simulated)."""

import random
from .base import DataConnector

class GiftCardMarketConnector(DataConnector):
    def pull(self):
        # Simulate gift card buy/sell rates
        return [
            {"brand": "StoreA", "buy_rate": 0.92, "sell_rate": 0.95},
            {"brand": "StoreB", "buy_rate": 0.88, "sell_rate": 0.9},
            {"brand": "StoreC", "buy_rate": 0.8, "sell_rate": 0.83},
        ]

    def parse(self, raw):
        return raw
