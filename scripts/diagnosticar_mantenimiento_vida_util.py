from __future__ import annotations

from collections import Counter
from pathlib import Path
import json
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
NORMATIVA = ROOT / "backend" / "normativa_tecnica.json"
PREGUNTAS = ROOT / "backend" / "preguntas_tecnicas.json"
SALIDA = ROOT / "docs" / "DIAGNOSTICO_MANTENIMIENTO_VIDA_UTIL_2026-07-27.md"

TERMINOS = (
    "mantenimiento", "conservacion", "vida util", "inspeccion", "revision periodica",
    "reparacion", "fisura", "grieta", "humedad", "filtracion", "corrosion", "salitre",
    "techo", "azotea", "canaleta", "sumidero", "fachada", "pintura", "sellante",
    "cisterna", "tanque", "limpieza", "desinfeccion", "tablero", "puesta a tierra",
    "fuga", "valvula", "gas", "garantia", "manual", "intervencion", "demolicion",
    "ampliacion", "sobrecarga", "muro", "columna", "viga", "losa", "puerta", "ventana"
)


def normalizar(texto: str) -> str:
    base = unicodedata.normalize("NFD", str(texto or "").lower())
    return "".join(c for c in base if unicodedata.category(c) != "Mn")


def main() -> None:
    normativa = json.loads(NORMATIVA.read_text(encoding="utf-8"))
    preguntas = json.loads(PREGUNTAS.read_text(encoding="utf-8"))
    parametros = normativa.get("parametros", [])
    faq = [p for c in preguntas.get("categorias", []) for p in c.get("preguntas", []) if isinstance(p, dict)]

    relacionados = []
    for item in parametros:
        texto = normalizar(" ".join([
            item.get("id", ""), item.get("categoria", ""), item.get("elemento", ""),
            item.get("parametro", ""), item.get("valor", {}).get("texto", ""),
            " ".join(item.get("condiciones", [])), item.get("advertencia", "")
        ]))
        if any(t in texto for t in TERMINOS):
            relacionados.append(item)

    normas = Counter(i.get("fuente", {}).get("norma", "Sin norma") for i in relacionados)
    estados = Counter(i.get("estado_revision", "") for i in relacionados)
    categorias = Counter(i.get("categoria", "") for i in relacionados)
    ge040 = [i for i in parametros if "GE.040" in i.get("fuente", {}).get("norma", "")]

    muestras = sorted(relacionados, key=lambda i: (i.get("categoria", ""), i.get("elemento", ""), i.get("parametro", "")))[:100]
    lineas = [
        "# Diagnóstico de cobertura — mantenimiento preventivo y vida útil",
        "",
        f"- Versión revisada: `{normativa.get('version')}`.",
        f"- Parámetros totales: `{len(parametros)}`.",
        f"- Preguntas totales: `{len(faq)}`.",
        f"- Parámetros relacionados encontrados: `{len(relacionados)}`.",
        f"- Parámetros GE.040 encontrados: `{len(ge040)}`.",
        "",
        "## Estados de revisión",
        "",
    ]
    lineas.extend(f"- {k}: {v}" for k, v in estados.most_common())
    lineas.extend(["", "## Principales fuentes ya presentes", ""])
    lineas.extend(f"- {k}: {v}" for k, v in normas.most_common(25))
    lineas.extend(["", "## Principales categorías relacionadas", ""])
    lineas.extend(f"- {k}: {v}" for k, v in categorias.most_common(25))
    lineas.extend(["", "## Cobertura GE.040", ""])
    for item in ge040:
        lineas.append(f"- `{item.get('id')}` — {item.get('parametro')} — {item.get('valor', {}).get('texto', '')}")
    lineas.extend(["", "## Muestra de registros relacionados", ""])
    for item in muestras:
        lineas.append(f"- `{item.get('id')}` — {item.get('categoria')} / {item.get('elemento')} — {item.get('parametro')}")

    SALIDA.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"Diagnóstico generado: {len(relacionados)} relacionados; {len(ge040)} GE.040")


if __name__ == "__main__":
    main()
