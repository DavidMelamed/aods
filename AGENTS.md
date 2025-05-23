# Repository Guidelines

- Run `python -m pytest -q` after every change and include the results in the PR description.
- If dependencies like `pytest`, `lightgbm`, or `matplotlib` are missing, the code should handle the ImportError gracefully with fallbacks.
- Keep commits small and descriptive.
- Summarize notable additions and test results in PR messages.
