#!/usr/bin/env python3
"""Valida y prepara la única raíz pública del sitio: `frontend/`."""

from __future__ import annotations

import shutil
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_ROOT = REPOSITORY_ROOT / "frontend"
REQUIRED_PUBLIC_DIRECTORIES = ("errores", "casos")


def validate_public_structure() -> int:
    public_files = 0
    for name in REQUIRED_PUBLIC_DIRECTORIES:
        legacy_path = REPOSITORY_ROOT / name
        public_path = FRONTEND_ROOT / name
        if legacy_path.exists():
            raise RuntimeError(
                f"La carpeta pública {name}/ no debe permanecer en la raíz del repositorio."
            )
        if not public_path.is_dir():
            raise FileNotFoundError(
                f"No se encontró la carpeta pública requerida: {public_path}"
            )
        public_files += sum(1 for path in public_path.rglob("*") if path.is_file())
    return public_files


def ensure_icon_alias() -> None:
    source = FRONTEND_ROOT / "app-icon-192.png"
    destination = FRONTEND_ROOT / "favicon-192.png"
    if not source.is_file():
        raise FileNotFoundError(f"No se encontró el icono fuente: {source}")
    shutil.copy2(source, destination)


def main() -> int:
    if not FRONTEND_ROOT.is_dir():
        raise FileNotFoundError(f"No se encontró la carpeta frontend: {FRONTEND_ROOT}")

    public_files = validate_public_structure()
    ensure_icon_alias()
    print(
        "Frontend preparado correctamente: "
        f"raíz pública única en frontend/, {public_files} archivos históricos "
        "y favicon-192.png disponibles."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
