from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
GENERATED_DIR = PROJECT_ROOT / "generated"


def generated_file(name: str) -> Path:
    return GENERATED_DIR / name