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
DOC = ROOT / "docs" / "VALIDACION_CONTROL_CALIDAD_CIERRE_2026-07-27.md"
RNE_URL = "https://www.gob.pe/institucion/vivienda/informes-publicaciones/2309793-reglamento-nacional-de-edificaciones-rne"

EXTRA = '''
    calidad_recepcion = api.detalle_parametro_normativo("ge030-recepcion-demuestra-cumplimiento")
    if calidad_recepcion["estado_revision"] != "validado_con_numeral":
        raise SystemExit("La recepción de obra debe conservar numeral GE.030 confirmado.")

    calidad_expediente = api.detalle_parametro_normativo("ge030-expediente-final-por-etapa")
    if calidad_expediente["fuente"]["numeral"] != "Artículo 17":
        raise SystemExit("El expediente final debe conservar la referencia al artículo 17.")

    calidad_oculto = api.detalle_parametro_normativo("criterio-calidad-liberacion-trabajo-oculto")
    if calidad_oculto["estado_revision"] != "criterio_tecnico_revisado":
        raise SystemExit("La liberación de trabajos ocultos debe conservarse como criterio técnico.")

    calidad_asbuilt = api.detalle_parametro_normativo("criterio-calidad-planos-conforme-obra")
    if calidad_asbuilt["elemento"] != "Planos conforme a obra":
        raise SystemExit("Los planos conforme a obra deben conservar su clasificación de cierre.")

    calidad_integrada = api.detalle_parametro_normativo("criterio-calidad-prueba-integrada-instalaciones")
    if calidad_integrada["fuente"]["tipo"] != "criterio_tecnico":
        raise SystemExit("La prueba integrada debe conservar fuente de criterio técnico.")

    calidad_pendientes = api.detalle_parametro_normativo("criterio-calidad-pendientes-en-acta")
    if calidad_pendientes["estado_revision"] != "criterio_tecnico_revisado":
        raise SystemExit("Los pendientes de entrega deben quedar como criterio revisado.")

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
        raise SystemExit("Uso: ampliar_control_calidad_cierre.py <payload.b64>")
    payload = Path(sys.argv[1]).read_text(encoding="utf-8").strip()
    inventario = json.loads(bz2.decompress(base64.b64decode(payload)).decode("utf-8"))
    base = json.loads(NORMATIVA.read_text(encoding="utf-8"))
    preguntas = json.loads(PREGUNTAS.read_text(encoding="utf-8"))
    if base.get("version") != "2.9.0":
        raise SystemExit("La ampliación debe iniciar desde la versión 2.9.0")

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

    terminos = [
        "calidad", "recepcion", "entrega", "cierre", "expediente final", "dossier",
        "prueba", "ensayo", "inspeccion", "conformidad", "observacion", "garantia",
        "manual", "mantenimiento", "conforme a obra", "puesta en servicio", "no conform",
        "trazabilidad", "certificado", "calibracion", "acta", "liberacion",
    ]
    relacionados = []
    for parametro in base["parametros"]:
        texto = normalizar(" ".join([
            parametro.get("id", ""), parametro.get("categoria", ""),
            parametro.get("elemento", ""), parametro.get("parametro", ""),
            parametro.get("valor", {}).get("texto", ""),
            parametro.get("fuente", {}).get("norma", ""),
        ]))
        if any(normalizar(termino) in texto for termino in terminos):
            relacionados.append(parametro)

    categoria_nombre = "Control de calidad, recepción y cierre de obra"
    categoria = next(
        (c for c in preguntas["categorias"] if c.get("nombre") == categoria_nombre),
        None,
    )
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

    for item in inventario["normativos"]:
        if item["id"] in ids or not aceptar(item["question"]):
            continue
        agregar({
            "id": item["id"],
            "categoria": item["categoria"],
            "elemento": item["elemento"],
            "parametro": item["parametro"],
            "clasificacion": "condicion_normativa",
            "valor": {"tipo": "texto", "texto": item["texto"]},
            "condiciones": [
                "Aplicar según el alcance del proyecto, contrato y etapa constructiva.",
                "Conservar evidencia verificable y trazable de su cumplimiento.",
            ],
            "fuente": {
                "tipo": "RNE",
                "norma": item["norma"],
                "denominacion": item["denominacion"],
                "dispositivo": "Reglamento Nacional de Edificaciones",
                "numeral": item["numeral"],
                "numeral_confirmado": True,
                "url_oficial": RNE_URL,
            },
            "estado_revision": "validado_con_numeral",
            "advertencia": "La recepción documental no reemplaza la verificación física, las pruebas ni la responsabilidad profesional.",
            "fecha_revision": "2026-07-27",
        }, item["question"], item["answer"])

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
                "Ajustar al proyecto, contrato, fabricante, especialidad y riesgo de la partida.",
                "Registrar responsable, ubicación, fecha, resultado y evidencia de cierre cuando corresponda.",
            ],
            "fuente": {
                "tipo": "criterio_tecnico",
                "norma": "Buenas prácticas de control de calidad y cierre de obra",
                "denominacion": "Revisión técnica basada en GE.030, supervisión, puesta en servicio y documentación de obra",
                "dispositivo": None,
                "numeral": None,
                "numeral_confirmado": False,
            },
            "estado_revision": "criterio_tecnico_revisado",
            "advertencia": "El criterio no sustituye especificaciones, ensayos normativos, manuales, contrato ni aprobación profesional.",
            "fecha_revision": "2026-07-27",
        }, pregunta, respuesta)

    cantidad = len(nuevos)
    if cantidad < 120:
        raise SystemExit(f"La depuración dejó solo {cantidad} registros nuevos")

    base["version"] = "3.0.0"
    base["fecha_revision"] = "2026-07-27"
    total_parametros = len(base["parametros"])
    total_preguntas = sum(len(c.get("preguntas", [])) for c in preguntas["categorias"])
    validados = sum(p.get("estado_revision") == "validado_con_numeral" for p in base["parametros"])
    criterios = sum(p.get("estado_revision") == "criterio_tecnico_revisado" for p in base["parametros"])

    NORMATIVA.write_text(json.dumps(base, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    PREGUNTAS.write_text(json.dumps(preguntas, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    check = CHECK.read_text(encoding="utf-8")
    reemplazos = [
        ("if len(base.parametros) < 1976:", f"if len(base.parametros) < {total_parametros}:"),
        ("por lo menos 1976 parámetros revisados", f"por lo menos {total_parametros} parámetros revisados"),
        ('if base.version != "2.9.0":', 'if base.version != "3.0.0":'),
        ("La versión normativa esperada es 2.9.0", "La versión normativa esperada es 3.0.0"),
        ("if validados < 1245:", f"if validados < {validados}:"),
        ("al menos 1245 numerales RNE validados", f"al menos {validados} numerales RNE validados"),
        ("if criterios < 713:", f"if criterios < {criterios}:"),
        ("al menos 713 criterios técnicos revisados", f"al menos {criterios} criterios técnicos revisados"),
        ("if len(todas) < 3439:", f"if len(todas) < {total_preguntas}:"),
        ("por lo menos 3439 preguntas técnicas", f"por lo menos {total_preguntas} preguntas técnicas"),
    ]
    for anterior, nuevo in reemplazos:
        check = reemplazar_unico(check, anterior, nuevo)
    check = reemplazar_unico(check, "    preguntas = json.loads(\n", EXTRA + "    preguntas = json.loads(\n")
    CHECK.write_text(check, encoding="utf-8")

    fuentes: dict[str, int] = {}
    for parametro in relacionados:
        fuente = parametro.get("fuente", {})
        nombre = fuente.get("norma") or fuente.get("denominacion") or "Sin fuente"
        fuentes[nombre] = fuentes.get(nombre, 0) + 1
    resumen = "\n".join(
        f"- {nombre}: {cantidad_fuente}"
        for nombre, cantidad_fuente in sorted(fuentes.items(), key=lambda par: (-par[1], par[0]))[:12]
    )

    DOC.write_text(f'''# Validación de control de calidad, recepción y cierre de obra — 27 de julio de 2026

