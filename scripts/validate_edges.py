from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.documentation.edge_validation import validate_edges_directory


def main() -> int:
    edge_dir = Path("docs/edges")
    results = validate_edges_directory(edge_dir)

    if not results:
        print("No EDGE records found.")
        return 0

    failed = False

    for path, errors in results.items():
        if errors:
            failed = True
            print(f"{path}: FAIL")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"{path}: OK")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
