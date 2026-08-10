from anthropic import Anthropic

from ai_lab.config import read_claude_api_key
from ai_lab.providers.provider import Provider, ProviderOutcome
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
        return self.ask_with_outcome(prompt).text

    def ask_with_outcome(self, prompt: str) -> ProviderOutcome:
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
        block_types: list[str] = []

        for block in response.content:
            block_type = getattr(block, "type", None)
            block_types.append(str(block_type))
            if block_type == "text":
                parts.append(block.text)

        usage = getattr(response, "usage", None)
        stop_reason = getattr(response, "stop_reason", None)

        return ProviderOutcome(
            text="\n".join(parts).strip(),
            stop_reason=str(stop_reason) if stop_reason is not None else None,
            stop_reason_field="stop_reason",
            input_tokens=getattr(usage, "input_tokens", None),
            output_tokens=getattr(usage, "output_tokens", None),
            content_block_types=block_types,
        )
