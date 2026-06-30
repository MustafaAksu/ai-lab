from anthropic import Anthropic

from ai_lab.config import read_claude_api_key
from ai_lab.providers.provider import Provider


class ClaudeProvider(Provider):
    """Claude implementation of the Provider interface."""

    def __init__(self, model: str = "claude-sonnet-4-5"):
        self._client = Anthropic(api_key=read_claude_api_key())
        self._model = model

    @property
    def name(self) -> str:
        return "Claude"

    def ask(self, prompt: str) -> str:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        parts: list[str] = []

        for block in response.content:
            if getattr(block, "type", None) == "text":
                parts.append(block.text)

        return "\n".join(parts).strip()
