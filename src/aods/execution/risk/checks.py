"""Risk checks for executions."""
from __future__ import annotations


class RiskViolation(Exception):
    pass


def within_daily_budget(amount: float) -> None:
    if amount > 1000:
        raise RiskViolation('daily budget exceeded')


def volatility_ok(vol: float) -> None:
    if vol > 0.5:
        raise RiskViolation('volatility too high')
