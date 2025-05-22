"""ROI and risk computation utilities."""

from typing import Iterable, List
import math


def expected_value(p_success: float, revenue: float, cost: float) -> float:
    return p_success * (revenue - cost) - (1 - p_success) * cost


def risk_adjusted_return(ev: float, std_dev: float) -> float:
    if std_dev == 0:
        return ev
    return ev / std_dev


def compute_scores(ps: Iterable[float], revs: Iterable[float], costs: Iterable[float], std_devs: Iterable[float]) -> List[float]:
    scores = []
    for p, r, c, s in zip(ps, revs, costs, std_devs):
        ev = expected_value(p, r, c)
        rar = risk_adjusted_return(ev, s)
        scores.append(rar)
    return scores
