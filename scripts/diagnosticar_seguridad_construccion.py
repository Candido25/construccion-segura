from __future__ import annotations

from pathlib import Path
import json
import unicodedata
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "backend" / "normativa_tecnica.json"
OUT = ROOT / "docs" / "DIAGNOSTICO_SEGURIDAD_CONSTRUCCION_2026-07-27.md"

TERMINOS = [
    "seguridad", "salud", "riesgo", "peligro", "accidente", "emergencia",
    "andamio", "escalera", "altura", "arnes", "arnés", "linea de vida", "línea de vida",
    "baranda", "rodapie", "rodapié", "plataforma", "abertura", "hueco", "borde",
    "excavacion", "excavación", "zanja", "talud", "entibado", "sostenimiento", "napa",
    "herramienta", "maquina", "máquina", "equipo", "guardas", "disco", "esmeril",
    "soldadura", "corte", "oxigeno", "oxígeno", "acetileno", "cilindro", "izaje", "grua", "grúa",
    "epp", "casco", "lente", "protector auditivo", "respirador", "guante", "calzado",
    "señalizacion", "señalización", "orden", "limpieza", "almacenamiento", "apilamiento",
    "electricidad provisional", "tablero provisional", "extintor", "incendio", "demolicion", "demolición",
    "espacio confinado", "permiso de trabajo", "bloqueo", "etiquetado", "vigia", "vigía",
    "transito", "tránsito", "vehiculo", "vehículo", "peaton", "peatón", "acceso",
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
            item.get("fuente", {}).get("norma", ""), item.get("fuente", {}).get("denominacion", ""),
            item.get("fuente", {}).get("numeral", "") or "",
        ]))
        if any(normalizar(t) in texto for t in TERMINOS):
            encontrados.append(item)

    grupos = Counter(item.get("fuente", {}).get("norma") or item.get("fuente", {}).get("denominacion") or "Sin norma" for item in encontrados)
    lineas = [
        "# Diagnóstico de cobertura — seguridad durante la construcción",
        "",
        f"Versión revisada: `{datos['version']}`. Parámetros totales: `{len(datos['parametros'])}`.",
        f"Parámetros relacionados encontrados: `{len(encontrados)}`.",
        "",
        "## Resumen por fuente",
        "",
    ]
    for nombre, cantidad in grupos.most_common():
        lineas.append(f"- {nombre}: {cantidad}")
    lineas.append("")

    for nombre, _ in grupos.most_common():
        lineas.extend([f"## {nombre}", ""])
        for item in encontrados:
            fuente = item.get("fuente", {}).get("norma") or item.get("fuente", {}).get("denominacion") or "Sin norma"
            if fuente != nombre:
                continue
            lineas.append(
                f"- `{item['id']}` | {item.get('categoria','')} | {item.get('elemento','')} | "
                f"{item.get('parametro','')} | {item.get('fuente',{}).get('numeral') or 'sin numeral'}"
            )
        lineas.append("")

    OUT.write_text("\n".join(lineas), encoding="utf-8")
    print(f"Diagnóstico generado: {len(encontrados)} registros relacionados")


if __name__ == "__main__":
    main()
