#!/usr/bin/env python3
"""Construye `public/` sin exponer el backend ni archivos internos."""

from __future__ import annotations

import shutil
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_ROOT = REPOSITORY_ROOT / "frontend"
APP_SOURCE = FRONTEND_ROOT / "app"
PUBLIC_ROOT = REPOSITORY_ROOT / "public"
MANIFEST_PATH = REPOSITORY_ROOT / "scripts" / "public_root_entries.txt"
FORBIDDEN_PUBLIC_ENTRIES = {
    ".git",
    ".github",
    "backend",
    "docs",
    "scripts",
    "requirements.txt",
    "AGENTS.md",
    "README.md",
    "public",
}


def load_public_entries() -> tuple[str, ...]:
    if not MANIFEST_PATH.is_file():
        raise FileNotFoundError(f"No se encontró el manifiesto público: {MANIFEST_PATH}")
    entries = tuple(
        line.strip()
        for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    )
    if not entries:
        raise RuntimeError("El manifiesto público está vacío.")
    if len(entries) != len(set(entries)):
        raise RuntimeError("El manifiesto público contiene entradas duplicadas.")
    forbidden = sorted(set(entries).intersection(FORBIDDEN_PUBLIC_ENTRIES))
    if forbidden:
        raise RuntimeError(f"El manifiesto intenta publicar rutas internas: {forbidden}")
    return entries


def validate_source(entries: tuple[str, ...]) -> None:
    if not FRONTEND_ROOT.is_dir():
        raise FileNotFoundError(f"No se encontró {FRONTEND_ROOT}")
    if not APP_SOURCE.is_dir():
        raise FileNotFoundError(f"No se encontró el cliente dinámico: {APP_SOURCE}")

    unexpected = sorted(child.name for child in FRONTEND_ROOT.iterdir() if child.name != "app")
    if unexpected:
        raise RuntimeError(
            "frontend/ debe contener únicamente app/. Entradas inesperadas: "
            f"{unexpected}"
        )

    missing = [entry for entry in entries if not (REPOSITORY_ROOT / entry).exists()]
    if missing:
        raise FileNotFoundError(f"Faltan fuentes públicas en la raíz: {missing}")

    for required in ("index.html", "styles.css", "script.js"):
        if required not in entries:
            raise RuntimeError(f"El manifiesto no incluye {required}")


def copy_entry(source: Path, destination: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, destination)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def build_public_site() -> int:
    entries = load_public_entries()
    validate_source(entries)

    if PUBLIC_ROOT.exists():
        shutil.rmtree(PUBLIC_ROOT)
    PUBLIC_ROOT.mkdir(parents=True)

    for entry in entries:
        copy_entry(REPOSITORY_ROOT / entry, PUBLIC_ROOT / entry)
    copy_entry(APP_SOURCE, PUBLIC_ROOT / "app")

    leaked = sorted(name for name in FORBIDDEN_PUBLIC_ENTRIES if (PUBLIC_ROOT / name).exists())
    if leaked:
        raise RuntimeError(f"El paquete público contiene rutas internas: {leaked}")

    required_outputs = (
        PUBLIC_ROOT / "index.html",
        PUBLIC_ROOT / "app" / "index.html",
        PUBLIC_ROOT / "service-worker.js",
        PUBLIC_ROOT / "site.webmanifest",
    )
    missing_outputs = [str(path) for path in required_outputs if not path.is_file()]
    if missing_outputs:
        raise FileNotFoundError(f"El paquete público quedó incompleto: {missing_outputs}")

    return sum(1 for path in PUBLIC_ROOT.rglob("*") if path.is_file())


def main() -> int:
    total = build_public_site()
    print(
        "Paquete público preparado correctamente en public/: "
        f"{total} archivos, web institucional desde la raíz y app desde frontend/app/."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
