"""Generate new arbitrage ideas using a language model."""

try:
    from pydantic import BaseModel
except Exception:  # pragma: no cover - optional dependency
    BaseModel = object  # type: ignore

try:
    import openai
except Exception:  # pragma: no cover - optional dependency
    openai = None


class IdeaAgent(BaseModel):
    """LLM-driven agent for brainstorming opportunities."""

    model: str = "gpt-4o"

    def generate_ideas(self, prompt: str) -> str:
        """Return ideas from the configured LLM."""
        if openai is None:
            raise RuntimeError("openai package is required for idea generation")
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp["choices"][0]["message"]["content"]
