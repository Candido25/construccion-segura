from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/site-photos/web/hero-portada.webp"
DESKTOP = ROOT / "assets/site-photos/web/hero-portada-desktop.webp"
MOBILE = ROOT / "assets/site-photos/web/hero-portada-mobile.webp"
INDEX = ROOT / "index.html"
SERVICE_WORKER = ROOT / "service-worker.js"
RESPONSIVE_CSS = ROOT / "hero-responsive.css"
VERSION = "20260718-1"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f"No se encontró el bloque esperado en {path.relative_to(ROOT)}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def normalized_source() -> Image.Image:
    with Image.open(SOURCE) as image:
        image.load()
        if image.format != "WEBP":
            raise RuntimeError(f"La portada fuente no es WebP: {image.format}")
        if image.mode in {"RGBA", "LA"}:
            base = Image.new("RGB", image.size, "white")
            base.paste(image.convert("RGBA"), mask=image.convert("RGBA").getchannel("A"))
            return base
        return image.convert("RGB")


def responsive_canvas(source: Image.Image, size: tuple[int, int]) -> Image.Image:
    width, height = size
    blurred = ImageOps.fit(source, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    blurred = blurred.filter(ImageFilter.GaussianBlur(radius=max(width, height) / 38))
    veil = Image.new("RGBA", size, (238, 242, 244, 105))
    background = Image.alpha_composite(blurred.convert("RGBA"), veil).convert("RGB")

    foreground = ImageOps.contain(source, size, method=Image.Resampling.LANCZOS)
    x = (width - foreground.width) // 2
    y = (height - foreground.height) // 2
    background.paste(foreground, (x, y))
    return background


def save_webp(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "WEBP", quality=84, method=6)


def validate_image(path: Path, expected_size: tuple[int, int]) -> None:
    with Image.open(path) as image:
        image.load()
        if image.format != "WEBP":
            raise RuntimeError(f"{path.name} no es un WebP válido")
        if image.size != expected_size:
            raise RuntimeError(f"{path.name} tiene tamaño {image.size}, se esperaba {expected_size}")


def patch_index() -> None:
    old_head = '''  <link rel="stylesheet" href="styles.css">
  <link rel="stylesheet" href="site-pages.css">
  <link rel="stylesheet" href="conversion.css">'''
    new_head = f'''  <link rel="preload" as="image" href="assets/site-photos/web/hero-portada-desktop.webp?v={VERSION}" type="image/webp" media="(min-width: 1081px)">
  <link rel="preload" as="image" href="assets/site-photos/web/hero-portada-mobile.webp?v={VERSION}" type="image/webp" media="(max-width: 1080px)">
  <link rel="stylesheet" href="styles.css">
  <link rel="stylesheet" href="site-pages.css">
  <link rel="stylesheet" href="conversion.css">
  <link rel="stylesheet" href="hero-responsive.css?v={VERSION}">'''
    replace_once(INDEX, old_head, new_head)

    old_hero = '''      <div class="hero-media watermark-frame" aria-hidden="true">
        <div class="hero-image"></div>
        <div class="hero-grid"></div>
        <div class="hero-badge hero-badge-top">Consulta remota nacional</div>
        <div class="hero-badge hero-badge-bottom">Visitas técnicas en Lima</div>
        <div class="hero-panel">
          <span>Responsable técnico</span>
          <strong>Ing. Omar Oswaldo Alcantara Aquino</strong>
          <p>Ingeniero<br>CIP N.° 364395</p>
        </div>
      </div>'''
    new_hero = f'''      <div class="hero-media hero-media-brand watermark-frame">
        <picture class="hero-image hero-picture">
          <source media="(max-width: 1080px)" srcset="assets/site-photos/web/hero-portada-mobile.webp?v={VERSION}">
          <img src="assets/site-photos/web/hero-portada-desktop.webp?v={VERSION}" width="1920" height="1080" alt="Vivienda, planos, herramientas y casco de Construcción Segura como representación de una obra planificada y protegida" decoding="async" fetchpriority="high">
        </picture>
        <div class="hero-grid" aria-hidden="true"></div>
        <div class="hero-badge hero-badge-top">Consulta remota nacional</div>
        <div class="hero-badge hero-badge-bottom">Visitas técnicas en Lima</div>
        <div class="hero-panel">
          <span>Responsable técnico</span>
          <strong>Ing. Omar Oswaldo Alcantara Aquino</strong>
          <p>Ingeniero<br>CIP N.° 364395</p>
        </div>
      </div>'''
    replace_once(INDEX, old_hero, new_hero)


def write_css() -> None:
    RESPONSIVE_CSS.write_text(
        '''/* Portada responsive: imagen HTML real con versiones de escritorio y móvil. */
.home-conversion-hero .hero-picture {
  position: absolute;
  inset: 0;
  display: block;
  overflow: hidden;
  border-radius: 0 0 0 var(--radius);
  background: #eef2f4 !important;
  filter: none !important;
}

.home-conversion-hero .hero-picture img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center;
}

@media (min-width: 1081px) {
  .home-conversion-hero .hero {
    min-height: 100svh;
    padding-top: 4.15rem;
  }

  .home-conversion-hero .hero-content,
  .home-conversion-hero .hero-media {
    min-height: calc(100svh - 4.15rem);
  }
}

@media (max-width: 1080px) {
  .home-conversion-hero .hero-picture {
    border-radius: 0 0 var(--radius) var(--radius);
  }

  .home-conversion-hero .hero-picture img {
    object-fit: contain;
    background: #eef2f4;
  }
}
''',
        encoding="utf-8",
    )


def patch_service_worker() -> None:
    replace_once(
        SERVICE_WORKER,
        'const CACHE_VERSION = "mi-casa-segura-pwa-v8";',
        'const CACHE_VERSION = "mi-casa-segura-pwa-v9";',
    )
    old = '''  "/conversion.css",
  "/site-global.js",'''
    new = f'''  "/conversion.css",
  "/hero-responsive.css?v={VERSION}",
  "/assets/site-photos/web/hero-portada-desktop.webp?v={VERSION}",
  "/assets/site-photos/web/hero-portada-mobile.webp?v={VERSION}",
  "/site-global.js",'''
    replace_once(SERVICE_WORKER, old, new)


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)

    source = normalized_source()
    save_webp(responsive_canvas(source, (1920, 1080)), DESKTOP)
    save_webp(responsive_canvas(source, (900, 1000)), MOBILE)
    validate_image(DESKTOP, (1920, 1080))
    validate_image(MOBILE, (900, 1000))

    patch_index()
    write_css()
    patch_service_worker()

    print(f"Generada: {DESKTOP.relative_to(ROOT)} ({DESKTOP.stat().st_size} bytes)")
    print(f"Generada: {MOBILE.relative_to(ROOT)} ({MOBILE.stat().st_size} bytes)")
    print("Portada responsive preparada y validada.")


if __name__ == "__main__":
    main()
