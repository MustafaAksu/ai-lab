from openai import OpenAI

from ai_lab.config import read_api_key
from ai_lab.providers.provider import Provider
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
        request: dict[str, object] = {
            "model": self._model,
            "input": prompt,
        }

        if self._reasoning_effort:
            request["reasoning"] = {"effort": self._reasoning_effort}

        response = self._client.responses.create(**request)
        return response.output_text
