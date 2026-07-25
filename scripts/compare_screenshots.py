#!/usr/bin/env python3
"""Compara capturas actuales contra el punto de restauración estable."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "visual-artifacts"
CURRENT = ARTIFACTS / "current"
BASELINE = ARTIFACTS / "baseline"
DIFFS = ARTIFACTS / "diffs"
REPORT = ARTIFACTS / "comparison-report.json"

MAX_CHANGED_PIXEL_RATIO = 0.001
MAX_MEAN_ABSOLUTE_ERROR = 0.20


def compare_images(current_path: Path, baseline_path: Path) -> dict[str, object]:
    with Image.open(current_path) as current_image:
        current = current_image.convert("RGB")
    with Image.open(baseline_path) as baseline_image:
        baseline = baseline_image.convert("RGB")

    result: dict[str, object] = {
        "current": current_path.relative_to(ARTIFACTS).as_posix(),
        "baseline": baseline_path.relative_to(ARTIFACTS).as_posix(),
        "current_size": list(current.size),
        "baseline_size": list(baseline.size),
    }

    if current.size != baseline.size:
        result.update(
            {
                "passed": False,
                "reason": "Las capturas tienen dimensiones diferentes.",
                "changed_pixel_ratio": 1.0,
                "mean_absolute_error": 255.0,
            }
        )
        return result

    difference = ImageChops.difference(current, baseline)
    histogram = difference.histogram()
    pixels = current.width * current.height
    total_channel_difference = sum(
        value * count
        for channel in range(3)
        for value, count in enumerate(histogram[channel * 256 : (channel + 1) * 256])
    )
    mean_absolute_error = total_channel_difference / (pixels * 3)

    grayscale = difference.convert("L")
    changed_pixels = sum(count for value, count in enumerate(grayscale.histogram()) if value > 3)
    changed_pixel_ratio = changed_pixels / pixels

    passed = (
        changed_pixel_ratio <= MAX_CHANGED_PIXEL_RATIO
        and mean_absolute_error <= MAX_MEAN_ABSOLUTE_ERROR
    )

    result.update(
        {
            "passed": passed,
            "changed_pixel_ratio": changed_pixel_ratio,
            "mean_absolute_error": mean_absolute_error,
            "thresholds": {
                "maximum_changed_pixel_ratio": MAX_CHANGED_PIXEL_RATIO,
                "maximum_mean_absolute_error": MAX_MEAN_ABSOLUTE_ERROR,
            },
        }
    )

    if not passed:
        DIFFS.mkdir(parents=True, exist_ok=True)
        diff_path = DIFFS / current_path.name
        highlighted = ImageEnhance.Contrast(difference).enhance(5.0)
        highlighted.save(diff_path)
        result["diff"] = diff_path.relative_to(ARTIFACTS).as_posix()

    return result


def main() -> int:
    errors: list[str] = []
    comparisons: list[dict[str, object]] = []

    if not CURRENT.is_dir() or not BASELINE.is_dir():
        print("No se encontraron ambas carpetas de capturas.", file=sys.stderr)
        return 1

    current_files = sorted(CURRENT.glob("*.png"))
    baseline_names = {path.name for path in BASELINE.glob("*.png")}

    for current_path in current_files:
        baseline_path = BASELINE / current_path.name
        if not baseline_path.exists():
            errors.append(f"Falta captura base: {current_path.name}")
            continue

        comparison = compare_images(current_path, baseline_path)
        comparisons.append(comparison)
        if not comparison["passed"]:
            errors.append(
                f"{current_path.name}: diferencia visual "
                f"{comparison['changed_pixel_ratio']:.6f}, "
                f"MAE {comparison['mean_absolute_error']:.4f}"
            )

    current_names = {path.name for path in current_files}
    for extra_name in sorted(baseline_names - current_names):
        errors.append(f"Falta captura actual: {extra_name}")

    report = {
        "passed": not errors,
        "comparisons": comparisons,
        "errors": errors,
    }
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if errors:
        print("Visual regression comparison failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Visual regression comparison passed for {len(comparisons)} screenshots.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
