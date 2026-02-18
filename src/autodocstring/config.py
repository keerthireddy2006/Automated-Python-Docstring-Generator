import tomllib
from pathlib import Path


def load_config():
    path = Path("pyproject.toml")

    defaults = {
        "style": "Google",
        "min_coverage": 80,
        "enforce_pep257": True,
    }

    if not path.exists():
        return defaults

    with open(path, "rb") as f:
        data = tomllib.load(f)

    return {**defaults, **data.get("tool", {}).get("autodoc", {})}
