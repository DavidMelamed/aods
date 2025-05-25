

"""Autonomous Opportunity Discovery System."""

from .pipeline import Pipeline
from .agents import IdeaAgent


def run() -> list[dict]:
    """Execute the default pipeline and return opportunities."""
    pipe = Pipeline()
    return pipe.run()


__all__ = ["Pipeline", "run", "IdeaAgent"]

