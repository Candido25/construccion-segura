from __future__ import annotations

from pathlib import Path
import base64
import gzip
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
NORMATIVA = BACKEND / "normativa_tecnica.json"
PREGUNTAS = BACKEND / "preguntas_tecnicas.json"
CHECK = ROOT / "scripts" / "check_normativa.py"
DOC = ROOT / "docs" / "VALIDACION_OBRAS_PRELIMINARES_SEGURIDAD_2026-07-27.md"

PAYLOAD_DIR = ROOT / "scripts" / "data_obras_preliminares"
PAYLOAD_B64 = "".join(
    ruta.read_text(encoding="utf-8").strip()
    for ruta in sorted(PAYLOAD_DIR.glob("part*.txt"))
)


def cargar_registros() -> dict:
    comprimido = base64.b64decode(PAYLOAD_B64)
    return json.loads(gzip.decompress(comprimido).decode("utf-8"))


def reemplazar_unico(texto: str, anterior: str, nuevo: str) -> str:
    if texto.count(anterior) != 1:
        raise SystemExit(f"No se encontró una única coincidencia para: {anterior}")
    return texto.replace(anterior, nuevo, 1)


def main() -> None:
    payload = cargar_registros()
    base = json.loads(NORMATIVA.read_text(encoding="utf-8"))
    banco = json.loads(PREGUNTAS.read_text(encoding="utf-8"))

    registros = payload["registros"]
    ids_existentes = {item["id"] for item in base["parametros"]}
    repetidos = [item["id"] for item in registros if item["id"] in ids_existentes]
    if repetidos:
        raise SystemExit("Los siguientes parámetros ya existen: " + ", ".join(repetidos))

    ids_nuevos = [item["id"] for item in registros]
    if len(ids_nuevos) != len(set(ids_nuevos)):
        raise SystemExit("El inventario propuesto contiene identificadores duplicados.")

    todas_preguntas = [
        pregunta
        for categoria in banco.get("categorias", [])
        for pregunta in categoria.get("preguntas", [])
        if isinstance(pregunta, dict)
    ]
    max_q = max(
        int(item["id"][1:])
        for item in todas_preguntas
        if re.fullmatch(r"q\d+", item.get("id", ""))
    )

    categorias = {categoria["nombre"]: categoria for categoria in banco["categorias"]}
    nuevos_parametros = []
    nuevas_preguntas = []

    for indice, registro in enumerate(registros, start=1):
        qid = f"q{max_q + indice}"
        parametro = {
            clave: valor
            for clave, valor in registro.items()
            if clave not in {"faq_categoria", "pregunta", "respuesta"}
        }
        parametro["faq_relacionadas"] = [qid]
        nuevos_parametros.append(parametro)

        nombre_categoria = registro["faq_categoria"]
        categoria = categorias.get(nombre_categoria)
        if categoria is None:
            categoria = {"nombre": nombre_categoria, "preguntas": []}
            banco["categorias"].append(categoria)
            categorias[nombre_categoria] = categoria

        pregunta = {
            "id": qid,
            "pregunta": registro["pregunta"],
            "respuesta": registro["respuesta"],
        }
        categoria["preguntas"].append(pregunta)
        nuevas_preguntas.append(pregunta)

    base["parametros"].extend(nuevos_parametros)
    base["version"] = payload["version_objetivo"]
    base["fecha_revision"] = payload["fecha_revision"]

    ids_finales = [item["id"] for item in base["parametros"]]
    if len(ids_finales) != len(set(ids_finales)):
        raise SystemExit("La ampliación produjo identificadores normativos duplicados.")

    faq_finales = [
        pregunta["id"]
        for categoria in banco["categorias"]
        for pregunta in categoria.get("preguntas", [])
    ]
    if len(faq_finales) != len(set(faq_finales)):
        raise SystemExit("La ampliación produjo identificadores de preguntas duplicados.")

    referencias = {
        faq
        for parametro in base["parametros"]
        for faq in parametro.get("faq_relacionadas", [])
    }
    faltantes = referencias - set(faq_finales)
    if faltantes:
        raise SystemExit("Hay referencias FAQ inexistentes: " + ", ".join(sorted(faltantes)))

    total_parametros = len(base["parametros"])
    total_preguntas = len(faq_finales)
    total_validados = sum(
        item.get("estado_revision") == "validado_con_numeral"
        for item in base["parametros"]
    )

    if total_parametros != 1126:
        raise SystemExit(f"Se esperaban 1126 parámetros y se obtuvieron {total_parametros}.")
    if total_preguntas != 2589:
        raise SystemExit(f"Se esperaban 2589 preguntas y se obtuvieron {total_preguntas}.")
    if total_validados != 1092:
        raise SystemExit(
            f"Se esperaban 1092 registros validados con numeral y se obtuvieron {total_validados}."
        )

    NORMATIVA.write_text(
        json.dumps(base, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    PREGUNTAS.write_text(
        json.dumps(banco, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    check = CHECK.read_text(encoding="utf-8")
    check = reemplazar_unico(
        check, "if len(base.parametros) < 982:", "if len(base.parametros) < 1126:"
    )
    check = reemplazar_unico(
        check,
        "por lo menos 982 parámetros revisados",
        "por lo menos 1126 parámetros revisados",
    )
    check = reemplazar_unico(check, "if validados < 948:", "if validados < 1092:")
    check = reemplazar_unico(
        check,
        "al menos 948 numerales RNE validados",
        "al menos 1092 numerales RNE validados",
    )
    check = reemplazar_unico(
        check, 'if base.version != "2.1.0":', 'if base.version != "2.2.0":'
    )
    check = reemplazar_unico(
        check,
        "La versión normativa esperada es 2.1.0",
        "La versión normativa esperada es 2.2.0",
    )
    check = reemplazar_unico(check, "if len(todas) < 2445:", "if len(todas) < 2589:")
    check = reemplazar_unico(
        check,
        "La base ampliada de azoteas, drenaje pluvial y estacionamientos requiere por lo menos 2445 preguntas técnicas.",
        "La base ampliada de obras preliminares y seguridad requiere por lo menos 2589 preguntas técnicas.",
    )
    CHECK.write_text(check, encoding="utf-8")

    DOC.write_text(
        f"""# Validación normativa de obras preliminares y seguridad — 27 de julio de 2026

## Alcance

Se incorporaron **{len(nuevos_parametros)} parámetros** y **{len(nuevas_preguntas)} preguntas** después de comparar el inventario completo de G.050 con los 982 parámetros de la versión 2.1.0.

## Contenido incorporado

- organización y delimitación de las áreas de trabajo;
- instalaciones eléctricas provisionales y control de extensiones;
- accesos, circulación, visitantes, terceros, evacuación y señalización;
- iluminación, ventilación, polvo y condiciones ambientales;
- agua potable, vestuarios, comedores, servicios higiénicos y bienestar;
- prevención de incendios y respuesta inicial ante emergencias;
- contenido operativo del Plan de Seguridad y Salud en el Trabajo;
- protecciones colectivas, orden, limpieza y residuos;
- almacenamiento, apilamiento, sustancias peligrosas y zonas de carga;
- zanjas, entibados, accesos, barreras, redes enterradas, napa y protección de colindantes.

## Fuentes oficiales

- G.050 Seguridad durante la Construcción — DS N.° 010-2009-VIVIENDA.
- Índice oficial del Reglamento Nacional de Edificaciones del Ministerio de Vivienda, Construcción y Saneamiento.

## Resultado

- Versión normativa: `2.2.0`.
- Parámetros totales: `{total_parametros}`.
- Registros `validado_con_numeral`: `{total_validados}`.
- Preguntas técnicas: `{total_preguntas}`.

## Criterios editoriales

- Se conservaron los 62 parámetros G.050 existentes y se excluyeron conceptos ya cubiertos sobre electricidad provisional, circulación mínima, comités, plan general, orden, residuos, caídas, andamios y demoliciones.
- El bloque de E.050 sobre sostenimientos y calzaduras no fue repetido.
- Las distancias y cantidades se condicionaron a su supuesto normativo: profundidad de excavación, presencia de vibraciones, número de trabajadores o tipo de material almacenado.
- La información es preventiva y educativa; no autoriza excavaciones profundas, entibados, apuntalamientos ni trabajos junto a colindantes sin diseño y supervisión competente.
""",
        encoding="utf-8",
    )

    print(
        f"Ampliación aplicada: {len(nuevos_parametros)} parámetros, "
        f"{len(nuevas_preguntas)} preguntas, versión {base['version']}."
    )


if __name__ == "__main__":
    main()
