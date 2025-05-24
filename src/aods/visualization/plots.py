
try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - optional dependency
    plt = None
from typing import Sequence


def scatter_roi_vs_cost(scores: Sequence[float], costs: Sequence[float]):
    if plt is None:
        raise RuntimeError("matplotlib is required for plotting")

    plt.scatter(costs, scores)
    plt.xlabel("Cost")
    plt.ylabel("Score")
    plt.title("Opportunity Score vs Cost")
    plt.grid(True)
    return plt
