from openai import OpenAI

from ai_lab.config import read_api_key
from ai_lab.providers.provider import Provider
from ai_lab.providers.settings import OPENAI_MODEL


class OpenAIProvider(Provider):
    """OpenAI implementation of the Provider interface."""

    def __init__(self, model: str = OPENAI_MODEL):
        self._client = OpenAI(api_key=read_api_key())
        self._model = model

    @property
    def name(self) -> str:
        return "OpenAI"

    @property
    def model(self) -> str:
        return self._model

    def ask(self, prompt: str) -> str:
        response = self._client.responses.create(
            model=self._model,
            input=prompt,
        )
        return response.output_text
