#!/usr/bin/env python3
"""Comprueba CSS, HTML extendido, JavaScript, manifest y service worker."""

from __future__ import annotations

import json
import mimetypes
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import tinycss2
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IGNORED_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript", "blob"}
CSS_URL_RE = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE | re.DOTALL)
APP_SHELL_RE = re.compile(
    r"const\s+APP_SHELL\s*=\s*\[(?P<body>.*?)\]\s*;",
    re.DOTALL,
)
QUOTED_VALUE_RE = re.compile(r"(['\"])(.*?)\1", re.DOTALL)
JS_RESOURCE_RE = re.compile(
    r"""(?P<quote>['"`])(?P<path>(?:(?:/|\./|\.\./)[^'"`\s?#]+|[^'"`\s?#]+/[^'"`\s?#]+)"""
    r"""\.(?:css|js|png|jpe?g|webp|ico|svg|html|json|webmanifest)"""
    r"""(?:\?[^'"`]*)?)(?P=quote)""",
    re.IGNORECASE,
)
MIME_BY_SUFFIX = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".ico": "image/x-icon",
    ".svg": "image/svg+xml",
}


class ExtendedHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, str]] = []
        self.inline_css: list[str] = []
        self._inside_style = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        for attribute in ("href", "src", "poster"):
            value = attributes.get(attribute)
            if value:
                self.references.append((attribute, value.strip()))

        srcset = attributes.get("srcset")
        if srcset:
            for candidate in srcset.split(","):
                value = candidate.strip().split(maxsplit=1)[0]
                if value:
                    self.references.append(("srcset", value))

        style = attributes.get("style")
        if style:
            self.inline_css.append(style)

        if tag.lower() == "style":
            self._inside_style = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "style":
            self._inside_style = False

    def handle_data(self, data: str) -> None:
        if self._inside_style and data.strip():
            self.inline_css.append(data)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def resolve_reference(source: Path, raw_reference: str) -> Path | None:
    reference = raw_reference.strip()
    if not reference or reference.startswith("#") or reference.startswith("//"):
        return None

    parsed = urlsplit(reference)
    if parsed.scheme.lower() in IGNORED_SCHEMES or parsed.netloc:
        return None

    clean_path = unquote(parsed.path)
    if not clean_path:
        return None

    if clean_path == "/":
        return ROOT / "index.html"

    if clean_path.startswith("/"):
        target = ROOT / clean_path.lstrip("/")
    else:
        target = source.parent / clean_path

    target = target.resolve()
    if target.is_dir() or clean_path.endswith("/"):
        target = target / "index.html"
    return target


def validate_reference(source: Path, kind: str, reference: str) -> str | None:
    target = resolve_reference(source, reference)
    if target is None:
        return None

    try:
        target.relative_to(ROOT)
    except ValueError:
        return f"{relative(source)}: {kind} sale del repositorio: {reference}"

    if not target.exists():
        return f"{relative(source)}: falta el recurso de {kind}: {reference}"

    return None


def css_reference_errors(source: Path, text: str, kind: str = "url() CSS") -> list[str]:
    errors: list[str] = []
    for match in CSS_URL_RE.finditer(text):
        reference = match.group(2).strip()
        error = validate_reference(source, kind, reference)
        if error:
            errors.append(error)
    return errors


