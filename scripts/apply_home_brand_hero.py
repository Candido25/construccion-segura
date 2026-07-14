#!/usr/bin/env python3
"""Apply the approved branded visual to the homepage hero."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CONVERSION = ROOT / "conversion.css"

index_text = INDEX.read_text(encoding="utf-8")

preload = '  <link rel="preload" as="image" href="assets/brand/portada-principal-construccion-segura.avif" type="image/avif">\n'
anchor = '  <link rel="stylesheet" href="conversion.css">\n'
if preload not in index_text:
    index_text = index_text.replace(anchor, preload + anchor, 1)

old_media = '''      <div class="hero-media watermark-frame" aria-hidden="true">
        <div class="hero-image"></div>
        <div class="hero-grid"></div>
        <div class="hero-badge hero-badge-top">Consulta remota nacional</div>
        <div class="hero-badge hero-badge-bottom">Visitas técnicas en Lima</div>
        <div class="hero-panel">
          <span>Responsable técnico</span>
          <strong>Ing. Omar Oswaldo Alcantara Aquino</strong>
          <p>Ingeniero<br>CIP N.° 364395</p>
        </div>
      </div>
'''
new_media = '''      <div class="hero-media hero-media-brand" role="img" aria-label="Vivienda terminada, planos y casco de Construcción Segura como representación de una obra planificada y protegida">
        <div class="hero-image"></div>
      </div>
'''
if old_media not in index_text and new_media not in index_text:
    raise SystemExit("Homepage hero media block was not found.")
index_text = index_text.replace(old_media, new_media, 1)
INDEX.write_text(index_text, encoding="utf-8")

css_text = CONVERSION.read_text(encoding="utf-8")
marker = "/* Branded homepage hero — approved July 2026 */"
hero_css = r'''

/* Branded homepage hero — approved July 2026 */
.home-conversion-hero .hero-media-brand {
  min-height: 34rem;
  background: #e9edf0;
}

.home-conversion-hero .hero-media-brand .hero-image {
  background-image:
    linear-gradient(200deg, rgba(255, 255, 255, 0.01), rgba(20, 34, 42, 0.08)),
    image-set(
      url("assets/brand/portada-principal-construccion-segura.avif") type("image/avif"),
      url("assets/site-photos/web/hero-portada.webp") type("image/webp")
    );
  background-position: center, center;
  background-size: cover, cover;
  background-repeat: no-repeat;
  filter: none;
}

@media (max-width: 1080px) {
  .home-conversion-hero .hero-media-brand {
    min-height: clamp(22rem, 55svh, 38rem);
  }

  .home-conversion-hero .hero-media-brand .hero-image {
    background-position: center, center 42%;
  }
}

@media (max-width: 600px) {
  .home-conversion-hero .hero-media-brand {
    min-height: 24rem;
  }

  .home-conversion-hero .hero-media-brand .hero-image {
    background-position: center, center;
  }
}
'''
if marker not in css_text:
    css_text = css_text.rstrip() + hero_css + "\n"
CONVERSION.write_text(css_text, encoding="utf-8")

# Remove the interrupted temporary upload from the working tree.
temporary_part = ROOT / "tmp/hero-portada/part-00.txt"
if temporary_part.exists():
    temporary_part.unlink()
    try:
        temporary_part.parent.rmdir()
        temporary_part.parent.parent.rmdir()
    except OSError:
        pass

print("Homepage brand hero applied.")
