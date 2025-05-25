
"""Portfolio optimizer using OR-Tools if available."""

import logging
from typing import List

try:
    from ortools.linear_solver import pywraplp
except Exception:  # pragma: no cover - optional
    pywraplp = None


    logging.warning("OR-Tools not available; using dynamic-programming fallback")


def _dp_knapsack(scores: List[float], costs: List[float], budget: float) -> List[int]:
    n = len(scores)
    B = int(budget)
    dp = [[0.0]*(B+1) for _ in range(n+1)]
    keep = [[False]*(B+1) for _ in range(n)]
    for i in range(1, n+1):
        c = int(costs[i-1])
        s = scores[i-1]
        for b in range(B+1):
            if c <= b and dp[i-1][b-c] + s > dp[i-1][b]:
                dp[i][b] = dp[i-1][b-c] + s
                keep[i-1][b] = True
            else:
                dp[i][b] = dp[i-1][b]
    b = B
    selected = []
    for i in range(n, 0, -1):
        if keep[i-1][b]:
            selected.append(i-1)
            b -= int(costs[i-1])
    return list(reversed(selected))



def optimise_portfolio(scores: List[float], costs: List[float], budget: float) -> List[int]:
    """Select opportunities under budget."""
    n = len(scores)
    if pywraplp is None:

        try:
            return _dp_knapsack(scores, costs, budget)
        except Exception:
            logging.exception("DP solver failed; using greedy fallback")
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
    solver.Maximize(solver.Sum(scores[i]*x[i] for i in range(n)))
    if solver.Solve() == pywraplp.Solver.OPTIMAL:
        return [i for i in range(n) if x[i].solution_value() > 0.5]
    return []
