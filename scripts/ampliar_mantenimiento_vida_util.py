from __future__ import annotations

from pathlib import Path
import base64
import bz2
import json
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
NORMATIVA = BACKEND / "normativa_tecnica.json"
PREGUNTAS = BACKEND / "preguntas_tecnicas.json"
CHECK = ROOT / "scripts" / "check_normativa.py"
DOC = ROOT / "docs" / "VALIDACION_MANTENIMIENTO_VIDA_UTIL_2026-07-27.md"

EXTRA = '''
    mantenimiento_plan = api.detalle_parametro_normativo("criterio-mantenimiento-plan-anual")
    if mantenimiento_plan["estado_revision"] != "criterio_tecnico_revisado":
        raise SystemExit("El plan de mantenimiento debe conservarse como criterio técnico revisado.")

    mantenimiento_fisura = api.detalle_parametro_normativo("criterio-mantenimiento-fisura-columna-viga")
    if mantenimiento_fisura["elemento"] != "Estructura y fisuras":
        raise SystemExit("La fisura en columna o viga debe conservar su categoría técnica.")

    mantenimiento_agua = api.detalle_parametro_normativo("criterio-mantenimiento-llave-general")
    if mantenimiento_agua["fuente"]["tipo"] != "criterio_tecnico":
        raise SystemExit("La llave general debe conservar fuente de criterio técnico.")

    mantenimiento_electrico = api.detalle_parametro_normativo("criterio-mantenimiento-calentamiento-tomacorriente")
    if mantenimiento_electrico["estado_revision"] != "criterio_tecnico_revisado":
        raise SystemExit("El tomacorriente caliente debe conservarse como criterio técnico revisado.")

    mantenimiento_gas = api.detalle_parametro_normativo("criterio-mantenimiento-olor-gas")
    if mantenimiento_gas["elemento"] != "Gas y combustión":
        raise SystemExit("La respuesta ante olor a gas debe conservar su clasificación.")

    mantenimiento_intervencion = api.detalle_parametro_normativo("criterio-mantenimiento-no-cortar-acero")
    if mantenimiento_intervencion["estado_revision"] != "criterio_tecnico_revisado":
        raise SystemExit("La prohibición práctica de cortar acero debe conservarse como criterio revisado.")

'''


def normalizar(texto: str) -> str:
    base = unicodedata.normalize("NFD", str(texto or "").lower())
    sin_tildes = "".join(c for c in base if unicodedata.category(c) != "Mn")
    return " ".join(re.sub(r"[^a-z0-9]+", " ", sin_tildes).split())


def similitud(a: str, b: str) -> float:
    ta, tb = set(normalizar(a).split()), set(normalizar(b).split())
    return len(ta & tb) / len(ta | tb) if ta and tb else 0.0


