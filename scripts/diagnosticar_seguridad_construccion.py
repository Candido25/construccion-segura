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

TEMAS = {
    "Planificación, IPERC, ATS y permisos": ["plan de seguridad", "analisis de riesgos", "iperc", "ats", "permiso de trabajo", "procedimiento de trabajo"],
    "EPP y protección respiratoria/auditiva": ["equipo de proteccion personal", "epp", "casco", "respirador", "protector auditivo", "guante", "calzado", "lentes"],
    "Trabajos en altura y protección de bordes": ["trabajo en altura", "caida", "arnes", "linea de vida", "baranda", "borde", "abertura", "hueco"],
    "Andamios y plataformas": ["andamio", "plataforma suspendida", "plataforma de trabajo"],
    "Escaleras portátiles y provisionales": ["escalera portatil", "escalera provisional", "escalera de acceso"],
    "Excavaciones y zanjas": ["excavacion", "zanja", "entibado", "talud", "napa", "espacio confinado"],
    "Herramientas manuales y eléctricas": ["herramienta", "esmeril", "taladro", "sierra", "disco", "guarda"],
    "Izaje, grúas y aparejos": ["izaje", "grua", "eslinga", "gancho", "aparejo", "carga suspendida"],
    "Soldadura, corte y trabajo en caliente": ["soldadura", "oxicorte", "trabajo en caliente", "acetileno", "cilindro de gas"],
    "Electricidad provisional": ["electricidad provisional", "tablero provisional", "extension electrica", "puesta a tierra", "diferencial"],
    "Orden, limpieza y almacenamiento": ["orden y limpieza", "apilamiento", "almacenamiento", "residuo", "ruta libre"],
    "Demoliciones": ["demolicion", "demolición"],
    "Tránsito, maquinaria y terceros": ["maquinaria", "vehiculo", "peaton", "via publica", "visitante", "señalizacion"],
    "Incendios y emergencias": ["extintor", "incendio", "evacuacion", "primeros auxilios", "botiquin", "emergencia"],
    "Polvo, ruido, vibración y clima": ["polvo", "ruido", "vibracion", "radiacion solar", "calor", "viento", "lluvia"],
    "Encofrado, desencofrado y acero": ["encofrado", "desencofrado", "acero de refuerzo", "varilla", "puntal"],
}


def normalizar(texto: str) -> str:
    base = unicodedata.normalize("NFD", str(texto or "").lower())
    return "".join(c for c in base if unicodedata.category(c) != "Mn")


def texto_item(item: dict) -> str:
    return normalizar(" ".join([
        item.get("id", ""), item.get("categoria", ""), item.get("elemento", ""),
        item.get("parametro", ""), item.get("valor", {}).get("texto", ""),
        " ".join(item.get("condiciones", []) or []), item.get("advertencia", ""),
        item.get("fuente", {}).get("norma", ""), item.get("fuente", {}).get("denominacion", ""),
        item.get("fuente", {}).get("numeral", "") or "",
    ]))


def main() -> None:
    datos = json.loads(BASE.read_text(encoding="utf-8"))
    textos = {item["id"]: texto_item(item) for item in datos["parametros"]}
    encontrados = [item for item in datos["parametros"] if any(normalizar(t) in textos[item["id"]] for t in TERMINOS)]

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

    lineas.extend(["", "## Cobertura temática", ""])
    for tema, claves in TEMAS.items():
        coinciden = [item for item in datos["parametros"] if any(normalizar(k) in textos[item["id"]] for k in claves)]
        criterios = [item for item in coinciden if item.get("estado_revision") == "criterio_tecnico_revisado"]
        lineas.append(f"### {tema} — {len(coinciden)} registros, {len(criterios)} criterios revisados")
        lineas.append("")
        for item in coinciden:
            lineas.append(
                f"- `{item['id']}` | {item.get('estado_revision','')} | {item.get('categoria','')} | "
                f"{item.get('elemento','')} | {item.get('parametro','')}"
            )
        lineas.append("")

    lineas.extend(["## Registros por fuente", ""])
    for nombre, _ in grupos.most_common():
        lineas.extend([f"### {nombre}", ""])
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
