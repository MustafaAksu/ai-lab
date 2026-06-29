from ai_lab.providers.openai_provider import OpenAIProvider


def main():
    provider = OpenAIProvider()

    print(f"Provider : {provider.name}")
    print()

    answer = provider.ask(
        "Hello world. Please greet the world."
    )

    print(answer)


if __name__ == "__main__":
    main()