def check_html() -> list[str]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        parser = ExtendedHTMLParser()
        try:
            parser.feed(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{relative(path)}: HTML no analizable: {type(exc).__name__}: {exc}")
            continue

        for kind, reference in parser.references:
            error = validate_reference(path, kind, reference)
            if error:
                errors.append(error)

        for inline_css in parser.inline_css:
            errors.extend(css_reference_errors(path, inline_css, "url() CSS inline"))
    return errors


def check_css() -> list[str]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.css")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        rules = tinycss2.parse_stylesheet(text, skip_comments=False, skip_whitespace=False)
        for token in rules:
            if token.type == "error":
                errors.append(
                    f"{relative(path)}:{token.source_line}:{token.source_column}: "
                    f"CSS inválido: {token.message}"
                )

        errors.extend(css_reference_errors(path, text))

        for rule in rules:
            if getattr(rule, "type", None) == "at-rule" and rule.lower_at_keyword == "import":
                serialized = tinycss2.serialize(rule.prelude).strip()
                match = re.search(r"(?:url\()?['\"]?([^'\"\s)]+)", serialized)
                if match:
                    error = validate_reference(path, "@import", match.group(1))
                    if error:
                        errors.append(error)
    return errors


def check_javascript_references() -> list[str]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.js")):
        if ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for match in JS_RESOURCE_RE.finditer(text):
            reference = match.group("path")
            if "${" in reference or "{" in reference:
                continue
            error = validate_reference(path, "ruta JavaScript", reference)
            if error:
                errors.append(error)
    return errors


def validate_manifest_image(
    manifest_path: Path,
    item: dict[str, object],
    label: str,
) -> list[str]:
    errors: list[str] = []
    source = item.get("src")
    if not isinstance(source, str):
        return errors

    error = validate_reference(manifest_path, label, source)
    if error:
        return [error]

    target = resolve_reference(manifest_path, source)
    if target is None:
        return errors

    declared_type = item.get("type")
    expected_type = MIME_BY_SUFFIX.get(target.suffix.lower()) or mimetypes.guess_type(target.name)[0]
    if isinstance(declared_type, str) and expected_type and declared_type != expected_type:
        errors.append(
            f"{relative(manifest_path)}: {label} declara {declared_type}; "
            f"el archivo corresponde a {expected_type}"
        )

    declared_sizes = item.get("sizes")
    if isinstance(declared_sizes, str) and declared_sizes != "any":
        declared = {
            tuple(int(value) for value in size.lower().split("x", 1))
            for size in declared_sizes.split()
            if re.fullmatch(r"\d+x\d+", size.lower())
        }
        if declared:
            try:
                with Image.open(target) as image:
                    actual_size = image.size
            except Exception as exc:
                errors.append(
                    f"{relative(manifest_path)}: no se pudo abrir {label}: "
                    f"{type(exc).__name__}: {exc}"
                )
            else:
                if actual_size not in declared:
                    errors.append(
                        f"{relative(manifest_path)}: {label} mide {actual_size}; "
                        f"declara {declared_sizes}"
                    )
    return errors


def check_manifest() -> list[str]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.webmanifest")):
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{relative(path)}: manifest inválido: {type(exc).__name__}: {exc}")
            continue

        for key in ("start_url", "scope"):
            value = manifest.get(key)
            if not isinstance(value, str):
                errors.append(f"{relative(path)}: falta o es inválido {key}")
                continue
            if key == "scope":
                target = resolve_reference(path, value)
                if target and not target.parent.exists() and not target.exists():
                    errors.append(f"{relative(path)}: scope inexistente: {value}")
            else:
                error = validate_reference(path, key, value)
                if error:
                    errors.append(error)

        icons = manifest.get("icons", [])
        if not isinstance(icons, list) or not icons:
            errors.append(f"{relative(path)}: icons debe ser una lista no vacía")
        else:
            for index, item in enumerate(icons):
                if not isinstance(item, dict):
                    errors.append(f"{relative(path)}: icons[{index}] debe ser un objeto")
                    continue
                errors.extend(validate_manifest_image(path, item, f"icons[{index}]"))

        screenshots = manifest.get("screenshots", [])
        if not isinstance(screenshots, list):
            errors.append(f"{relative(path)}: screenshots debe ser una lista")
        else:
            for index, item in enumerate(screenshots):
                if isinstance(item, dict):
                    errors.extend(validate_manifest_image(path, item, f"screenshots[{index}]"))
                else:
                    errors.append(f"{relative(path)}: screenshots[{index}] debe ser un objeto")

        shortcuts = manifest.get("shortcuts", [])
        if not isinstance(shortcuts, list):
            errors.append(f"{relative(path)}: shortcuts debe ser una lista")
        else:
            for index, item in enumerate(shortcuts):
                if not isinstance(item, dict):
                    errors.append(f"{relative(path)}: shortcuts[{index}] debe ser un objeto")
                    continue
                url = item.get("url")
                if isinstance(url, str):
                    error = validate_reference(path, f"shortcuts[{index}].url", url)
                    if error:
                        errors.append(error)
                else:
                    errors.append(f"{relative(path)}: shortcuts[{index}] no tiene url válida")
                shortcut_icons = item.get("icons", [])
                if not isinstance(shortcut_icons, list):
                    errors.append(
                        f"{relative(path)}: shortcuts[{index}].icons debe ser una lista"
                    )
                    continue
                for icon_index, icon in enumerate(shortcut_icons):
                    if isinstance(icon, dict):
                        errors.extend(
                            validate_manifest_image(
                                path,
                                icon,
                                f"shortcuts[{index}].icons[{icon_index}]",
                            )
                        )
                    else:
                        errors.append(
                            f"{relative(path)}: shortcuts[{index}].icons[{icon_index}] "
                            "debe ser un objeto"
                        )
    return errors


def check_service_worker() -> list[str]:
    errors: list[str] = []
    path = ROOT / "service-worker.js"
    if not path.exists():
        return ["Falta service-worker.js"]

    text = path.read_text(encoding="utf-8")
    match = APP_SHELL_RE.search(text)
    if not match:
        return ["service-worker.js: no se encontró APP_SHELL"]

    entries = [value for _, value in QUOTED_VALUE_RE.findall(match.group("body"))]
    duplicates = sorted({entry for entry in entries if entries.count(entry) > 1})
    errors.extend(f"service-worker.js: entrada duplicada en APP_SHELL: {entry}" for entry in duplicates)

    for entry in entries:
        error = validate_reference(path, "APP_SHELL", entry)
        if error:
            errors.append(error)
    return errors


def main() -> int:
    errors = [
        *check_html(),
        *check_css(),
        *check_javascript_references(),
        *check_manifest(),
        *check_service_worker(),
    ]

    if errors:
        print("Resource integrity checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Resource integrity checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
