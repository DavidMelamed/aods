"""Utilities for identifying cross-market arbitrage."""

from typing import List, Dict


def price_arbitrage_opportunities(records: List[Dict], key_field: str, price_field: str,
                                  source_field: str) -> List[Dict]:
    """Identify price differences for the same item across sources."""
    opportunities = []
    by_key = {}
    for rec in records:
        key = rec[key_field]
        by_key.setdefault(key, []).append(rec)
    for key, rows in by_key.items():
        if len(rows) < 2:
            continue
        rows = sorted(rows, key=lambda r: r[price_field])
        low, high = rows[0], rows[-1]
        diff = high[price_field] - low[price_field]
        if diff > 0:
            opportunities.append({
                key_field: key,
                "buy_from": low[source_field],
                "sell_to": high[source_field],
                "spread": diff,
            })
    return opportunities
