#!/usr/bin/env python3
"""One-time migration: show the professional identity simply as Ingeniero."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = [
    ("Ingeniero Civil colegiado", "Ingeniero colegiado"),
    ("Ingeniero civil colegiado", "Ingeniero colegiado"),
    ("ingeniero civil colegiado", "ingeniero colegiado"),
    ("ING. CIVIL", "ING."),
    ("Ing. Civil", "Ing."),
    ("Ingeniero Civil", "Ingeniero"),
    ("Ingeniero civil", "Ingeniero"),
    ("ingeniero civil", "ingeniero"),
    ("Ingeniería Civil", "Ingeniería"),
    ("ingeniería civil", "ingeniería"),
]


def replace_in_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    updated = text
    for old, new in REPLACEMENTS:
        updated = updated.replace(old, new)
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


changed = []
for html_file in ROOT.rglob("*.html"):
    if replace_in_file(html_file):
        changed.append(str(html_file.relative_to(ROOT)))

agents = ROOT / "AGENTS.md"
if agents.exists() and replace_in_file(agents):
    changed.append("AGENTS.md")

check_path = ROOT / "scripts/check_site.py"
check_text = check_path.read_text(encoding="utf-8")
marker = "FORBIDDEN_PUBLIC_PHRASES = {\n"
entries = (
    '    "ing. civil": "La presentación pública debe usar Ing. y el nombre completo, sin mostrar la especialidad.",\n'
    '    "ingeniero civil": "La presentación pública debe usar Ingeniero y CIP N.° 364395, sin mostrar la especialidad.",\n'
)
if entries not in check_text:
    check_text = check_text.replace(marker, marker + entries, 1)
    check_path.write_text(check_text, encoding="utf-8")
    changed.append("scripts/check_site.py")

for html_file in ROOT.rglob("*.html"):
    normalized = html_file.read_text(encoding="utf-8").casefold()
    if "ing. civil" in normalized or "ingeniero civil" in normalized:
        raise SystemExit(f"Retired specialty remains in {html_file.relative_to(ROOT)}")

print(f"Updated {len(changed)} files.")
for path in changed:
    print(path)
