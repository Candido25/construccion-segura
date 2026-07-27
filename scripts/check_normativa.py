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
    if len(base.parametros) < 1126:
        raise SystemExit("La base normativa debe contener por lo menos 1126 parámetros revisados.")

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
        if parametro.fuente.tipo in {"RNE", "normativa_nacional", "manual_oficial"}:
            url = str(parametro.fuente.url_oficial or "")
            if "gob.pe" not in url:
                raise SystemExit(f"{parametro.id}: la fuente oficial no apunta a gob.pe.")
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
    if validados < 1092:
        raise SystemExit(
            f"La revisión editorial debe conservar al menos 1092 numerales RNE validados; hay {validados}."
        )
    if base.version != "2.2.0":
        raise SystemExit(f"La versión normativa esperada es 2.2.0 y se recibió {base.version}.")

    oficiales = sum(
        parametro.estado_revision == "validado_con_fuente_oficial"
        for parametro in base.parametros
    )
    criterios = sum(
        parametro.estado_revision == "criterio_tecnico_revisado"
        for parametro in base.parametros
    )
    if oficiales < 17:
        raise SystemExit(f"El bloque requiere al menos 17 referencias oficiales externas al RNE; hay {oficiales}.")
    if criterios < 16:
        raise SystemExit(f"El bloque requiere al menos 16 criterios técnicos revisados; hay {criterios}.")

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

    dano = api.detalle_parametro_normativo("edan-vivienda-inhabitable")
    if dano["estado_revision"] != "validado_con_fuente_oficial":
        raise SystemExit("La clasificación EDAN debe conservar su estado oficial.")

    prueba = api.detalle_parametro_normativo("e060-prueba-carga-mantenimiento-total")
    if prueba["valor"]["valor"] != 24:
        raise SystemExit("La prueba de carga debe conservar 24 horas.")

    calzadura = api.detalle_parametro_normativo("e050-calzadura-panel-ancho-maximo")
    if calzadura["valor"]["valor"] != 1.2:
        raise SystemExit("El panel de calzadura debe conservar 1.20 m.")

    demolicion = api.detalle_parametro_normativo("g050-demolicion-vivalva-zona-seguridad")
    if demolicion["valor"]["valor"] != 8:
        raise SystemExit("La zona de seguridad de la cuchara vivalva debe ser 8 m.")

    licencia = api.detalle_parametro_normativo("licencia-vigencia-prorroga")
    if "36 meses" not in licencia["valor"]["texto"] or "12 meses" not in licencia["valor"]["texto"]:
        raise SystemExit("La licencia no conserva su vigencia y prórroga.")

    criterio = api.detalle_parametro_normativo("criterio-ampliacion-evaluar-edificio-completo")
    if criterio["estado_revision"] != "criterio_tecnico_revisado":
        raise SystemExit("La ampliación debe mostrarse como criterio técnico revisado.")

    dotacion = api.detalle_parametro_normativo(
        "is010-dotacion-vivienda-calido"
    )
    if dotacion["valor"]["valor"] != 169:
        raise SystemExit("La dotación de clima cálido debe ser 169 L/persona/día.")

    ventilacion = api.detalle_parametro_normativo(
        "a010-ventilacion-natural-vano-minimo"
    )
    if "0.05" not in ventilacion["valor"]["formula"]:
        raise SystemExit("La ventilación natural debe conservar la regla de 5%.")

    desague = api.detalle_parametro_normativo(
        "is010-desague-pendiente-hasta-75"
    )
    if desague["valor"]["valor"] != 1.5:
        raise SystemExit("La pendiente hasta 75 mm debe conservar 1.5%.")

    telecom = api.detalle_parametro_normativo(
        "em020-pau-caja-dimensiones-minimas"
    )
    if "300 mm" not in telecom["valor"]["texto"]:
        raise SystemExit("La caja PAU no conserva sus dimensiones mínimas.")

    termica = api.detalle_parametro_normativo(
        "em110-u-techo-altoandino-maxima"
    )
    if termica["valor"]["valor"] != 0.83:
        raise SystemExit("La transmitancia máxima del techo altoandino debe ser 0.83.")

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

    mezclado = api.detalle_parametro_normativo(
        "e060-mezclado-tiempo-minimo"
    )
    if mezclado["valor"]["valor"] != 90:
        raise SystemExit("El tiempo mínimo de mezclado debe conservar 90 segundos.")

    tubo_columna = api.detalle_parametro_normativo(
        "e060-columna-tuberias-area-maxima"
    )
    if tubo_columna["valor"]["valor"] != 4:
        raise SystemExit("Las tuberías en columna deben conservar el límite de 4%.")

    caida = api.detalle_parametro_normativo(
        "g050-caida-anclaje-resistencia-minima"
    )
    if caida["valor"]["valor"] != 2265:
        raise SystemExit("El anclaje anticaídas debe conservar 2265 kgf.")

    unidades = api.detalle_parametro_normativo(
        "e070-unidad-concreto-edad-minima"
    )
    if unidades["valor"]["valor"] != 28:
        raise SystemExit("Las unidades de concreto deben conservar 28 días mínimos.")


    rampa = api.detalle_parametro_normativo("a120-rampa-accesible-ancho-minimo")
    if rampa["valor"]["valor"] != 1.0:
        raise SystemExit("La rampa accesible debe conservar 1.00 m de ancho mínimo.")

    emergencia = api.detalle_parametro_normativo("a130-iluminacion-emergencia-autonomia")
    if emergencia["valor"]["valor"] != 1.5:
        raise SystemExit("La iluminación de emergencia debe conservar 1.5 horas.")

    incendio = api.detalle_parametro_normativo("a130-vivienda-11-20-reserva-minima")
    if incendio["valor"]["valor"] != 28:
        raise SystemExit("La reserva contra incendios debe conservar 28 m³.")

    gas_presion = api.detalle_parametro_normativo("em040-glp-presion-maxima-despues-regulador")
    if gas_presion["valor"]["valor"] != 20:
        raise SystemExit("La presión máxima de GLP debe conservar 20 psig.")

    pozo_luz = api.detalle_parametro_normativo("em070-pozo-iluminacion-minima")
    if pozo_luz["valor"]["valor"] != 50:
        raise SystemExit("El pozo de ascensor debe conservar 50 lux.")

    minicarga = api.detalle_parametro_normativo("em070-minicarga-capacidad-maxima")
    if minicarga["valor"]["valor"] != 300:
        raise SystemExit("La minicarga debe conservar 300 kg.")

    chimenea = api.detalle_parametro_normativo("em060-chimenea-metalica-vivienda-prohibida")
    if chimenea["clasificacion"] != "prohibicion":
        raise SystemExit("La chimenea metálica en vivienda debe conservarse como prohibición.")

    gas = api.detalle_parametro_normativo("em040-edificacion-nueva-aberturas-area-total")
    if gas["valor"]["valor"] != 280:
        raise SystemExit("La ventilación de gas debe conservar 280 cm² en edificaciones nuevas.")

    solar = api.detalle_parametro_normativo("em080-fv-superficie-preliminar-kwp")
    if "10" not in solar["valor"]["formula"]:
        raise SystemExit("La superficie preliminar fotovoltaica debe conservar 10 m²/kWp.")

    ascensor = api.detalle_parametro_normativo("em070-cuarto-maquinas-iluminacion")
    if ascensor["valor"]["valor"] != 200:
        raise SystemExit("El cuarto de máquinas debe conservar 200 lux.")

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
    if len(todas) < 2589:
        raise SystemExit("La base ampliada de obras preliminares y seguridad requiere por lo menos 2589 preguntas técnicas.")
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
