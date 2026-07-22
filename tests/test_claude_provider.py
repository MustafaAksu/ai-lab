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
        # Default raised to 16000 by the governed settings rider of
        # PLAN-20260722-0001 (WARR-20260722-0001) after the COMP-0032
        # truncation incident.
        assert provider._client.messages.create.call_args.kwargs["max_tokens"] == 16000


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

def test_claude_provider_passes_effort():
    with (
        patch("ai_lab.providers.claude_provider.read_claude_api_key") as read_key,
        patch("ai_lab.providers.claude_provider.Anthropic") as anthropic_cls,
    ):
        read_key.return_value = "test-key"
        client = anthropic_cls.return_value

        text_block = type("Block", (), {"type": "text", "text": "ok"})()
        client.messages.create.return_value.content = [text_block]

        provider = ClaudeProvider(
            model="claude-test",
            max_tokens=1234,
            effort="xhigh",
        )

        assert provider.ask("prompt") == "ok"

        client.messages.create.assert_called_once_with(
            model="claude-test",
            max_tokens=1234,
            messages=[{"role": "user", "content": "prompt"}],
            output_config={"effort": "xhigh"},
        )
