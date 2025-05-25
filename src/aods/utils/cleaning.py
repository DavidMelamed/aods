"""Basic record cleaning utilities."""

from typing import List, Dict


def deduplicate(records: List[Dict]) -> List[Dict]:
    """Remove duplicate dictionary records."""
    seen = set()
    unique = []
    for rec in records:
        key = tuple(sorted(rec.items()))
        if key not in seen:
            seen.add(key)
            unique.append(rec)
    return unique


def fill_missing(records: List[Dict], defaults: Dict) -> List[Dict]:
    """Fill missing keys in each record with defaults."""
    return [{**defaults, **rec} for rec in records]
