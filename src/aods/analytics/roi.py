
"""ROI and risk computation utilities."""

from typing import Iterable, List, Sequence
import math


def expected_value(p_success: float, revenue: float, cost: float) -> float:
    """Compute expected value of an opportunity."""
    return p_success * (revenue - cost) - (1 - p_success) * cost


def risk_adjusted_return(ev: float, volatility: float) -> float:
    if volatility == 0:
        return ev
    return ev / volatility


def score_opportunity(p_success: float, revenue: float, cost: float, volatility: float, payback_months: float, payback_weight: float = 1.0) -> float:
    ev = expected_value(p_success, revenue, cost)
    rar = risk_adjusted_return(ev, volatility)
    return rar * (payback_weight / max(payback_months, 1e-6))


def compute_scores(p_success: Sequence[float], revenue: Sequence[float], cost: Sequence[float], volatility: Sequence[float], payback_months: float = 3.0, payback_weight: float = 1.0) -> List[float]:
    """Compute scores for multiple opportunities."""
    scores: List[float] = []
    for p, rev, c, vol in zip(p_success, revenue, cost, volatility):
        scores.append(score_opportunity(p, rev, c, vol, payback_months, payback_weight))
    return scores
