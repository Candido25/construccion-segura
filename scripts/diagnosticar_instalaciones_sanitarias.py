from __future__ import annotations

from pathlib import Path
import json
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
SALIDA = ROOT / "docs" / "DIAGNOSTICO_INSTALACIONES_SANITARIAS_2026-07-27.md"

TERMINOS = [
    "is.010", "agua fria", "agua caliente", "desague", "desagüe", "ventilacion",
    "ventilación", "registro", "caja de registro", "cisterna", "tanque elevado",
    "bomba", "electrobomba", "hidroneumatico", "hidroneumático", "sumidero",
    "trampa", "sifon", "sifón", "montante", "colector", "ramal", "pendiente",
    "prueba hidraulica", "prueba hidráulica", "prueba de estanqueidad", "tuberia",
    "tubería", "aparato sanitario", "valvula", "válvula", "rebose", "limpieza",
    "pase", "empotramiento", "manguito", "agua residual", "aguas residuales",
]


def normalizar(texto: str) -> str:
    base = unicodedata.normalize("NFD", str(texto or "").lower())
    return "".join(c for c in base if unicodedata.category(c) != "Mn")


def main() -> None:
    normativa = json.loads((BACKEND / "normativa_tecnica.json").read_text(encoding="utf-8"))
    preguntas = json.loads((BACKEND / "preguntas_tecnicas.json").read_text(encoding="utf-8"))
    parametros = normativa.get("parametros", [])
    total_preguntas = sum(len(c.get("preguntas", [])) for c in preguntas.get("categorias", []))

    relacionados = []
    is010 = []
    for item in parametros:
        texto = normalizar(" ".join([
            item.get("id", ""), item.get("categoria", ""), item.get("elemento", ""),
            item.get("parametro", ""), item.get("valor", {}).get("texto", ""),
            item.get("fuente", {}).get("norma", ""), item.get("fuente", {}).get("numeral", ""),
            " ".join(item.get("condiciones", [])),
        ]))
        if "is.010" in normalizar(item.get("fuente", {}).get("norma", "")) or item.get("id", "").startswith("is010-"):
            is010.append(item)
        if any(normalizar(t) in texto for t in TERMINOS):
            relacionados.append(item)

    lineas = [
        "# Diagnóstico de cobertura existente — instalaciones sanitarias",
        "",
        f"Versión revisada: `{normativa.get('version')}`.",
        f"Parámetros totales: `{len(parametros)}`.",
        f"Preguntas totales: `{total_preguntas}`.",
        f"Parámetros IS.010 existentes: `{len(is010)}`.",
        f"Parámetros sanitarios relacionados: `{len(relacionados)}`.",
        "",
        "## Parámetros IS.010 existentes",
        "",
    ]
    for item in sorted(is010, key=lambda x: x.get("id", "")):
        fuente = item.get("fuente", {})
        lineas.append(
            f"- `{item.get('id')}` | {item.get('categoria')} | {item.get('elemento')} | "
            f"{item.get('parametro')} | {fuente.get('numeral')}"
        )

    lineas.extend(["", "## Cobertura por término", ""])
    for termino in TERMINOS:
        t = normalizar(termino)
        coincidencias = []
        for item in relacionados:
            texto = normalizar(" ".join([
                item.get("id", ""), item.get("categoria", ""), item.get("elemento", ""),
                item.get("parametro", ""), item.get("valor", {}).get("texto", ""),
            ]))
            if t in texto:
                coincidencias.append(item.get("id"))
        lineas.append(f"- **{termino}**: {len(coincidencias)}" + (f" — {', '.join(sorted(coincidencias)[:30])}" if coincidencias else ""))

    SALIDA.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"Diagnóstico generado: {len(is010)} IS.010 y {len(relacionados)} relacionados.")


if __name__ == "__main__":
    main()
