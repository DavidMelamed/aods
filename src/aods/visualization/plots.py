"""Visualization helpers using matplotlib."""

import matplotlib.pyplot as plt
from typing import Sequence


def scatter_roi_vs_cost(scores: Sequence[float], costs: Sequence[float]):
    plt.scatter(costs, scores)
    plt.xlabel("Cost")
    plt.ylabel("Score")
    plt.title("Opportunity Score vs Cost")
    plt.grid(True)
    return plt
