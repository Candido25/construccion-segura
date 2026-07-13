#!/usr/bin/env python3
"""One-time migration: prioritize the public identity as civil engineer."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_all(path: Path, replacements: list[tuple[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")


# Replacements shared by technical articles and case-study pages.
shared_html_replacements = [
    (
        '"description":"CIP N.° 364395 y Técnico en Edificaciones — SENCICO"',
        '"description":"Ingeniero civil colegiado, CIP N.° 364395"',
    ),
    (
        '<span>CIP N.° 364395 · Técnico en Edificaciones — SENCICO</span>',
        '<span>Ingeniero civil · CIP N.° 364395</span>',
    ),
    (
        'CIP N.° 364395 · Técnico en Edificaciones — SENCICO',
        'Ingeniero civil · CIP N.° 364395',
    ),
]

for html_file in ROOT.rglob("*.html"):
    replace_all(html_file, shared_html_replacements)

file_replacements: dict[str, list[tuple[str, str]]] = {
    "index.html": [
        (
            '"description": "Ingeniero civil CIP N.° 364395 y técnico en Edificaciones formado en SENCICO."',
            '"description": "Ingeniero civil colegiado, CIP N.° 364395, especializado en orientación técnica para propietarios."',
        ),
        (
            '<p>CIP N.° 364395<br>Técnico en Edificaciones — SENCICO</p>',
            '<p>Ingeniero civil<br>CIP N.° 364395</p>',
        ),
        (
            '<article><strong>Formación técnica</strong><span>Técnico en Edificaciones — SENCICO</span></article>',
            '<article><strong>Criterio profesional</strong><span>Orientación basada en normativa peruana y experiencia de obra</span></article>',
        ),
        ('            <span>Técnico en Edificaciones — SENCICO</span>\n', ''),
        (
            'antes de complementar esa experiencia con formación técnica y universitaria.',
            'antes de complementar esa experiencia práctica con formación universitaria en ingeniería civil.',
        ),
    ],
    "nosotros.html": [
        (
            'content="Conoce al responsable de Construcción Segura: Omar Oswaldo Alcantara Aquino, ingeniero civil CIP 364395 y técnico en Edificaciones formado en SENCICO."',
            'content="Conoce al responsable de Construcción Segura: Omar Oswaldo Alcantara Aquino, ingeniero civil colegiado, CIP N.° 364395, con experiencia práctica vinculada a la ejecución de obra."',
        ),
        (
            'content="Omar Oswaldo Alcantara Aquino, ingeniero civil, CIP 364395, técnico en edificaciones SENCICO, Construcción Segura"',
            'content="Omar Oswaldo Alcantara Aquino, ingeniero civil, CIP 364395, asesoría técnica de obra, Construcción Segura"',
        ),
        (
            'content="Experiencia práctica de obra, formación técnica en SENCICO y respaldo profesional como ingeniero civil."',
            'content="Experiencia práctica de obra y respaldo profesional como ingeniero civil colegiado."',
        ),
        (
            '<h1>Experiencia práctica de obra, formación técnica y respaldo profesional.</h1>',
            '<h1>Experiencia práctica de obra y respaldo profesional como ingeniero civil.</h1>',
        ),
        (
            '<p>Construcción Segura es dirigida por Omar Oswaldo Alcantara Aquino, ingeniero civil, CIP N.° 364395, y técnico en Edificaciones formado en SENCICO.</p>',
            '<p>Construcción Segura es dirigida por Omar Oswaldo Alcantara Aquino, ingeniero civil colegiado, CIP N.° 364395.</p>',
        ),
        (
            '<article class="quick-link-card"><strong>Formación técnica</strong><span>Técnico en Edificaciones — SENCICO.</span></article>',
            '<article class="quick-link-card"><strong>Experiencia de obra</strong><span>Conocimiento directo de procesos constructivos y autoconstrucción.</span></article>',
        ),
        (
            '<p>Posteriormente se formó como técnico en Edificaciones en SENCICO y como ingeniero civil. Esa trayectoria permite comprender el lenguaje del propietario y del maestro de obra, y al mismo tiempo revisar decisiones con criterio técnico y normativo.</p>',
            '<p>Posteriormente obtuvo el título de ingeniero civil. La combinación de experiencia práctica y formación profesional permite comprender el lenguaje del propietario y del maestro de obra, y al mismo tiempo revisar decisiones con criterio técnico y normativo.</p>',
        ),
    ],
    "servicios.html": [
        (
            '<article class="quick-link-card"><strong>Experiencia práctica</strong><span>Técnico en Edificaciones — SENCICO y trayectoria vinculada a la ejecución de obra.</span></article>',
            '<article class="quick-link-card"><strong>Experiencia práctica</strong><span>Trayectoria vinculada a la ejecución de obra y la autoconstrucción.</span></article>',
        ),
    ],
    "contacto.html": [
        (
            '<p>Ing. Civil Omar Oswaldo Alcantara Aquino, CIP N.° 364395. Técnico en Edificaciones — SENCICO. Las condiciones y entregables se confirman antes de iniciar.</p>',
            '<p>Ing. Civil Omar Oswaldo Alcantara Aquino, CIP N.° 364395. Las condiciones y entregables se confirman antes de iniciar.</p>',
        ),
    ],
    "condiciones-servicio.html": [
        (
            '<p>La atención está a cargo de <strong>Omar Oswaldo Alcantara Aquino</strong>, ingeniero civil, CIP N.° 364395, y Técnico en Edificaciones — SENCICO.</p>',
            '<p>La atención está a cargo de <strong>Omar Oswaldo Alcantara Aquino</strong>, ingeniero civil colegiado, CIP N.° 364395.</p>',
        ),
    ],
}

for relative_path, replacements in file_replacements.items():
    replace_all(ROOT / relative_path, replacements)

agents_path = ROOT / "AGENTS.md"
replace_all(
    agents_path,
    [
        ('- Formación técnica: Técnico en Edificaciones — SENCICO\n', ''),
        (
            '- Profesión: Ingeniero civil\n- CIP: 364395\n',
            '- Profesión e identidad pública principal: Ingeniero civil\n- CIP: 364395\n- Presentación pública: **Ing. Civil Omar Oswaldo Alcantara Aquino · CIP N.° 364395**\n- No mostrar SENCICO ni el título técnico en páginas públicas, firmas, metadatos o datos estructurados.\n',
        ),
    ],
)

forbidden = ("técnico en edificaciones", "tecnico en edificaciones", "sencico")
remaining: list[str] = []
for html_file in ROOT.rglob("*.html"):
    text = html_file.read_text(encoding="utf-8").casefold()
    if any(term in text for term in forbidden):
        remaining.append(str(html_file.relative_to(ROOT)))

if remaining:
    print("Remaining retired credentials:")
    for item in sorted(remaining):
        print(f"- {item}")
else:
    print("Public identity updated across all HTML files.")
