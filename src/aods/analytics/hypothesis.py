"""Simple hypothesis generation placeholder."""

from typing import List, Dict

RULE_THRESHOLD = 0.1


def generate_hypotheses(records: List[Dict]) -> List[Dict]:

    """Generate opportunity hypotheses from diverse records."""
    hyps = []
    for rec in records:
        if rec.get("cpc", 1.0) < RULE_THRESHOLD:
            hyps.append({"type": "keyword", "id": rec.get("keyword"), "reason": "low cpc"})
        if rec.get("price") and rec.get("price") < 10:
            hyps.append({"type": "product", "id": rec.get("sku"), "reason": "cheap price"})
        if rec.get("engagement_rate") and rec.get("engagement_rate") > 0.15:
            hyps.append({"type": "trend", "id": rec.get("topic"), "reason": "viral topic"})

    return hyps
