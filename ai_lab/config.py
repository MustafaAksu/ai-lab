from pathlib import Path


class ConfigError(Exception):
    """Raised when AI-Lab configuration is missing or invalid."""


def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).resolve().parent.parent


def read_api_key(filename: str = "api_key.txt") -> str:
    """Read the OpenAI API key from a local ignored file."""
    key_path = project_root() / filename

    if not key_path.exists():
        raise ConfigError(f"API key file not found: {key_path}")

    api_key = key_path.read_text(encoding="utf-8").strip()

    if not api_key:
        raise ConfigError(f"API key file is empty: {key_path}")

    return api_key
