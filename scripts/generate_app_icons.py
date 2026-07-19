#!/usr/bin/env python3
"""Genera de forma determinista los iconos públicos desde fuentes oficiales válidas."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FAVICON_SOURCE = ROOT / "favicon.ico"
TOUCH_SOURCE = ROOT / "apple-touch-icon.png"


def open_verified(path: Path) -> Image.Image:
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        return image.convert("RGBA")


def save_png(image: Image.Image, destination: Path) -> None:
    image.save(
        destination,
        format="PNG",
        optimize=True,
        compress_level=9,
        icc_profile=None,
        exif=b"",
    )


def main() -> None:
    favicon_source = open_verified(FAVICON_SOURCE)
    touch_source = open_verified(TOUCH_SOURCE)

    favicon_48 = favicon_source.resize((48, 48), Image.Resampling.LANCZOS)
    save_png(favicon_48, ROOT / "favicon-48.png")

    icon_192 = touch_source.resize((192, 192), Image.Resampling.LANCZOS)
    save_png(icon_192, ROOT / "app-icon-192.png")

    maskable_canvas = Image.new("RGBA", (512, 512), (255, 255, 255, 255))
    maskable_symbol = touch_source.resize((400, 400), Image.Resampling.LANCZOS)
    maskable_canvas.alpha_composite(maskable_symbol, ((512 - 400) // 2, (512 - 400) // 2))
    save_png(maskable_canvas, ROOT / "app-icon-maskable-512.png")

    for path, expected in (
        (ROOT / "favicon-48.png", (48, 48)),
        (ROOT / "app-icon-192.png", (192, 192)),
        (ROOT / "app-icon-maskable-512.png", (512, 512)),
    ):
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            image.load()
            if image.format != "PNG" or image.size != expected:
                raise RuntimeError(f"No se pudo generar correctamente {path.name}")

    print("Iconos generados y verificados desde fuentes oficiales.")


if __name__ == "__main__":
    main()
