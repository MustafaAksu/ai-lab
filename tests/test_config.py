from pathlib import Path

from ai_lab.config import project_root


def test_project_root_exists():
    root = project_root()
    assert isinstance(root, Path)
    assert root.exists()


def test_api_key_is_gitignored():
    gitignore = project_root() / ".gitignore"
    assert gitignore.exists()
    assert "api_key.txt" in gitignore.read_text(encoding="utf-8")
