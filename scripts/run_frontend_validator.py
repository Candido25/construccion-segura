#!/usr/bin/env python3
"""Ejecuta los validadores históricos usando `frontend/` como raíz pública."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

VALIDATORS = {"check_assets", "check_resources", "check_site"}
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_ROOT = REPOSITORY_ROOT / "frontend"


def load_validator(name: str):
    path = REPOSITORY_ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"frontend_validator_{name}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def display_relative(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(FRONTEND_ROOT).as_posix()
    except ValueError:
        return resolved.relative_to(REPOSITORY_ROOT).as_posix()


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in VALIDATORS:
        available = ", ".join(sorted(VALIDATORS))
        print(f"Uso: {Path(sys.argv[0]).name} <{available}>", file=sys.stderr)
        return 2

    if not FRONTEND_ROOT.is_dir():
        print("No se encontró la carpeta frontend/.", file=sys.stderr)
        return 2

    name = sys.argv[1]
    validator = load_validator(name)
    validator.ROOT = FRONTEND_ROOT

    if name == "check_assets":
        validator.relative = display_relative
        validator.FORBIDDEN_PATHS = (
            REPOSITORY_ROOT / "review_photos",
            REPOSITORY_ROOT / "_incoming",
            REPOSITORY_ROOT / "debug.log",
            FRONTEND_ROOT / "review_photos",
            FRONTEND_ROOT / "_incoming",
            FRONTEND_ROOT / "debug.log",
        )

    return int(validator.main())


if __name__ == "__main__":
    raise SystemExit(main())
