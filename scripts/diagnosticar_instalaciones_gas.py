from __future__ import annotations

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "backend" / "normativa_tecnica.json"
OUT = ROOT / "docs" / "DIAGNOSTICO_INSTALACIONES_GAS_2026-07-27.md"


def main() -> None:
    datos = json.loads(BASE.read_text(encoding="utf-8"))
    encontrados = []
    for item in datos.get("parametros", []):
        fuente = item.get("fuente", {})
        texto = " ".join([
            item.get("id", ""), item.get("categoria", ""), item.get("elemento", ""),
            item.get("parametro", ""), item.get("valor", {}).get("texto", ""),
            fuente.get("norma", ""), fuente.get("numeral", "") or ""
        ]).lower()
        if fuente.get("norma") == "EM.040" or any(t in texto for t in [
            "gas natural", "glp", "balón de gas", "balon de gas", "regulador", "válvula de gas",
            "valvula de gas", "artefacto a gas", "tubería de gas", "tuberia de gas", "hermeticidad"
        ]):
            encontrados.append(item)

    lineas = [
        "# Diagnóstico de cobertura — instalaciones de gas y combustión",
        "",
        f"Versión revisada: `{datos.get('version')}`. Parámetros totales: `{len(datos.get('parametros', []))}`.",
        f"Parámetros relacionados encontrados: `{len(encontrados)}`.",
        "",
    ]
    por_norma: dict[str, list[dict]] = {}
    for item in encontrados:
        norma = item.get("fuente", {}).get("norma", "Sin norma")
        por_norma.setdefault(norma, []).append(item)
    for norma, items in sorted(por_norma.items()):
        lineas += [f"## {norma} — {len(items)}", ""]
        for item in sorted(items, key=lambda x: x["id"]):
            fuente = item.get("fuente", {})
            lineas.append(
                f"- `{item['id']}` | {item['categoria']} | {item['elemento']} | "
                f"{item['parametro']} | {fuente.get('numeral') or 'sin numeral'} | "
                f"{item.get('valor', {}).get('texto', '')}"
            )
        lineas.append("")

    OUT.write_text("\n".join(lineas), encoding="utf-8")
    print(f"Diagnóstico generado: {len(encontrados)} parámetros relacionados.")


if __name__ == "__main__":
    main()