def reemplazar_unico(texto: str, anterior: str, nuevo: str) -> str:
    if texto.count(anterior) != 1:
        raise SystemExit("No se encontró una sola vez: " + anterior)
    return texto.replace(anterior, nuevo, 1)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Uso: ampliar_mantenimiento_vida_util.py <payload.b64>")

    payload = Path(sys.argv[1]).read_text(encoding="utf-8").strip()
    inventario = json.loads(bz2.decompress(base64.b64decode(payload)).decode("utf-8"))
    base = json.loads(NORMATIVA.read_text(encoding="utf-8"))
    preguntas = json.loads(PREGUNTAS.read_text(encoding="utf-8"))
    if base.get("version") != "3.0.0":
        raise SystemExit("La ampliación debe iniciar desde la versión 3.0.0")

    ids = {p.get("id") for p in base["parametros"]}
    todas = [
        item for categoria in preguntas["categorias"]
        for item in categoria.get("preguntas", []) if isinstance(item, dict)
    ]
    textos = [item.get("pregunta", "") for item in todas]
    normalizados = {normalizar(texto) for texto in textos}
    max_q = max(
        [int(m.group(1)) for item in todas
         if (m := re.fullmatch(r"q(\d+)", str(item.get("id", ""))))],
        default=0,
    )

    categoria_nombre = "Mantenimiento preventivo y vida útil de la vivienda"
    categoria = next((c for c in preguntas["categorias"] if c.get("nombre") == categoria_nombre), None)
    if categoria is None:
        categoria = {"nombre": categoria_nombre, "preguntas": []}
        preguntas["categorias"].append(categoria)

    nuevos: list[dict] = []
    omitidos: list[tuple[str, float]] = []

    def aceptar(pregunta: str) -> bool:
        pregunta_normalizada = normalizar(pregunta)
        if pregunta_normalizada in normalizados:
            return False
        mejor = max((similitud(pregunta, existente) for existente in textos), default=0.0)
        if mejor >= 0.87:
            omitidos.append((pregunta, mejor))
            return False
        return True

    def agregar(parametro: dict, pregunta: str, respuesta: str) -> None:
        nonlocal max_q
        max_q += 1
        qid = f"q{max_q}"
        parametro["faq_relacionadas"] = [qid]
        base["parametros"].append(parametro)
        categoria["preguntas"].append({"id": qid, "pregunta": pregunta, "respuesta": respuesta})
        ids.add(parametro["id"])
        textos.append(pregunta)
        normalizados.add(normalizar(pregunta))
        nuevos.append(parametro)

    for rid, elemento, nombre_parametro, pregunta, respuesta in inventario["practicas"]:
        if rid in ids or not aceptar(pregunta):
            continue
        agregar({
            "id": rid,
            "categoria": categoria_nombre,
            "elemento": elemento,
            "parametro": nombre_parametro,
            "clasificacion": "recomendacion",
            "valor": {"tipo": "sin_valor_universal", "texto": respuesta},
            "condiciones": [
                "Ajustar la inspección o intervención al elemento, exposición, antigüedad, uso, fabricante y nivel de riesgo.",
                "Documentar síntomas, causa probable, responsable, fecha, resultado y evidencia cuando corresponda.",
            ],
            "fuente": {
                "tipo": "criterio_tecnico",
                "norma": "Buenas prácticas de mantenimiento preventivo y vida útil",
                "denominacion": "Revisión técnica basada en GE.040, manuales de uso, conservación e inspección de viviendas",
                "dispositivo": None,
                "numeral": None,
                "numeral_confirmado": False,
            },
            "estado_revision": "criterio_tecnico_revisado",
            "advertencia": "El criterio no sustituye GE.040, manuales, garantías, evaluación estructural, técnicos competentes ni licencias para modificar la vivienda.",
            "fecha_revision": "2026-07-27",
        }, pregunta, respuesta)

    cantidad = len(nuevos)
    if cantidad < 130:
        raise SystemExit(f"La depuración dejó solo {cantidad} registros nuevos")

    base["version"] = "3.1.0"
    base["fecha_revision"] = "2026-07-27"
    total_parametros = len(base["parametros"])
    total_preguntas = sum(len(c.get("preguntas", [])) for c in preguntas["categorias"])
    validados = sum(p.get("estado_revision") == "validado_con_numeral" for p in base["parametros"])
    criterios = sum(p.get("estado_revision") == "criterio_tecnico_revisado" for p in base["parametros"])

    NORMATIVA.write_text(json.dumps(base, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    PREGUNTAS.write_text(json.dumps(preguntas, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    check = CHECK.read_text(encoding="utf-8")
    reemplazos = [
        ("if len(base.parametros) < 2149:", f"if len(base.parametros) < {total_parametros}:"),
        ("por lo menos 2149 parámetros revisados", f"por lo menos {total_parametros} parámetros revisados"),
        ('if base.version != "3.0.0":', 'if base.version != "3.1.0":'),
        ("La versión normativa esperada es 3.0.0", "La versión normativa esperada es 3.1.0"),
        ("if validados < 1254:", f"if validados < {validados}:"),
        ("al menos 1254 numerales RNE validados", f"al menos {validados} numerales RNE validados"),
        ("if criterios < 877:", f"if criterios < {criterios}:"),
        ("al menos 877 criterios técnicos revisados", f"al menos {criterios} criterios técnicos revisados"),
        ("if len(todas) < 3612:", f"if len(todas) < {total_preguntas}:"),
        ("por lo menos 3612 preguntas técnicas", f"por lo menos {total_preguntas} preguntas técnicas"),
    ]
    for anterior, nuevo in reemplazos:
        check = reemplazar_unico(check, anterior, nuevo)
    check = reemplazar_unico(check, "    preguntas = json.loads(\n", EXTRA + "    preguntas = json.loads(\n")
    CHECK.write_text(check, encoding="utf-8")

    DOC.write_text(f'''# Validación de mantenimiento preventivo y vida útil — 27 de julio de 2026

## Alcance

Se incorporaron **{cantidad} parámetros** y **{cantidad} preguntas** después de depurar **1313 registros relacionados** de la versión 3.0.0, incluidos **20 parámetros GE.040** ya existentes.

## Contenido

- plan, inventario, responsables, bitácora, fotografías y prioridades de mantenimiento;
- inspecciones periódicas, antes y después de lluvias, cambios de uso y viviendas desocupadas;
- fisuras, deformaciones, corrosión, desprendimientos, sobrecargas y señales estructurales;
- muros, acabados, sellantes, pintura, eflorescencia, moho y compatibilidad de reparaciones;
- cubiertas, sumideros, canaletas, bajantes, penetraciones, jardineras y drenaje exterior;
- fachadas, vidrios, puertas, ventanas, barandas, herrajes y portones automáticos;
- agua, desagüe, bombas, válvulas, depósitos, calentadores y conexiones flexibles;
- tableros, diferenciales, puesta a tierra, extensiones, fotovoltaicos, baterías y generadores;
- GLP, artefactos, ventilación, detectores, reguladores y respuesta ante olor a gas;
- evacuación, extintores, alarmas, accesibilidad, plagas, madera, metales y químicos;
- ampliaciones, perforaciones, nuevos equipos, cambio de vanos y documentación de modificaciones;
- revisiones después de sismo, incendio, inundación, impacto, excavación vecina, lluvia y viento;
- garantías, vida útil, repuestos, transferencia de información y revisión posreparación.

## Resultado

- Versión normativa: `3.1.0`.
- Parámetros totales: `{total_parametros}`.
- Registros `validado_con_numeral`: `{validados}`.
- Criterios técnicos revisados: `{criterios}`.
- Preguntas técnicas: `{total_preguntas}`.
- Registros omitidos por similitud fuerte: `{len(omitidos)}`.

## Criterios editoriales

- Se conservaron sin duplicar los 20 requisitos GE.040 ya registrados y las pruebas específicas de estructuras, impermeabilización, instalaciones y cierre de obra.
- No se fijaron frecuencias, vidas útiles, anchos de fisura, periodos de reemplazo ni plazos universales cuando dependen del material, exposición, fabricante, uso, historial o evaluación profesional.
- Las prácticas nuevas se identifican como `criterio_tecnico_revisado`.
- Pintar, sellar o resanar no se presenta como solución suficiente cuando no se ha corregido la causa.
- Las modificaciones que afecten estructura, instalaciones, ventilación, evacuación o cargas requieren revisión profesional y las autorizaciones correspondientes.

## Fuentes oficiales complementarias

- MVCS: Reglamento Nacional de Edificaciones, Norma GE.040 Uso y Mantenimiento.
- SENCICO: Construcción y mantenimiento de viviendas de albañilería.
''', encoding="utf-8")

    print(
        f"Aplicados {cantidad} parámetros y preguntas; versión 3.1.0; "
        f"totales {total_parametros} parámetros y {total_preguntas} preguntas; "
        f"omitidos similares {len(omitidos)}."
    )


if __name__ == "__main__":
    main()
