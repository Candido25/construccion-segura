from __future__ import annotations

from pathlib import Path
import json
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "backend" / "normativa_tecnica.json"
SALIDA = ROOT / "docs" / "DIAGNOSTICO_ACABADOS_2026-07-27.md"

TERMINOS = [
    "acabado", "tarrajeo", "revoque", "enlucido", "mortero", "revestimiento",
    "enchape", "ceramico", "porcelanato", "pepelma", "fachaleta", "zocalo",
    "contrazocalo", "contrapiso", "falso piso", "piso", "junta", "fragua",
    "adhesivo", "pintura", "sellador", "imprimante", "empaste", "barniz",
    "laca", "cielorraso", "drywall", "yeso", "humedad", "eflorescencia",
    "fisura", "planeidad", "aplomo", "tolerancia", "carpinteria", "vidrio",
    "puerta", "ventana", "madera", "metal", "corrosion", "impermeabilizacion",
]

NORMAS = ["A.010", "A.020", "A.120", "E.040", "E.060", "E.070", "GE.030", "GE.040"]


def normalizar(texto: str) -> str:
    base = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in base if unicodedata.category(c) != "Mn")


def main() -> None:
    datos = json.loads(BASE.read_text(encoding="utf-8"))
    parametros = datos["parametros"]
    lineas = [
        "# Diagnóstico de cobertura existente — acabados",
        "",
        f"Versión revisada: `{datos['version']}`. Parámetros totales: `{len(parametros)}`.",
        "",
    ]
    ids = set()
    for termino in TERMINOS:
        coincidencias = []
        for item in parametros:
            texto = normalizar(json.dumps(item, ensure_ascii=False))
            if termino in texto:
                coincidencias.append(item)
                ids.add(item["id"])
        lineas.extend([f"## {termino} — {len(coincidencias)}", ""])
        for item in coincidencias:
            lineas.append(
                f"- `{item['id']}` | {item['categoria']} | {item['elemento']} | {item['parametro']} | {item['fuente']['norma']} {item['fuente'].get('numeral') or ''}"
            )
        lineas.append("")

    lineas.extend(["## Inventario por normas relacionadas", ""])
    for norma in NORMAS:
        coincidencias = [
            item for item in parametros
            if normalizar(str(item.get("fuente", {}).get("norma", ""))).startswith(normalizar(norma))
        ]
        lineas.extend([f"### {norma} — {len(coincidencias)}", ""])
        for item in coincidencias:
            texto = normalizar(json.dumps(item, ensure_ascii=False))
            if any(termino in texto for termino in TERMINOS):
                lineas.append(
                    f"- `{item['id']}` | {item['categoria']} | {item['elemento']} | {item['parametro']} | {item['fuente'].get('numeral') or ''}"
                )
        lineas.append("")

    lineas.extend(["## Total de parámetros únicos relacionados", "", f"`{len(ids)}`", ""])
    SALIDA.write_text("\n".join(lineas), encoding="utf-8")
    print(f"Diagnóstico generado con {len(ids)} parámetros únicos relacionados.")


if __name__ == "__main__":
    main()
