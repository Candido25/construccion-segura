#!/usr/bin/env python3
"""Extrae una sola vez la portada desde styles.css y conversion.css hacia hero.css."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLES = ROOT / "styles.css"
CONVERSION = ROOT / "conversion.css"
INDEX = ROOT / "index.html"
SERVICE_WORKER = ROOT / "service-worker.js"
HERO = ROOT / "hero.css"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    occurrences = text.count(old)
    if occurrences != 1:
        raise RuntimeError(f"{label}: se esperaba una coincidencia exacta y se encontraron {occurrences}")
    return text.replace(old, new, 1)


def main() -> None:
    if not HERO.is_file():
        raise RuntimeError("Falta hero.css")

    styles = STYLES.read_text(encoding="utf-8")
    conversion = CONVERSION.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")
    service_worker = SERVICE_WORKER.read_text(encoding="utf-8")

    if "HOME HERO: structural rules live in hero.css" in styles:
        print("La portada ya fue extraída.")
        return

    styles = replace_once(
        styles,
        '''/* ── HERO ────────────────────────────────────────────────────────── */
.hero {
  position: relative;
  min-height: 32rem;
  padding: 6.1rem 0 0;
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
  align-items: stretch;
  overflow: clip;
}

.hero::after {
  content: "";
  position: absolute;
  inset: auto 0 0;
  height: 3.5rem;
  background: linear-gradient(180deg, transparent, rgba(245,237,224,0.98));
  pointer-events: none;
}

.hero-content,
.section,
.cta-panel {
  width: min(var(--max), calc(100% - 2.8rem));
  margin-inline: auto;
}

.hero-content {
  position: relative;
  z-index: 2;
  align-self: stretch;
  min-height: 32rem;
  width: auto;
  max-width: 52rem;
  margin-inline: auto;
  padding: 1.2rem 2.4rem 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.hero-brand {
  margin: 0 0 0.55rem;
  font-family: var(--font-display);
  font-size: clamp(1.9rem, 3vw, 2.9rem);
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--accent);
  margin-inline: auto;
}

''',
        '''/* ── HOME HERO: structural rules live in hero.css ───────────────── */
.section,
.cta-panel {
  width: min(var(--max), calc(100% - 2.8rem));
  margin-inline: auto;
}

''',
        "bloque principal de portada",
    )

    styles = replace_once(
        styles,
        '''.hero h1 {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(2.6rem, 4.2vw, 4.2rem);
  font-weight: 700;
  line-height: 0.98;
  letter-spacing: -0.04em;
  max-width: 14.5ch;
  margin-inline: auto;
  text-wrap: balance;
}

.hero-text {
  max-width: 31rem;
  margin: 1.4rem 0 0;
  color: var(--muted);
  font-size: 1.03rem;
  line-height: 1.78;
  margin-inline: auto;
}

''',
        "",
        "título y texto de portada",
    )

    styles = replace_once(
        styles,
        '''/* Review panel */
.hero-review-panel {
  max-width: 36rem;
  margin-bottom: 2rem;
  padding: 1.15rem 1.25rem;
  border: 1.5px solid rgba(201,111,45,0.18);
  border-radius: var(--radius-sm);
  background: rgba(253,248,241,0.84);
  box-shadow: var(--shadow-sm);
  text-align: left;
}
.hero-review-panel strong {
  display: block;
  margin-bottom: 0.8rem;
  font-size: 1rem;
  line-height: 1.4;
}
.hero-review-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.hero-review-list li {
  position: relative;
  padding: 0.6rem 0 0.6rem 1.45rem;
  color: var(--muted);
  font-size: 0.92rem;
  line-height: 1.6;
  border-top: 1px solid rgba(28, 42, 51, 0.08);
}
.hero-review-list li:first-child { border-top: 0; padding-top: 0; }
.hero-review-list li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 1.05rem;
  width: 0.55rem;
  height: 0.55rem;
  border-radius: 50%;
  background: var(--accent);
}
.hero-review-list li:first-child::before { top: 0.45rem; }

''',
        "",
        "panel de revisión",
    )

    styles = replace_once(
        styles,
        '''/* Hero points */
.hero-points {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.85rem;
  padding: 0;
  margin: 0;
  list-style: none;
}
.hero-points li {
  padding: 1rem 1rem 1.05rem;
  border: 1px solid var(--line);
  border-radius: var(--radius-sm);
  color: var(--muted);
  font-size: 0.88rem;
  line-height: 1.65;
  background: rgba(253,248,241,0.72);
  box-shadow: var(--shadow-sm);
  position: relative;
  overflow: hidden;
}
.hero-points li::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--accent), transparent);
  opacity: 0.55;
}

''',
        "",
        "puntos de portada",
    )

    styles = replace_once(
        styles,
        '''/* Hero media */
.hero-media {
  position: relative;
  min-height: 32rem;
  margin-bottom: 0;
}
.hero-image,
.hero-grid {
  position: absolute;
  inset: 0;
}
.hero-image {
  background:
    linear-gradient(200deg, rgba(255,244,232,0.06), rgba(30,52,62,0.42)),
    url("assets/site-photos/web/hero-portada.webp") center/cover;
  border-radius: 0 0 0 var(--radius);
  filter: saturate(0.9) contrast(1.03);
}
.hero-grid {
  background-image:
    linear-gradient(rgba(255,255,255,0.14) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.14) 1px, transparent 1px);
  background-size: 72px 72px;
  mix-blend-mode: overlay;
  opacity: 0.45;
  border-radius: 0 0 0 var(--radius);
}

/* Floating badges */
.hero-badge {
  position: absolute;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.7rem 1.1rem;
  border-radius: 999px;
  background: rgba(253,248,241,0.90);
  border: 1.5px solid rgba(201,111,45,0.20);
  backdrop-filter: blur(10px);
  color: var(--text-dark);
  font-weight: 700;
  font-size: 0.9rem;
  box-shadow: 0 10px 26px rgba(50,34,14,0.13);
}
.hero-badge::before {
  content: "";
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--accent);
  flex-shrink: 0;
}
.hero-badge-top    { top: 18%; right: 11%; }
.hero-badge-bottom { bottom: 14%; left: 9%; }

''',
        "",
        "medio visual y distintivos",
    )

    styles = replace_once(
        styles,
        '''@media (max-width: 1080px) {
  .hero { grid-template-columns: 1fr; min-height: auto; }
  .hero-media { order: -1; min-height: 56svh; margin-bottom: 0; }
  .hero-image, .hero-grid { border-radius: 0; }

  .hero-content,
  .section,
  .cta-panel {
    width: min(var(--max), calc(100% - 1.8rem));
  }
  .hero-content {
    width: min(var(--max), calc(100% - 1.8rem));
    max-width: none;
    margin-inline: auto;
    padding: 2rem 0 4.5rem;
    align-items: stretch;
    text-align: left;
  }
  .hero h1 {
    max-width: 15ch;
    font-size: clamp(2.8rem, 8vw, 4.4rem);
    line-height: 0.98;
    text-wrap: pretty;
  }
  .hero-text {
    max-width: 42rem;
    margin-inline: 0;
  }

  .hero-points,
  .proof-inner,
''',
        '''@media (max-width: 1080px) {
  .section,
  .cta-panel {
    width: min(var(--max), calc(100% - 1.8rem));
  }

  .proof-inner,
''',
        "responsive 1080",
    )

    styles = replace_once(
        styles,
        '''  .hero { padding-top: 5.8rem; padding-bottom: 4.2rem; }
  .hero-media { min-height: 46svh; }
  .hero-panel { right: 0.9rem; left: 0.9rem; bottom: 0.9rem; max-width: none; }
.hero-review-panel { max-width: none; }
  .hero-content {
    width: calc(100% - 1.4rem);
    padding: 1.2rem 0 3.1rem;
  }
  .hero h1 {
    max-width: none;
    font-size: clamp(2.2rem, 10.2vw, 3.45rem);
    line-height: 0.96;
    letter-spacing: -0.045em;
    text-wrap: balance;
  }
  .hero-text {
    max-width: none;
    margin-top: 1rem;
    font-size: 0.98rem;
    line-height: 1.72;
  }

''',
        '''  .hero-panel { right: 0.9rem; left: 0.9rem; bottom: 0.9rem; max-width: none; }

''',
        "responsive 760",
    )

    styles = replace_once(
        styles,
        '''  .hero { grid-template-columns: minmax(440px,1fr) minmax(540px,0.9fr); }

  .section,
''',
        '''  .section,
''',
        "responsive 1280 estructura",
    )

    styles = replace_once(
        styles,
        '''  .hero-content {
    width: auto;
    max-width: 46rem;
    margin-left: 0;
    margin-right: auto;
    padding: 2rem 2.8rem 4.5rem 2.2rem;
  }
''',
        "",
        "responsive 1280 contenido",
    )

    styles = replace_once(
        styles,
        '''.hero-text,
.hero-panel p,''',
        '''.hero-panel p,''',
        "alineación de texto",
    )

    conversion = replace_once(
        conversion,
        '''/* Conversion and commercial presentation helpers */
.home-conversion-hero {
  padding-top: 0;
}

.home-conversion-hero .hero-content {
  align-items: flex-start;
  text-align: left;
}

.home-conversion-hero .hero-brand,
.home-conversion-hero .eyebrow,
.home-conversion-hero .hero h1,
.home-conversion-hero .hero-text {
  margin-inline: 0;
}

.home-conversion-hero .hero h1 {
  max-width: 15ch;
}

.home-conversion-hero .hero-actions {
  justify-content: flex-start;
}

.home-conversion-hero .hero-points {
  width: 100%;
}

''',
        '''/* Conversion and commercial presentation helpers */
''',
        "conversion principal",
    )

    conversion = replace_once(
        conversion,
        '''@media (max-width: 1080px) {
  .home-conversion-hero .hero-content {
    order: -1;
  }

  .home-conversion-hero .hero-media {
    order: initial;
    min-height: 42svh;
  }
}

''',
        "",
        "conversion responsive 1080",
    )

    conversion = replace_once(
        conversion,
        '''  .home-conversion-hero .hero {
    padding-top: 5.2rem;
  }

''',
        "",
        "conversion responsive 760 estructura",
    )

    conversion = replace_once(
        conversion,
        '''  .home-conversion-hero .hero-actions .button {
    width: 100%;
    justify-content: center;
    text-align: center;
  }

''',
        "",
        "conversion responsive 760 botones",
    )

    index = replace_once(
        index,
        '''  <link rel="stylesheet" href="conversion.css">''',
        '''  <link rel="stylesheet" href="conversion.css">
  <link rel="stylesheet" href="hero.css">''',
        "referencia de hero.css",
    )

    service_worker = replace_once(
        service_worker,
        '''const CACHE_VERSION = "mi-casa-segura-pwa-v8";''',
        '''const CACHE_VERSION = "mi-casa-segura-pwa-v9";''',
        "versión del caché",
    )
    service_worker = replace_once(
        service_worker,
        '''  "/conversion.css",''',
        '''  "/conversion.css",
  "/hero.css",''',
        "APP_SHELL de hero.css",
    )

    STYLES.write_text(styles, encoding="utf-8")
    CONVERSION.write_text(conversion, encoding="utf-8")
    INDEX.write_text(index, encoding="utf-8")
    SERVICE_WORKER.write_text(service_worker, encoding="utf-8")
    print("Portada extraída hacia hero.css de forma determinista.")


if __name__ == "__main__":
    main()
