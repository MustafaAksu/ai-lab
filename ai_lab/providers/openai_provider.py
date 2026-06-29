from openai import OpenAI

from ai_lab.config import read_api_key
from ai_lab.providers.provider import Provider


class OpenAIProvider(Provider):
    """OpenAI implementation of the Provider interface."""

    def __init__(self):
        self._client = OpenAI(api_key=read_api_key())

    @property
    def name(self) -> str:
        return "OpenAI"

    def ask(self, prompt: str) -> str:
        response = self._client.responses.create(
            model="gpt-5",
            input=prompt,
        )

        return response.output_text
