from __future__ import annotations

from pathlib import Path
import json
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "backend" / "normativa_tecnica.json"
SALIDA = ROOT / "docs" / "DIAGNOSTICO_OBRAS_PRELIMINARES_2026-07-27.md"

TERMINOS = [
    "excavacion", "zanja", "entibado", "apuntalamiento", "tablestacado",
    "calzadura", "predio vecino", "edificacion vecina", "talud", "barrera",
    "obra provisional", "instalacion provisional", "cerco", "guardiania",
    "servicio higienico", "comedor", "vestuario", "agua potable",
    "energia provisional", "puesta a tierra", "transito peatonal",
    "proteccion colectiva", "orden y limpieza", "acopio", "andamio",
    "demolicion", "plan de seguridad", "botiquin", "emergencia",
]


def normalizar(texto: str) -> str:
    base = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in base if unicodedata.category(c) != "Mn")


def main() -> None:
    datos = json.loads(BASE.read_text(encoding="utf-8"))
    parametros = datos["parametros"]
    lineas = [
        "# Diagnóstico de cobertura existente — obras preliminares y seguridad",
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
    lineas.extend(["## Total de parámetros únicos relacionados", "", f"`{len(ids)}`", ""])
    SALIDA.write_text("\n".join(lineas), encoding="utf-8")
    print(f"Diagnóstico generado con {len(ids)} parámetros únicos relacionados.")


if __name__ == "__main__":
    main()
