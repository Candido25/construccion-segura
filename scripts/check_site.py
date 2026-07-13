#!/usr/bin/env python3
"""Small dependency-free checks for the static Construcción Segura site."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
IGNORED_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}
FORBIDDEN_PUBLIC_PHRASES = {
    "técnico en edificaciones": "La identidad pública debe priorizar Ingeniero civil y CIP N.° 364395.",
    "tecnico en edificaciones": "La identidad pública debe priorizar Ingeniero civil y CIP N.° 364395.",
    "sencico": "SENCICO no debe aparecer en las páginas públicas del sitio.",
}


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, str]] = []
        self.ids: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        element_id = attributes.get("id")
        if element_id:
            self.ids.append(element_id)

        for attribute in ("href", "src"):
            value = attributes.get(attribute)
            if value:
                self.references.append((attribute, value.strip()))


def resolve_local_reference(source: Path, raw_reference: str) -> Path | None:
    if not raw_reference or raw_reference.startswith("#") or raw_reference.startswith("//"):
        return None

    parsed = urlsplit(raw_reference)
    if parsed.scheme.lower() in IGNORED_SCHEMES or parsed.netloc:
        return None

    clean_path = unquote(parsed.path)
    if not clean_path:
        return None

    if clean_path.startswith("/"):
        target = ROOT / clean_path.lstrip("/")
    else:
        target = source.parent / clean_path

    return target.resolve()


def check_html_file(path: Path) -> list[str]:
    parser = SiteParser()
    source_text = path.read_text(encoding="utf-8")
    parser.feed(source_text)
    errors: list[str] = []

    seen_ids: set[str] = set()
    for element_id in parser.ids:
        if element_id in seen_ids:
            errors.append(f"{path.relative_to(ROOT)}: duplicate id #{element_id}")
        seen_ids.add(element_id)

    for attribute, reference in parser.references:
        target = resolve_local_reference(path, reference)
        if target is None:
            continue
        try:
            target.relative_to(ROOT)
        except ValueError:
            errors.append(
                f"{path.relative_to(ROOT)}: {attribute} escapes repository: {reference}"
            )
            continue

        if not target.exists():
            errors.append(
                f"{path.relative_to(ROOT)}: missing local target for {attribute}=\"{reference}\""
            )

    normalized_text = source_text.casefold()
    for phrase, explanation in FORBIDDEN_PUBLIC_PHRASES.items():
        if phrase in normalized_text:
            errors.append(
                f"{path.relative_to(ROOT)}: forbidden public phrase '{phrase}'. {explanation}"
            )

    return errors


def main() -> int:
    html_files = sorted(
        path for path in ROOT.rglob("*.html") if ".git" not in path.parts
    )
    all_errors: list[str] = []

    for html_file in html_files:
        all_errors.extend(check_html_file(html_file))

    if all_errors:
        print("Static site checks failed:", file=sys.stderr)
        for error in all_errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Static site checks passed for {len(html_files)} HTML files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
