#!/usr/bin/env python3
"""Prepara el artefacto estático que GitHub Pages publicará desde `frontend/`.

La reorganización conserva temporalmente las guías y expedientes históricos en la
raíz del repositorio. Este paso los copia al artefacto público sin duplicarlos en
Git y crea los alias de recursos que esperan las páginas existentes.
"""

from __future__ import annotations

import shutil
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_ROOT = REPOSITORY_ROOT / "frontend"
LEGACY_PUBLIC_DIRECTORIES = ("errores", "casos")


def copy_public_directory(name: str) -> int:
    source = REPOSITORY_ROOT / name
    destination = FRONTEND_ROOT / name
    if not source.is_dir():
        raise FileNotFoundError(f"No se encontró la carpeta pública de origen: {source}")

    shutil.copytree(source, destination, dirs_exist_ok=True)
    return sum(1 for path in destination.rglob("*") if path.is_file())


def ensure_icon_alias() -> None:
    source = FRONTEND_ROOT / "app-icon-192.png"
    destination = FRONTEND_ROOT / "favicon-192.png"
    if not source.is_file():
        raise FileNotFoundError(f"No se encontró el icono fuente: {source}")
    shutil.copy2(source, destination)


def main() -> int:
    if not FRONTEND_ROOT.is_dir():
        raise FileNotFoundError(f"No se encontró la carpeta frontend: {FRONTEND_ROOT}")

    copied_files = 0
    for directory in LEGACY_PUBLIC_DIRECTORIES:
        copied_files += copy_public_directory(directory)

    ensure_icon_alias()
    print(
        "Frontend preparado correctamente: "
        f"{copied_files} archivos históricos y favicon-192.png disponibles."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