## Alcance

Se incorporaron **{cantidad} parámetros** y **{cantidad} preguntas** después de depurar **{len(relacionados)} registros relacionados** de la versión 2.9.0.

## Contenido

- plan de calidad, criterios de aceptación, puntos de espera y liberación de trabajos ocultos;
- planos vigentes, consultas, cambios, muestras, proveedores y trazabilidad por lotes;
- recepción de materiales, certificados, almacenamiento, calibración y cadena de custodia;
- controles de estructuras, albañilería, impermeabilización, fachadas y acabados;
- pruebas sanitarias, eléctricas, de gas, telecomunicaciones y puesta en servicio;
- pruebas integradas, observaciones, repruebas y recepciones parciales;
- planos conforme a obra, manuales, garantías, capacitación, llaves, repuestos e inventarios;
- expediente final, respaldo digital, actas, restricciones de uso y revisión posentrega.

## Resultado

- Versión normativa: `3.0.0`.
- Parámetros totales: `{total_parametros}`.
- Registros `validado_con_numeral`: `{validados}`.
- Criterios técnicos revisados: `{criterios}`.
- Preguntas técnicas: `{total_preguntas}`.
- Registros omitidos por similitud fuerte: `{len(omitidos)}`.

## Criterios editoriales

- Se conservaron sin duplicar pruebas y controles ya registrados en normas estructurales, sanitarias, eléctricas, de gas, transporte mecánico y bloques prácticos anteriores.
- Se incorporaron condiciones de GE.030 y G.030 sobre gestión de calidad, recepción, expediente final, información documentada y garantías.
- No se fijaron tolerancias, frecuencias, presiones, tiempos, capacidades o plazos universales cuando dependen de la norma específica, contrato, fabricante o proyecto.
- Las prácticas operativas nuevas se identifican como `criterio_tecnico_revisado`.
- La entrega de llaves o la firma de un acta no reemplaza pruebas, cierre de observaciones ni documentación conforme a obra.

## Principales fuentes ya presentes en la cobertura relacionada

{resumen}
''', encoding="utf-8")

    print(
        f"Aplicados {cantidad} parámetros y preguntas; versión 3.0.0; "
        f"totales {total_parametros} parámetros y {total_preguntas} preguntas; "
        f"omitidos similares {len(omitidos)}."
    )


if __name__ == "__main__":
    main()
