from anthropic import Anthropic

from ai_lab.config import read_claude_api_key
from ai_lab.providers.provider import Provider
from ai_lab.providers.settings import CLAUDE_EFFORT, CLAUDE_MAX_TOKENS, CLAUDE_MODEL


class ClaudeProvider(Provider):
    """Claude implementation of the Provider interface."""

    def __init__(
        self,
        model: str = CLAUDE_MODEL,
        max_tokens: int = CLAUDE_MAX_TOKENS,
        effort: str | None = CLAUDE_EFFORT,
    ):
        self._client = Anthropic(api_key=read_claude_api_key())
        self._model = model
        self._max_tokens = max_tokens
        self._effort = effort

    @property
    def name(self) -> str:
        return "Claude"

    @property
    def model(self) -> str:
        return self._model

    def ask(self, prompt: str) -> str:
        request: dict[str, object] = {
            "model": self._model,
            "max_tokens": self._max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }

        if self._effort:
            request["output_config"] = {"effort": self._effort}

        response = self._client.messages.create(**request)

        parts: list[str] = []

        for block in response.content:
            if getattr(block, "type", None) == "text":
                parts.append(block.text)

        return "\n".join(parts).strip()
