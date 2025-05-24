
"""ROI and risk computation utilities."""

from typing import Iterable, List
from typing import Sequence
import math


def expected_value(p_success: float, revenue: float, cost: float) -> float:

    """Compute expected value."""
    return p_success * (revenue - cost) - (1 - p_success) * cost


def risk_adjusted_return(ev: float, volatility: float) -> float:
    if volatility == 0:
        return ev
    return ev / volatility


def score_opportunity(p_success: float, revenue: float, cost: float, volatility: float, payback_months: float, payback_weight: float = 1.0) -> float:
    ev = expected_value(p_success, revenue, cost)
    rar = risk_adjusted_return(ev, volatility)
    return rar * (payback_weight / max(payback_months, 1e-6))
