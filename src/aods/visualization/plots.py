"""Visualization helpers using matplotlib if available."""

from typing import Sequence

try:
    import matplotlib.pyplot as plt  # type: ignore
except Exception:  # matplotlib may be missing
    plt = None


def scatter_roi_vs_cost(scores: Sequence[float], costs: Sequence[float]):
    if plt is None:
        raise ImportError("matplotlib not installed")
    plt.scatter(costs, scores)
    plt.xlabel("Cost")
    plt.ylabel("Score")
    plt.title("Opportunity Score vs Cost")
    plt.grid(True)
    return plt
