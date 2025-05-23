
# Repository Guidelines

- Run `python -m pytest -q` after every change and include the results in the PR description.
- If dependencies like `pytest`, `lightgbm`, or `matplotlib` are missing, the code should handle the ImportError gracefully with fallbacks.
- Keep commits small and descriptive.
- Summarize notable additions and test results in PR messages.

# Agent Instructions

## Scope
These instructions apply to the entire repository.

## Required Checks
- After modifying code or documentation, run `python -m pytest -q` from the repo root.
- Include the output of the tests in the PR description's Testing section.
- If tests fail because dependencies are missing (e.g., pytest), note the failure output.

## Coding Guidelines
- Keep modules lightweight and handle optional dependencies with `try`/`except`.
- Provide concise docstrings for public functions and classes.
- Prefer simple, readable implementations over complex one-liners.

## Commit Messages
- Use short, imperative summaries (<= 50 characters) followed by an empty line and descriptive body if needed.

## Pull Request Notes
- Summarize key changes referencing file paths with line numbers.
- Mention test results with the exact command output.
