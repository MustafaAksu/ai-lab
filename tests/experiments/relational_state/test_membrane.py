"""Two-tier import membrane (PREREG §9; WARR-20260912-0001 conditions 4-6)."""

import ast
import sys
from pathlib import Path

from ai_lab.experiments import relational_state
from ai_lab.providers.invocation_record import CAPTURE_PATHS

PKG = Path(relational_state.__file__).parent
FORBIDDEN_PREFIXES = ("ai_lab.documentation", "ai_lab.research")


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:  # relative import within the package
                names.add(f"{relational_state.__name__}.{node.module or ''}")
            else:
                names.add(node.module or "")
    return names


def test_integration_effect_is_none():
    assert relational_state.INTEGRATION_EFFECT == "none"


def test_non_runner_modules_are_standard_library_only():
    for path in PKG.glob("*.py"):
        if path.name == "runner.py":
            continue
        for name in _imports(path):
            top = name.split(".")[0]
            assert top in sys.stdlib_module_names or name.startswith(relational_state.__name__), (path.name, name)


def test_runner_if_present_imports_only_providers_from_ai_lab():
    runner = PKG / "runner.py"
    if not runner.exists():
        return
    for name in _imports(runner):
        if name.startswith("ai_lab."):
            assert name.startswith(("ai_lab.providers", relational_state.__name__)), name


def test_nothing_imports_host_documentation_or_research_layers():
    for path in PKG.glob("*.py"):
        for name in _imports(path):
            assert not name.startswith(FORBIDDEN_PREFIXES), (path.name, name)


def test_host_capture_path_set_is_untouched():
    assert CAPTURE_PATHS == frozenset({"scripts/compare_providers.py"})
