"""Connector for crypto exchange prices (simulated)."""

import random
from .base import DataConnector

class CryptoExchangeConnector(DataConnector):
    def pull(self):
        # Simulate pulling prices for BTC and ETH from two exchanges
        return [
            {"asset": "BTC", "exchange": "A", "price": random.uniform(28000, 30000)},
            {"asset": "BTC", "exchange": "B", "price": random.uniform(27900, 30100)},
            {"asset": "ETH", "exchange": "A", "price": random.uniform(1800, 1900)},
            {"asset": "ETH", "exchange": "B", "price": random.uniform(1790, 1910)},
        ]

    def parse(self, raw):
        return raw
