from openai import OpenAI

from ai_lab.config import read_api_key
from ai_lab.providers.provider import Provider, ProviderOutcome
from ai_lab.providers.settings import OPENAI_MODEL, OPENAI_REASONING_EFFORT


class OpenAIProvider(Provider):
    """OpenAI implementation of the Provider interface."""

    def __init__(
        self,
        model: str = OPENAI_MODEL,
        reasoning_effort: str | None = OPENAI_REASONING_EFFORT,
    ):
        self._client = OpenAI(api_key=read_api_key())
        self._model = model
        self._reasoning_effort = reasoning_effort

    @property
    def name(self) -> str:
        return "OpenAI"

    @property
    def model(self) -> str:
        return self._model

    def ask(self, prompt: str) -> str:
        return self.ask_with_outcome(prompt).text

    def ask_with_outcome(self, prompt: str) -> ProviderOutcome:
        request: dict[str, object] = {
            "model": self._model,
            "input": prompt,
        }

        if self._reasoning_effort:
            request["reasoning"] = {"effort": self._reasoning_effort}

        response = self._client.responses.create(**request)

        # The Responses API reports status, and incomplete_details.reason when
        # a call ended early. Anthropic reports stop_reason. The two are not
        # normalised onto a shared vocabulary here: stop_reason_field records
        # which field the value came from and the value is the provider's own.
        status = getattr(response, "status", None)
        details = getattr(response, "incomplete_details", None)
        detail_reason = getattr(details, "reason", None) if details else None
        if detail_reason is not None:
            stop_reason, stop_reason_field = str(detail_reason), "incomplete_details.reason"
        elif status is not None:
            stop_reason, stop_reason_field = str(status), "status"
        else:
            stop_reason, stop_reason_field = None, None

        usage = getattr(response, "usage", None)

        block_types: list[str] = []
        for item in getattr(response, "output", None) or []:
            item_type = getattr(item, "type", None)
            block_types.append(str(item_type))

        return ProviderOutcome(
            text=response.output_text,
            stop_reason=stop_reason,
            stop_reason_field=stop_reason_field,
            input_tokens=getattr(usage, "input_tokens", None),
            output_tokens=getattr(usage, "output_tokens", None),
            content_block_types=block_types,
        )
