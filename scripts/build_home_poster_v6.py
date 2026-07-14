#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import re

root = Path(__file__).resolve().parents[1]
source = root / 'assets/brand/portada-principal-construccion-segura.webp'
raw = bytearray(source.read_bytes())
if raw[:4] != b'RIFF':
    raise SystemExit('Fuente sin cabecera RIFF válida.')
raw[8:12] = b'WEBP'
repaired = root / 'assets/brand/portada-fuente-v6.webp'
repaired.write_bytes(raw)
with Image.open(repaired) as opened:
    base = opened.convert('RGB')

# Escritorio 16:9, conservando el afiche completo.
target = (1920, 1080)
scale = max(target[0] / base.width, target[1] / base.height)
bg = base.resize((round(base.width * scale), round(base.height * scale)), Image.Resampling.LANCZOS)
left = (bg.width - target[0]) // 2
top = (bg.height - target[1]) // 2
bg = bg.crop((left, top, left + target[0], top + target[1])).filter(ImageFilter.GaussianBlur(45))
bg = ImageEnhance.Brightness(bg).enhance(1.02).convert('RGBA')
fg_width = round(base.width * target[1] / base.height)
fg = base.resize((fg_width, target[1]), Image.Resampling.LANCZOS).convert('RGBA')
mask = Image.new('L', fg.size, 255)
px = mask.load()
for x in range(50):
    alpha = int(255 * x / 50)
    for y in range(mask.height):
        px[x, y] = alpha
        px[mask.width - 1 - x, y] = alpha
