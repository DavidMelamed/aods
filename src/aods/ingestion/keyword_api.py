from .base import DataConnector
import random

class KeywordAPIConnector(DataConnector):
    """Example connector for keyword volume/cpc data."""

    def pull(self):
        # Placeholder: simulate API results
        keywords = ["ai", "ml", "cloud", "data"]
        return [{"keyword": kw, "search_volume": random.randint(1000, 5000),
                "cpc": round(random.uniform(0.5, 5.0), 2)} for kw in keywords]

    def parse(self, raw):
        # In a real implementation, transform raw API payload
        return raw

    def upsert(self, records):
        # No-op: return parsed records
        return super().upsert(records)
