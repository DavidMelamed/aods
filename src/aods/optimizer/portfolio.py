
"""Portfolio optimizer using OR-Tools if available."""

import logging
from typing import List

try:
    from ortools.linear_solver import pywraplp
except Exception:  # pragma: no cover - optional
    pywraplp = None


    logging.warning("OR-Tools not available; using greedy fallback")



def optimise_portfolio(
    scores: List[float],
    costs: List[float],
    budget: float,
    channels: List[str] | None = None,
    max_per_channel: int | None = None,
    risk_caps: List[float] | None = None,
) -> List[int]:
    """Select opportunities under budget with optional diversity cap."""
    n = len(scores)
    if pywraplp is None:
        order = sorted(range(n), key=lambda i: scores[i] / (costs[i] or 1), reverse=True)
        selected = []
        spent = 0.0
        for i in order:
            if spent + costs[i] <= budget:
                selected.append(i)
                spent += costs[i]
        return selected

    solver = pywraplp.Solver.CreateSolver('CBC')
    x = [solver.IntVar(0, 1, f'x{i}') for i in range(n)]
    solver.Add(sum(costs[i]*x[i] for i in range(n)) <= budget)
    if risk_caps:
        for i, cap in enumerate(risk_caps):
            solver.Add(costs[i] * x[i] <= cap * budget)
    if channels is not None and max_per_channel:
        uniq = set(channels)
        for ch in uniq:
            idx = [i for i, c in enumerate(channels) if c == ch]
            solver.Add(sum(x[i] for i in idx) <= max_per_channel)
    solver.Maximize(solver.Sum(scores[i]*x[i] for i in range(n)))
    if solver.Solve() == pywraplp.Solver.OPTIMAL:
        return [i for i in range(n) if x[i].solution_value() > 0.5]
    return []
