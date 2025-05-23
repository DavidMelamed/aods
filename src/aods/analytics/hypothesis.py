"""Simple hypothesis generation placeholder."""

from typing import List, Dict

RULE_THRESHOLD = 0.1


def generate_hypotheses(records: List[Dict]) -> List[Dict]:
    """Generate opportunity hypotheses from records."""
    hyps = []
    for rec in records:
        if rec.get("cpc", 0) < RULE_THRESHOLD:
            hyps.append({"keyword": rec["keyword"], "reason": "low cpc"})
    return hyps
