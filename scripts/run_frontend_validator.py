#!/usr/bin/env python3
"""Ejecuta los validadores sobre el paquete estático generado en `public/`."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

VALIDATORS = {"check_assets", "check_resources", "check_site"}
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOT = REPOSITORY_ROOT / "public"


def load_validator(name: str):
    path = REPOSITORY_ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"public_validator_{name}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def display_relative(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(PUBLIC_ROOT).as_posix()
    except ValueError:
        return resolved.relative_to(REPOSITORY_ROOT).as_posix()


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in VALIDATORS:
        available = ", ".join(sorted(VALIDATORS))
        print(f"Uso: {Path(sys.argv[0]).name} <{available}>", file=sys.stderr)
        return 2
    if not PUBLIC_ROOT.is_dir():
        print(
            "No se encontró public/. Ejecuta primero scripts/prepare_frontend.py.",
            file=sys.stderr,
        )
        return 2

    name = sys.argv[1]
    validator = load_validator(name)
    validator.ROOT = PUBLIC_ROOT

    if name == "check_assets":
        validator.relative = display_relative
        validator.FORBIDDEN_PATHS = (
            REPOSITORY_ROOT / "review_photos",
            REPOSITORY_ROOT / "_incoming",
            REPOSITORY_ROOT / "debug.log",
            PUBLIC_ROOT / "review_photos",
            PUBLIC_ROOT / "_incoming",
            PUBLIC_ROOT / "debug.log",
        )

    return int(validator.main())


if __name__ == "__main__":
    raise SystemExit(main())
