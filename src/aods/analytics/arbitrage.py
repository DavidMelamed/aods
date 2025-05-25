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


def currency_triangular_arbitrage(rates: List[Dict]) -> List[Dict]:
    """Detect simple triangular arbitrage cycles among currency pairs."""
    pair_rate = {r["pair"]: r["rate"] for r in rates}
    currencies = set()
    for pair in pair_rate:
        a, b = pair.split("/")
        currencies.update([a, b])
    cycles = []
    cur_list = list(currencies)
    for i in range(len(cur_list)):
        for j in range(len(cur_list)):
            for k in range(len(cur_list)):
                a, b, c = cur_list[i], cur_list[j], cur_list[k]
                if len({a, b, c}) < 3:
                    continue
                r1 = pair_rate.get(f"{a}/{b}")
                r2 = pair_rate.get(f"{b}/{c}")
                r3 = pair_rate.get(f"{c}/{a}")
                if r1 and r2 and r3:
                    prod = r1 * r2 * r3
                    if prod > 1.001:
                        cycles.append({
                            "cycle": [f"{a}/{b}", f"{b}/{c}", f"{c}/{a}"],
                            "profit": prod - 1,
                        })
    return cycles
