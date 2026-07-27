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
    if len(base.parametros) < 20:
        raise SystemExit("La fase piloto debe contener por lo menos 20 parámetros.")

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
    if validados < 19:
        raise SystemExit(
            f"La revisión editorial debe conservar al menos 19 numerales validados; hay {validados}."
        )
    if base.version == "1.0.0-piloto":
        raise SystemExit("La versión piloto inicial ya no debe permanecer activa.")

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

    detalle = api.detalle_parametro_normativo(
        "a010-escalera-contrahuella-maxima"
    )
    if detalle["valor"]["valor"] != 0.18:
        raise SystemExit("El detalle normativo de prueba no conserva el valor esperado.")

    print(
        "Normativa técnica válida:",
        f"{len(base.parametros)} parámetros,",
        f"{len({p.elemento for p in base.parametros})} elementos,",
        f"{len({p.categoria for p in base.parametros})} categorías.",
    )


if __name__ == "__main__":
    main()
