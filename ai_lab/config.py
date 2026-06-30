from pathlib import Path


class ConfigError(Exception):
    """Raised when AI-Lab configuration is missing or invalid."""


def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).resolve().parent.parent


def read_local_secret(filename: str) -> str:
    """Read a local secret from a git-ignored file in the project root."""
    secret_path = project_root() / filename

    if not secret_path.exists():
        raise ConfigError(f"Secret file not found: {secret_path}")

    secret = secret_path.read_text(encoding="utf-8").strip()

    if not secret:
        raise ConfigError(f"Secret file is empty: {secret_path}")

    return secret


def read_api_key(filename: str = "api_key.txt") -> str:
    """Read the OpenAI API key from a local ignored file."""
    return read_local_secret(filename)


def read_claude_api_key(filename: str = "claude_api_key.txt") -> str:
    """Read the Claude API key from a local ignored file."""
    return read_local_secret(filename)
