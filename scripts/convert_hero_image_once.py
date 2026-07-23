#!/usr/bin/env python3
"""Convierte una sola vez la imagen de portada de fondo CSS a imagen HTML real."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
HERO = ROOT / "hero.css"
SERVICE_WORKER = ROOT / "service-worker.js"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    occurrences = text.count(old)
    if occurrences != 1:
        raise RuntimeError(f"{label}: se esperaba una coincidencia y se encontraron {occurrences}")
    return text.replace(old, new, 1)


def main() -> None:
    index = INDEX.read_text(encoding="utf-8")
    hero = HERO.read_text(encoding="utf-8")
    service_worker = SERVICE_WORKER.read_text(encoding="utf-8")

    if '<picture class="hero-image">' in index:
        print("La portada ya utiliza una imagen HTML real.")
        return

    index = replace_once(
        index,
        '''        <div class="hero-image"></div>''',
        '''        <picture class="hero-image">
          <img src="assets/site-photos/web/hero-portada.webp" width="2844" height="1600" alt="" decoding="async" fetchpriority="high">
        </picture>''',
        "estructura HTML de la imagen",
    )

    hero = replace_once(
        hero,
        '''.home-conversion-hero .hero-image {
  background:
    linear-gradient(200deg, rgba(255,244,232,0.06), rgba(30,52,62,0.42)),
    url("assets/site-photos/web/hero-portada.webp") center/cover;
  border-radius: 0 0 0 var(--radius);
  filter: saturate(0.9) contrast(1.03);
}
''',
        '''.home-conversion-hero .hero-image {
  display: block;
  overflow: hidden;
  border-radius: 0 0 0 var(--radius);
  filter: saturate(0.9) contrast(1.03);
}

.home-conversion-hero .hero-image img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.home-conversion-hero .hero-image::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(200deg, rgba(255,244,232,0.06), rgba(30,52,62,0.42));
  pointer-events: none;
}
''',
        "reglas de imagen HTML",
    )

    service_worker = replace_once(
        service_worker,
        '''const CACHE_VERSION = "mi-casa-segura-pwa-v9";''',
        '''const CACHE_VERSION = "mi-casa-segura-pwa-v10";''',
        "versión de caché",
    )
    service_worker = replace_once(
        service_worker,
        '''  "/hero.css",
  "/site-global.js",''',
        '''  "/hero.css",
  "/assets/site-photos/web/hero-portada.webp",
  "/site-global.js",''',
        "imagen de portada en APP_SHELL",
    )

    INDEX.write_text(index, encoding="utf-8")
    HERO.write_text(hero, encoding="utf-8")
    SERVICE_WORKER.write_text(service_worker, encoding="utf-8")
    print("Imagen de portada convertida a <picture>/<img>.")


if __name__ == "__main__":
    main()
