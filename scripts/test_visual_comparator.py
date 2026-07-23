#!/usr/bin/env python3
"""Pruebas mínimas del criterio de regresión visual."""

from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "compare_screenshots.py"
TEST_ROOT = ROOT / "visual-artifacts" / "comparator-self-test"


def load_comparator():
    specification = importlib.util.spec_from_file_location("visual_comparator", MODULE_PATH)
    if specification is None or specification.loader is None:
        raise RuntimeError("No se pudo cargar compare_screenshots.py")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def save_pair(name: str, baseline: Image.Image, current: Image.Image) -> tuple[Path, Path]:
    directory = TEST_ROOT / name
    directory.mkdir(parents=True, exist_ok=True)
    baseline_path = directory / "baseline.png"
    current_path = directory / "current.png"
    baseline.save(baseline_path)
    current.save(current_path)
    return current_path, baseline_path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    shutil.rmtree(TEST_ROOT, ignore_errors=True)
    comparator = load_comparator()

    white = Image.new("RGB", (100, 100), "white")

    current_path, baseline_path = save_pair("identical", white.copy(), white.copy())
    identical = comparator.compare_images(current_path, baseline_path)
    require(identical["passed"], "Una captura idéntica debe ser aceptada")

    sparse = white.copy()
    sparse.putpixel((50, 50), (200, 200, 200))
    current_path, baseline_path = save_pair("sparse-interpolation", white.copy(), sparse)
    sparse_result = comparator.compare_images(current_path, baseline_path)
    require(sparse_result["passed"], "Una diferencia subpíxel aislada debe ser aceptada")

    broad = white.copy()
    ImageDraw.Draw(broad).rectangle((20, 20, 59, 59), fill=(250, 250, 250))
    current_path, baseline_path = save_pair("broad-subtle-change", white.copy(), broad)
    broad_result = comparator.compare_images(current_path, baseline_path)
    require(not broad_result["passed"], "Una región amplia modificada debe ser rechazada")

    contrast = white.copy()
    ImageDraw.Draw(contrast).rectangle((48, 48, 51, 51), fill="black")
    current_path, baseline_path = save_pair("high-contrast-change", white.copy(), contrast)
    contrast_result = comparator.compare_images(current_path, baseline_path)
    require(not contrast_result["passed"], "Una modificación de alto contraste debe ser rechazada")

    different_size = Image.new("RGB", (101, 100), "white")
    current_path, baseline_path = save_pair("different-size", white.copy(), different_size)
    size_result = comparator.compare_images(current_path, baseline_path)
    require(not size_result["passed"], "Un cambio de dimensiones debe ser rechazado")

    print("Visual comparator self-tests passed.")


if __name__ == "__main__":
    main()
