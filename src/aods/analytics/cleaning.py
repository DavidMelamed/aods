"""Simple record cleaning utilities."""

from typing import List, Dict, Sequence, Any


def deduplicate_records(records: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove exact duplicate records."""
    seen = set()
    result: List[Dict[str, Any]] = []
    for rec in records:
        key = tuple(sorted(rec.items()))
        if key not in seen:
            seen.add(key)
            result.append(rec)
    return result


def fill_missing(records: List[Dict[str, Any]], field: str, default: Any) -> List[Dict[str, Any]]:
    """Fill missing field value in-place and return records."""
    for rec in records:
        rec.setdefault(field, default)
    return records

