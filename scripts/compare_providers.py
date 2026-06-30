from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.providers.claude_provider import ClaudeProvider
from ai_lab.providers.openai_provider import OpenAIProvider


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: python scripts/compare_providers.py "<prompt>"')
        return 1

    prompt = " ".join(sys.argv[1:])

    providers = [
        OpenAIProvider(),
        ClaudeProvider(),
    ]

    print("Prompt:")
    print(prompt)
    print()

    for provider in providers:
        print(f"=== {provider.name} ===")
        print(provider.ask(prompt))
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
