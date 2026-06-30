from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.providers.claude_provider import ClaudeProvider
from ai_lab.providers.openai_provider import OpenAIProvider


def provider_from_name(name: str):
    normalized = name.strip().lower()

    if normalized == "openai":
        return OpenAIProvider()

    if normalized in {"claude", "anthropic"}:
        return ClaudeProvider()

    raise ValueError(f"Unknown provider: {name}")


def main() -> int:
    if len(sys.argv) < 3:
        print('Usage: python scripts/ask_provider.py <openai|claude> "<prompt>"')
        return 1

    provider_name = sys.argv[1]
    prompt = " ".join(sys.argv[2:])

    provider = provider_from_name(provider_name)

    print(f"Provider: {provider.name}")
    print()
    print(provider.ask(prompt))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