fg.putalpha(mask)
bg.alpha_composite(fg, ((target[0] - fg_width) // 2, 0))
desktop = root / 'assets/brand/portada-construccion-segura-escritorio-v6.webp'
bg.convert('RGB').save(desktop, 'WEBP', quality=88, method=6)

# Móvil: recorte visual limpio; los textos y botones permanecen en HTML.
crop = base.crop((600, 0, 1536, 900))
mobile_img = ImageOps.fit(crop, (900, 1000), method=Image.Resampling.LANCZOS, centering=(0.52, 0.5))
mobile = root / 'assets/brand/portada-construccion-segura-movil-v6.webp'
mobile_img.save(mobile, 'WEBP', quality=86, method=6)

for path, expected in [(desktop, (1920, 1080)), (mobile, (900, 1000))]:
    with Image.open(path) as check:
        check.verify()
    with Image.open(path) as check:
        if check.size != expected or check.format != 'WEBP':
            raise SystemExit(f'Imagen inválida: {path}')

index = root / 'index.html'
html = index.read_text(encoding='utf-8')
html, n = re.subn(
    r'\s*<link rel="preload" as="image" href="assets/site-photos/web/hero-portada\.webp[^>]*>\s*<link rel="stylesheet" href="conversion\.css[^\"]*">\s*<style>.*?</style>',
    '\n  <link rel="preload" as="image" href="/assets/brand/portada-construccion-segura-escritorio-v6.webp" type="image/webp" media="(min-width: 901px)">\n  <link rel="preload" as="image" href="/assets/brand/portada-construccion-segura-movil-v6.webp" type="image/webp" media="(max-width: 900px)">\n  <link rel="stylesheet" href="conversion.css?v=20260714-6">',
    html,
    count=1,
    flags=re.S,
)
if n != 1:
    raise SystemExit('No se encontró el bloque antiguo del encabezado.')
html = html.replace('https://www.construccionsegura.org.pe/assets/brand/logo-marca-construccion-segura-web.png', 'https://www.construccionsegura.org.pe/assets/brand/portada-construccion-segura-escritorio-v6.webp')
html, n = re.subn(
    r'\s*<div class="hero-media hero-media-brand"[^>]*>\s*<div class="hero-image"></div>\s*</div>',
    '''\n      <div class="hero-poster-frame">\n        <picture class="hero-poster">\n          <source media="(max-width: 900px)" srcset="/assets/brand/portada-construccion-segura-movil-v6.webp">\n          <img src="/assets/brand/portada-construccion-segura-escritorio-v6.webp" width="1920" height="1080" alt="Construcción Segura: vivienda, casco, planos y orientación técnica para propietarios" fetchpriority="high" decoding="async">\n        </picture>\n        <div class="hero-poster-hotspots" aria-label="Acciones de la portada">\n          <a class="hero-poster-hotspot hero-poster-whatsapp" href="https://wa.me/51968481482?text=Hola%2C%20necesito%20revisar%20mi%20obra.%20La%20obra%20est%C3%A1%20en%20___%2C%20se%20encuentra%20en%20la%20etapa%20de%20___%20y%20mi%20principal%20duda%20es%20___." target="_blank" rel="noreferrer" data-track="whatsapp_hero_poster" aria-label="Consultar mi obra por WhatsApp">Consultar mi obra</a>\n          <a class="hero-poster-hotspot hero-poster-services" href="#servicios" data-track="view_prices_hero_poster" aria-label="Ver servicios y precios">Ver servicios y precios</a>\n        </div>\n      </div>''',
    html,
    count=1,
    flags=re.S,
)
if n != 1:
    raise SystemExit('No se encontró el bloque antiguo de imagen.')
html = html.replace('<section class="hero">', '<section class="hero hero-poster-section">', 1)
html = html.replace('<div class="hero-content">', '<div class="hero-content hero-content-mobile">', 1)
html = re.sub(r'/site-global\.js\?v=[^\"]+', '/site-global.js?v=20260714-6', html)
html = re.sub(r'script\.js\?v=[^\"]+', 'script.js?v=20260714-6', html)
index.write_text(html, encoding='utf-8')

css_path = root / 'conversion.css'
css = css_path.read_text(encoding='utf-8')
marker = '/* Branded homepage hero — approved July 2026 */'
if marker not in css:
    raise SystemExit('No se encontró el bloque antiguo de estilos.')
css = css.split(marker, 1)[0].rstrip() + '''\n\n/* Branded homepage hero — full-screen poster v6 */\n.home-conversion-hero .hero.hero-poster-section {\n  --home-header-height: 4.7rem; width: 100%; min-height: 100svh; height: 100svh;\n  padding: var(--home-header-height) 0 0; display: flex; align-items: center; justify-content: center;\n  overflow: hidden; background: #f4f1eb;\n}\n.home-conversion-hero .hero-poster-frame {\n  position: relative; width: min(100vw, calc((100svh - var(--home-header-height)) * 16 / 9));\n  height: min(calc(100svh - var(--home-header-height)), calc(100vw * 9 / 16));\n  max-width: 100vw; max-height: calc(100svh - var(--home-header-height)); aspect-ratio: 16 / 9;\n  margin: 0 auto; background: #f4f1eb;\n}\n.home-conversion-hero .hero-poster, .home-conversion-hero .hero-poster img { display: block; width: 100%; height: 100%; }\n.home-conversion-hero .hero-poster img { object-fit: contain; object-position: center; }\n.home-conversion-hero .hero-content-mobile { display: none; }\n.home-conversion-hero .hero-poster-hotspots { position: absolute; inset: 0; pointer-events: none; }\n.home-conversion-hero .hero-poster-hotspot { position: absolute; z-index: 3; display: block; overflow: hidden; border-radius: .75rem; color: transparent; font-size: 0; pointer-events: auto; }\n.home-conversion-hero .hero-poster-hotspot:focus-visible { outline: 3px solid #fff; outline-offset: 2px; box-shadow: 0 0 0 6px #0f2744; }\n.home-conversion-hero .hero-poster-whatsapp { left: 11.5%; top: 64.5%; width: 14.3%; height: 6.8%; }\n.home-conversion-hero .hero-poster-services { left: 26.7%; top: 64.5%; width: 16.3%; height: 6.8%; }\n@media (max-width: 900px) {\n  .home-conversion-hero .hero.hero-poster-section { min-height: 0; height: auto; padding-top: 4.8rem; display: block; overflow: visible; }\n  .home-conversion-hero .hero-poster-frame { width: 100%; height: auto; max-height: none; aspect-ratio: 9 / 10; }\n  .home-conversion-hero .hero-poster img { object-fit: cover; }\n  .home-conversion-hero .hero-poster-hotspots { display: none; }\n  .home-conversion-hero .hero-content-mobile { display: flex; width: min(100%, calc(100% - 1.4rem)); min-height: 0; max-width: 46rem; margin: 0 auto; padding: 1.5rem .35rem 2.2rem; align-items: flex-start; text-align: left; }\n  .home-conversion-hero .hero-content-mobile .hero-brand, .home-conversion-hero .hero-content-mobile .eyebrow, .home-conversion-hero .hero-content-mobile h1, .home-conversion-hero .hero-content-mobile .hero-text { margin-inline: 0; }\n}\n'''
css_path.write_text(css, encoding='utf-8')

js_path = root / 'site-global.js'
js = js_path.read_text(encoding='utf-8')
js = re.sub(r'\n\s*const HERO_BRAND_DATA_URI = .*?;\n\s*const HERO_BRAND_ALT = .*?;\n', '\n', js, count=1, flags=re.S)
js = re.sub(r'\n\s*const ensureHeroStyle = \(\) => \{.*?\n\s*const applyGlobalEnhancements =', '\n\n  const applyGlobalEnhancements =', js, count=1, flags=re.S)
js = js.replace('    applyHeroBrandImage();\n', '')
js_path.write_text(js, encoding='utf-8')

repaired.unlink(missing_ok=True)
print('Portada v6 generada y documentos actualizados.')
