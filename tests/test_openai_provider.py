from unittest.mock import patch

from ai_lab.providers.openai_provider import OpenAIProvider


def test_openai_provider_name():
    with (
        patch("ai_lab.providers.openai_provider.read_api_key") as read_key,
        patch("ai_lab.providers.openai_provider.OpenAI"),
    ):
        read_key.return_value = "test-key"
        provider = OpenAIProvider()

        assert provider.name == "OpenAI"


def test_openai_provider_ask_returns_output_text():
    with (
        patch("ai_lab.providers.openai_provider.read_api_key") as read_key,
        patch("ai_lab.providers.openai_provider.OpenAI") as openai_cls,
    ):
        read_key.return_value = "test-key"
        client = openai_cls.return_value
        client.responses.create.return_value.output_text = "OpenAI response."

        provider = OpenAIProvider(model="gpt-test")

        assert provider.ask("Hello") == "OpenAI response."
        client.responses.create.assert_called_once_with(
            model="gpt-test",
            input="Hello",
        )


def test_openai_provider_passes_reasoning_effort():
    with (
        patch("ai_lab.providers.openai_provider.read_api_key") as read_key,
        patch("ai_lab.providers.openai_provider.OpenAI") as openai_cls,
    ):
        read_key.return_value = "test-key"
        client = openai_cls.return_value
        client.responses.create.return_value.output_text = "ok"

        provider = OpenAIProvider(model="gpt-test", reasoning_effort="xhigh")

        assert provider.ask("prompt") == "ok"
        client.responses.create.assert_called_once_with(
            model="gpt-test",
            input="prompt",
            reasoning={"effort": "xhigh"},
        )
