
Repository Guidelines
=====================

- After making changes, run `python -m pytest -q` and record whether it succeeds or fails in the PR description.
- If dependencies are missing and tests cannot run, note the failure but continue.
- Keep commits concise with clear messages.
- Summaries in PRs should mention key files changed and highlight any new features or modules.


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

