from __future__ import annotations

from pathlib import Path
import json
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "backend" / "normativa_tecnica.json"
OUT = ROOT / "docs" / "DIAGNOSTICO_PUERTAS_VENTANAS_2026-07-27.md"

TERMINOS = [
    "puerta", "ventana", "mampara", "marco", "hoja", "cerradura", "cerrajeria",
    "bisagra", "herraje", "picaporte", "manija", "vano", "jamba", "dintel",
    "alféizar", "alfeizar", "rejilla", "baranda", "parapeto", "vidrio", "acristalamiento",
    "evacuacion", "evacuación", "cortafuego", "humo", "ventilacion", "ventilación",
    "carpinteria", "carpintería", "porton", "portón", "reja", "sellado", "burlete"
]


def normalizar(texto: str) -> str:
    base = unicodedata.normalize("NFD", str(texto or "").lower())
    return "".join(c for c in base if unicodedata.category(c) != "Mn")


def main() -> None:
    datos = json.loads(BASE.read_text(encoding="utf-8"))
    encontrados = []
    for item in datos["parametros"]:
        texto = normalizar(" ".join([
            item.get("id", ""), item.get("categoria", ""), item.get("elemento", ""),
            item.get("parametro", ""), item.get("valor", {}).get("texto", ""),
            item.get("fuente", {}).get("norma", ""), item.get("fuente", {}).get("numeral", "") or ""
        ]))
        if any(normalizar(t) in texto for t in TERMINOS):
            encontrados.append(item)

    lineas = [
        "# Diagnóstico de cobertura — puertas, ventanas y cerrajería",
        "",
        f"Versión revisada: `{datos['version']}`. Parámetros totales: `{len(datos['parametros'])}`.",
        f"Parámetros relacionados encontrados: `{len(encontrados)}`.",
        "",
    ]
    por_norma = {}
    for item in encontrados:
        norma = item.get("fuente", {}).get("norma", "Sin norma")
        por_norma.setdefault(norma, []).append(item)
    for norma, items in sorted(por_norma.items()):
        lineas += [f"## {norma} — {len(items)}", ""]
        for item in sorted(items, key=lambda x: x["id"]):
            numeral = item.get("fuente", {}).get("numeral") or "sin numeral"
            lineas.append(
                f"- `{item['id']}` | {item['categoria']} | {item['elemento']} | "
                f"{item['parametro']} | {numeral}"
            )
        lineas.append("")
    OUT.write_text("\n".join(lineas), encoding="utf-8")
    print(f"Diagnóstico generado: {len(encontrados)} parámetros relacionados.")


if __name__ == "__main__":
    main()
