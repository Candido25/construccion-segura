#!/usr/bin/env python3
"""Valida recursos gráficos y evita material privado en el repositorio público."""

from __future__ import annotations

import hashlib
import sys
import warnings
from pathlib import Path
from xml.etree import ElementTree

from PIL import ExifTags, Image

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_PATHS = (
    ROOT / "review_photos",
    ROOT / "_incoming",
    ROOT / "debug.log",
)
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".ico"}
EXPECTED_FORMATS = {
    ".png": "PNG",
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
    ".webp": "WEBP",
    ".ico": "ICO",
}
EXPECTED_ICON_SIZES = {
    "favicon-48.png": (48, 48),
    "app-icon-192.png": (192, 192),
    "app-icon-maskable-512.png": (512, 512),
}
GPS_TAG = next(tag for tag, name in ExifTags.TAGS.items() if name == "GPSInfo")


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def validate_image(path: Path) -> tuple[list[str], str]:
    errors: list[str] = []
    expected_format = EXPECTED_FORMATS[path.suffix.lower()]
    digest = hashlib.sha256(path.read_bytes()).hexdigest()

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            with Image.open(path) as image:
                actual_format = image.format
                dimensions = image.size
                image.verify()

            with Image.open(path) as image:
                exif = image.getexif()
                if exif and GPS_TAG in exif:
                    errors.append(f"{relative(path)}: contiene ubicación GPS en EXIF")
                image.load()
    except Exception as exc:  # Pillow normaliza diversos errores binarios.
        return [f"{relative(path)}: imagen inválida: {type(exc).__name__}: {exc}"], digest

    if actual_format != expected_format:
        errors.append(
            f"{relative(path)}: formato interno {actual_format!r}; se esperaba {expected_format!r}"
        )

    expected_size = EXPECTED_ICON_SIZES.get(relative(path))
    if expected_size and dimensions != expected_size:
        errors.append(
            f"{relative(path)}: dimensiones {dimensions}; se esperaban {expected_size}"
        )

    return errors, digest


def main() -> int:
    errors: list[str] = []
    verified_icons: list[str] = []

    for forbidden in FORBIDDEN_PATHS:
        if forbidden.exists():
            errors.append(f"Ruta privada o temporal todavía versionada: {relative(forbidden)}")

    images = sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix.lower() in IMAGE_EXTENSIONS
    )

    for image in images:
        image_errors, digest = validate_image(image)
        errors.extend(image_errors)
        if relative(image) in EXPECTED_ICON_SIZES and not image_errors:
            verified_icons.append(f"{relative(image)} sha256={digest}")

    for svg in sorted(ROOT.rglob("*.svg")):
        if ".git" in svg.parts:
            continue
        try:
            ElementTree.parse(svg)
        except Exception as exc:
            errors.append(f"{relative(svg)}: SVG inválido: {type(exc).__name__}: {exc}")

    missing_expected = [name for name in EXPECTED_ICON_SIZES if not (ROOT / name).is_file()]
    errors.extend(f"Falta el recurso obligatorio: {name}" for name in missing_expected)

    if errors:
        print("Asset safety checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Asset safety checks passed for {len(images)} raster images.")
    for record in verified_icons:
        print(f"- {record}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
