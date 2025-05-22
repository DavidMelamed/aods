class DataConnector:
    """Base interface for data connectors."""

    def pull(self):
        """Retrieve raw data from the source."""
        raise NotImplementedError

    def parse(self, raw):
        """Parse raw payload into structured records."""
        raise NotImplementedError

    def upsert(self, records):
        """Upsert records into storage (placeholder)."""
        # In a real implementation, this would write to a DB or file system
        return records
