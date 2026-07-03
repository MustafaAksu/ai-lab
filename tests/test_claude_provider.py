from unittest.mock import Mock, patch

from ai_lab.providers.claude_provider import ClaudeProvider


def test_claude_provider_name():
    with patch("ai_lab.providers.claude_provider.read_claude_api_key") as read_key:
        read_key.return_value = "test-key"

        provider = ClaudeProvider()

        assert provider.name == "Claude"


def test_claude_provider_ask_returns_text_blocks():
    with patch("ai_lab.providers.claude_provider.read_claude_api_key") as read_key:
        read_key.return_value = "test-key"

        provider = ClaudeProvider()
        provider._client = Mock()

        text_block = Mock()
        text_block.type = "text"
        text_block.text = "Hello from Claude."

        provider._client.messages.create.return_value = Mock(content=[text_block])

        answer = provider.ask("Hello")

        assert answer == "Hello from Claude."
        provider._client.messages.create.assert_called_once()
        assert provider._client.messages.create.call_args.kwargs["max_tokens"] == 4096


def test_claude_provider_accepts_custom_max_tokens():
    with patch("ai_lab.providers.claude_provider.read_claude_api_key") as read_key:
        read_key.return_value = "test-key"

        provider = ClaudeProvider(max_tokens=2048)
        provider._client = Mock()

        text_block = Mock()
        text_block.type = "text"
        text_block.text = "Short response."

        provider._client.messages.create.return_value = Mock(content=[text_block])

        assert provider.ask("Hello") == "Short response."
        assert provider._client.messages.create.call_args.kwargs["max_tokens"] == 2048
