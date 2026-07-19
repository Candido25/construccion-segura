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
EXPECTED_ICONS = {
    "favicon-48.png": {
        "size": (48, 48),
        "sha256": "a2e73287df3be3c2409383f137c11a86f31c83648c03c3e7efbe147456b5d6b9",
    },
    "app-icon-192.png": {
        "size": (192, 192),
        "sha256": "2a72b896772d90d0abde060f8d68040275b2f9d6cd8dcaea001332a68988edbb",
    },
    "app-icon-maskable-512.png": {
        "size": (512, 512),
        "sha256": "91989c23a546235d5b5c4574c91c8c9a8933d49fbdf60edc8ebe2971cf0c96c4",
    },
}
GPS_TAG = next(tag for tag, name in ExifTags.TAGS.items() if name == "GPSInfo")


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def validate_image(path: Path) -> list[str]:
    errors: list[str] = []
    expected_format = EXPECTED_FORMATS[path.suffix.lower()]

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
        return [f"{relative(path)}: imagen inválida: {type(exc).__name__}: {exc}"]

    if actual_format != expected_format:
        errors.append(
            f"{relative(path)}: formato interno {actual_format!r}; se esperaba {expected_format!r}"
        )

    expected_icon = EXPECTED_ICONS.get(relative(path))
    if expected_icon:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if dimensions != expected_icon["size"]:
            errors.append(
                f"{relative(path)}: dimensiones {dimensions}; se esperaban {expected_icon['size']}"
            )
        if digest != expected_icon["sha256"]:
            errors.append(
                f"{relative(path)}: SHA-256 {digest}; se esperaba {expected_icon['sha256']}"
            )

    return errors


def main() -> int:
    errors: list[str] = []

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
        errors.extend(validate_image(image))

    for svg in sorted(ROOT.rglob("*.svg")):
        if ".git" in svg.parts:
            continue
        try:
            ElementTree.parse(svg)
        except Exception as exc:
            errors.append(f"{relative(svg)}: SVG inválido: {type(exc).__name__}: {exc}")

    missing_expected = [name for name in EXPECTED_ICONS if not (ROOT / name).is_file()]
    errors.extend(f"Falta el recurso obligatorio: {name}" for name in missing_expected)

    if errors:
        print("Asset safety checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Asset safety checks passed for {len(images)} raster images.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
