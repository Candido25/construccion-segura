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
DOC = ROOT / "docs" / "VALIDACION_AZOTEAS_DRENAJE_ESTACIONAMIENTOS_2026-07-27.md"

PAYLOAD_DIR = ROOT / "scripts" / "data_azoteas"
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

    registros_payload = payload["registros"]
    ids_existentes = {item["id"] for item in base["parametros"]}
    repetidos = [
        item["id"] for item in registros_payload if item["id"] in ids_existentes
    ]
    duplicados_esperados = ["a020-piso-exterior-antideslizante"]
    if repetidos != duplicados_esperados:
        raise SystemExit(
            "La depuración de duplicados no coincide con lo previsto: "
            + ", ".join(repetidos)
        )
    registros = [
        item for item in registros_payload if item["id"] not in ids_existentes
    ]

    todas_preguntas = [
        pregunta
        for categoria in banco.get("categorias", [])
        for pregunta in categoria.get("preguntas", [])
        if isinstance(pregunta, dict)
    ]
    max_q = max(int(item["id"][1:]) for item in todas_preguntas if re.fullmatch(r"q\d+", item.get("id", "")))

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

    if total_parametros != 982:
        raise SystemExit(f"Se esperaban 982 parámetros y se obtuvieron {total_parametros}.")
    if total_preguntas != 2445:
        raise SystemExit(f"Se esperaban 2445 preguntas y se obtuvieron {total_preguntas}.")
    if total_validados != 948:
        raise SystemExit(f"Se esperaban 948 registros validados con numeral y se obtuvieron {total_validados}.")

    NORMATIVA.write_text(
        json.dumps(base, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    PREGUNTAS.write_text(
        json.dumps(banco, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    check = CHECK.read_text(encoding="utf-8")
    check = reemplazar_unico(check, "if len(base.parametros) < 886:", "if len(base.parametros) < 982:")
    check = reemplazar_unico(check, "por lo menos 886 parámetros revisados", "por lo menos 982 parámetros revisados")
    check = reemplazar_unico(check, "if validados < 852:", "if validados < 948:")
    check = reemplazar_unico(check, "al menos 852 numerales RNE validados", "al menos 948 numerales RNE validados")
    check = reemplazar_unico(check, 'if base.version != "2.0.0":', 'if base.version != "2.1.0":')
    check = reemplazar_unico(check, "if len(todas) < 2349:", "if len(todas) < 2445:")
    check = reemplazar_unico(
        check,
        "El bloque de gas, energía solar y transporte mecánico requiere por lo menos 2349 preguntas técnicas.",
        "La base ampliada de azoteas, drenaje pluvial y estacionamientos requiere por lo menos 2445 preguntas técnicas.",
    )
    CHECK.write_text(check, encoding="utf-8")

    DOC.write_text(
        f"""# Validación normativa de azoteas, cubiertas, drenaje pluvial y estacionamientos — 27 de julio de 2026

## Alcance

Se incorporaron **{len(nuevos_parametros)} parámetros** y **{len(nuevas_preguntas)} preguntas** sin fijar una cuota artificial. El inventario se obtuvo del contraste de las reglas aplicables a vivienda y autoconstrucción contenidas en A.010, A.020 y CE.040.

## Contenido incorporado

- azoteas: usos, accesos, porcentaje techable, retranques, parapetos y barandas;
- cubiertas ligeras: fijación, hermeticidad, pendiente, comportamiento térmico y mantenimiento;
- impermeabilización y acabados exteriores expuestos a agua;
- drenaje pluvial: pendientes por zona climática, canaletas, montantes y tubería de entrega;
- instalaciones exteriores y elementos permitidos en retiros;
- estacionamientos: dotación, accesos, rampas, cajones, maniobras, ventilación, bicicletas, motos y señalización.

## Fuentes oficiales

- A.010 Condiciones Generales de Diseño — RM N.° 191-2021-VIVIENDA.
- A.020 Vivienda — RM N.° 188-2021-VIVIENDA.
- CE.040 Drenaje Pluvial — RM N.° 126-2021-VIVIENDA.
- Se revisó la RM N.° 431-2024-VIVIENDA; su modificación del numeral 21.2.1 de CE.040 no altera los artículos 8, 9, 11, 12 y 13 utilizados en este bloque.

## Resultado

- Versión normativa: `2.1.0`.
- Parámetros totales: `{total_parametros}`.
- Registros `validado_con_numeral`: `{total_validados}`.
- Preguntas técnicas: `{total_preguntas}`.

## Criterios editoriales

- Se separaron valores mínimos, máximos, fórmulas, condiciones, dependencias de cálculo y prohibiciones.
- Se descartó `a020-piso-exterior-antideslizante` porque ya estaba incorporado correctamente en la versión 2.0.0.
- Las pendientes de techo de 12%, 30% y 45% se condicionaron expresamente a la clasificación climática de SENAMHI.
- Se distinguió el parapeto general de A.010 (1.80 m hacia colindantes) del requisito específico de vivienda de A.020 (2.10 m).
- Se evitó presentar impermeabilizantes, espesores de membrana o marcas comerciales como mínimos del RNE.
- Las dimensiones mínimas de canaletas y montantes se acompañaron de la advertencia de que el cálculo hidráulico puede exigir secciones mayores.
""",
        encoding="utf-8",
    )

    print(
        f"Ampliación aplicada: {len(nuevos_parametros)} parámetros, "
        f"{len(nuevas_preguntas)} preguntas, versión {base['version']}."
    )


if __name__ == "__main__":
    main()
