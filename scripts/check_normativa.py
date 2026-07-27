from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from normativa import BaseNormativa, cargar_normativa_tecnica  # noqa: E402


LEGACY_KEYS = {
    "parametros_minimos",
    "tolerancias_admisibles",
    "nivel_riesgo_si_se_ignora",
}


def main() -> None:
    ruta = BACKEND / "normativa_tecnica.json"
    datos_crudos = json.loads(ruta.read_text(encoding="utf-8"))
    texto_crudo = ruta.read_text(encoding="utf-8")

    for clave in LEGACY_KEYS:
        if f'"{clave}"' in texto_crudo:
            raise SystemExit(f"El contrato antiguo todavía contiene la clave rígida: {clave}")

    base: BaseNormativa = cargar_normativa_tecnica()
    if len(base.parametros) < 100:
        raise SystemExit("La base normativa debe contener por lo menos 100 parámetros validados.")

    ids = [parametro.id for parametro in base.parametros]
    if len(ids) != len(set(ids)):
        raise SystemExit("Hay identificadores normativos duplicados.")

    faq_ids = {
        item.get("id")
        for categoria in json.loads(
            (BACKEND / "preguntas_tecnicas.json").read_text(encoding="utf-8")
        ).get("categorias", [])
        for item in categoria.get("preguntas", [])
        if isinstance(item, dict)
    }

    for parametro in base.parametros:
        faltantes = set(parametro.faq_relacionadas) - faq_ids
        if faltantes:
            raise SystemExit(
                f"{parametro.id}: FAQ inexistentes: {', '.join(sorted(faltantes))}"
            )
        if parametro.fuente.tipo == "RNE":
            url = str(parametro.fuente.url_oficial or "")
            if "gob.pe" not in url:
                raise SystemExit(f"{parametro.id}: la fuente RNE no es oficial.")
        if parametro.fuente.numeral_confirmado and not parametro.fuente.numeral:
            raise SystemExit(
                f"{parametro.id}: un numeral marcado como confirmado no puede estar vacío."
            )
        if parametro.estado_revision == "validado_con_numeral":
            if not parametro.fuente.numeral or not parametro.fuente.numeral_confirmado:
                raise SystemExit(
                    f"{parametro.id}: un registro validado requiere numeral confirmado."
                )

    validados = sum(
        parametro.estado_revision == "validado_con_numeral"
        for parametro in base.parametros
    )
    if validados < 99:
        raise SystemExit(
            f"La revisión editorial debe conservar al menos 99 numerales validados; hay {validados}."
        )
    if base.version != "1.4.0":
        raise SystemExit(f"La versión normativa esperada es 1.4.0 y se recibió {base.version}.")

    BaseNormativa.model_validate(datos_crudos)

    import api  # noqa: E402

    rutas = {ruta.path for ruta in api.app.routes}
    esperadas = {
        "/api/v1/normativa/elementos",
        "/api/v1/normativa/parametros",
        "/api/v1/normativa/parametros/{parametro_id}",
        "/normativa",
    }
    faltan_rutas = esperadas - rutas
    if faltan_rutas:
        raise SystemExit(
            "Faltan rutas normativas: " + ", ".join(sorted(faltan_rutas))
        )

    listado = api.listar_parametros_normativos()
    if listado["total_encontrados"] != len(base.parametros):
        raise SystemExit("El endpoint no devuelve la totalidad del piloto visible.")

    desarrollo = api.detalle_parametro_normativo(
        "e060-desarrollo-traccion-longitud-minima"
    )
    if desarrollo["valor"]["valor"] != 300:
        raise SystemExit("La longitud mínima de desarrollo a tracción debe ser 300 mm.")

    separacion = api.detalle_parametro_normativo(
        "e030-separacion-edificios-formula-minima"
    )
    if "0.02" not in separacion["valor"]["formula"] or "0.03" not in separacion["valor"]["formula"]:
        raise SystemExit("La fórmula de separación sísmica no conserva la E.030 2026.")

    deriva = api.detalle_parametro_normativo(
        "e030-albanileria-distorsion-entrepiso-maxima"
    )
    if deriva["valor"]["valor"] != 0.005:
        raise SystemExit("La distorsión máxima para albañilería debe ser 0.005.")

    detalle = api.detalle_parametro_normativo(
        "a010-escalera-contrahuella-maxima"
    )
    if detalle["valor"]["valor"] != 0.18:
        raise SystemExit("El detalle normativo de prueba no conserva el valor esperado.")

    recubrimiento = api.detalle_parametro_normativo(
        "e060-recubrimiento-contra-suelo-minimo"
    )
    if recubrimiento["valor"]["valor"] != 70:
        raise SystemExit("El recubrimiento contra suelo debe conservar 70 mm.")

    preguntas = json.loads(
        (BACKEND / "preguntas_tecnicas.json").read_text(encoding="utf-8")
    )
    todas = [
        item
        for categoria in preguntas.get("categorias", [])
        for item in categoria.get("preguntas", [])
        if isinstance(item, dict)
    ]
    if len(todas) < 1569:
        raise SystemExit("El lote 4 requiere por lo menos 1569 preguntas técnicas.")
    respuesta_q307 = next(
        item.get("respuesta", "") for item in todas if item.get("id") == "q307"
    )
    if "70 mm" not in respuesta_q307 or "75 mm" in respuesta_q307:
        raise SystemExit("La FAQ q307 debe indicar el recubrimiento correcto de 70 mm.")

    print(
        "Normativa técnica válida:",
        f"{len(base.parametros)} parámetros,",
        f"{len({p.elemento for p in base.parametros})} elementos,",
        f"{len({p.categoria for p in base.parametros})} categorías.",
    )


if __name__ == "__main__":
    main()
