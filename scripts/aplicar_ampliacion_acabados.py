from __future__ import annotations

from pathlib import Path
import base64
import gzip
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
NORMATIVA = BACKEND / "normativa_tecnica.json"
PREGUNTAS = BACKEND / "preguntas_tecnicas.json"
CHECK = ROOT / "scripts" / "check_normativa.py"
DATA_DIR = ROOT / "scripts" / "data_acabados"
DOC = ROOT / "docs" / "VALIDACION_ACABADOS_CONSTRUCCION_2026-07-27.md"

PAYLOAD_SHA256 = "4fe4a9cf94961b087d4337853817f31e1ff38a063a00453d139777495967b85e"


def reemplazar_unico(texto: str, anterior: str, nuevo: str) -> str:
    if texto.count(anterior) != 1:
        raise SystemExit(f"No se encontró una única coincidencia para: {anterior}")
    return texto.replace(anterior, nuevo, 1)


def cargar_registros() -> list[dict]:
    rutas = [DATA_DIR / f"part{indice:02d}.txt" for indice in range(1, 5)]
    rutas.extend(sorted(DATA_DIR.glob("seg*.txt")))
    if len(rutas) != 24 or any(not ruta.is_file() for ruta in rutas):
        raise SystemExit("El inventario fragmentado debe contener exactamente 24 archivos verificados.")

    texto = "".join(ruta.read_text(encoding="utf-8").strip() for ruta in rutas)
    huella = hashlib.sha256(texto.encode("utf-8")).hexdigest()
    if huella != PAYLOAD_SHA256:
        raise SystemExit(f"La huella del inventario no coincide: {huella}")

    comprimido = base64.b64decode(texto, validate=True)
    registros = json.loads(gzip.decompress(comprimido).decode("utf-8"))
    if len(registros) != 250:
        raise SystemExit(f"Se esperaban 250 registros y se recibieron {len(registros)}.")
    return registros


def main() -> None:
    registros = cargar_registros()
    base = json.loads(NORMATIVA.read_text(encoding="utf-8"))
    banco = json.loads(PREGUNTAS.read_text(encoding="utf-8"))

    ids_nuevos = [item["id"] for item in registros]
    if len(ids_nuevos) != len(set(ids_nuevos)):
        raise SystemExit("El inventario contiene identificadores duplicados.")

    ids_existentes = {item["id"] for item in base["parametros"]}
    repetidos = sorted(set(ids_nuevos) & ids_existentes)
    if repetidos:
        raise SystemExit("Los siguientes parámetros ya existen: " + ", ".join(repetidos))

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
    nuevos_parametros: list[dict] = []
    nuevas_preguntas: list[dict] = []

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
    base["version"] = "2.3.0"
    base["fecha_revision"] = "2026-07-27"

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
    total_criterios = sum(
        item.get("estado_revision") == "criterio_tecnico_revisado"
        for item in base["parametros"]
    )

    if total_parametros != 1376:
        raise SystemExit(f"Se esperaban 1376 parámetros y se obtuvieron {total_parametros}.")
    if total_preguntas != 2839:
        raise SystemExit(f"Se esperaban 2839 preguntas y se obtuvieron {total_preguntas}.")
    if total_validados != 1171:
        raise SystemExit(f"Se esperaban 1171 registros validados con numeral y se obtuvieron {total_validados}.")
    if total_criterios != 187:
        raise SystemExit(f"Se esperaban 187 criterios técnicos revisados y se obtuvieron {total_criterios}.")

    NORMATIVA.write_text(
        json.dumps(base, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    PREGUNTAS.write_text(
        json.dumps(banco, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    check = CHECK.read_text(encoding="utf-8")
    check = reemplazar_unico(check, "if len(base.parametros) < 1126:", "if len(base.parametros) < 1376:")
    check = reemplazar_unico(check, "por lo menos 1126 parámetros revisados", "por lo menos 1376 parámetros revisados")
    check = reemplazar_unico(check, "if validados < 1092:", "if validados < 1171:")
    check = reemplazar_unico(check, "al menos 1092 numerales RNE validados", "al menos 1171 numerales RNE validados")
    check = reemplazar_unico(check, 'if base.version != "2.2.0":', 'if base.version != "2.3.0":')
    check = reemplazar_unico(check, "if criterios < 16:", "if criterios < 187:")
    check = reemplazar_unico(check, "al menos 16 criterios técnicos revisados", "al menos 187 criterios técnicos revisados")
    check = reemplazar_unico(check, "if len(todas) < 2589:", "if len(todas) < 2839:")
    check = reemplazar_unico(
        check,
        "La base ampliada de obras preliminares y seguridad requiere por lo menos 2589 preguntas técnicas.",
        "La base ampliada de acabados de construcción requiere por lo menos 2839 preguntas técnicas.",
    )

    bloque_pruebas = '''    vidrio_junta = api.detalle_parametro_normativo("e040-paneles-separacion-minima")
    if vidrio_junta["valor"]["valor"] != 4:
        raise SystemExit("La separación mínima general entre paneles de vidrio debe conservar 4 mm.")

    vidrio_cinta = api.detalle_parametro_normativo("e040-cinta-espesor-minimo")
    if vidrio_cinta["valor"]["valor"] != 2:
        raise SystemExit("La cinta de doble contacto debe conservar 2 mm mínimos.")

    vidrio_insulado = api.detalle_parametro_normativo("e040-insulado-espera-manipulacion")
    if vidrio_insulado["valor"]["valor"] != 24:
        raise SystemExit("El vidrio insulado debe conservar 24 horas antes de manipularse.")

    acabado = api.detalle_parametro_normativo("criterio-enchape-juntas-no-cero")
    if acabado["estado_revision"] != "criterio_tecnico_revisado":
        raise SystemExit("Las juntas de enchape deben conservarse como criterio técnico revisado.")

'''
    check = reemplazar_unico(
        check,
        "    preguntas = json.loads(\n",
        bloque_pruebas + "    preguntas = json.loads(\n",
    )
    CHECK.write_text(check, encoding="utf-8")

    DOC.write_text(
        f"""# Validación normativa y técnica de acabados de construcción — 27 de julio de 2026

## Alcance

Se incorporaron **{len(nuevos_parametros)} parámetros** y **{len(nuevas_preguntas)} preguntas** después de comparar el inventario con los 1,126 parámetros de la versión 2.2.0.

## Contenido incorporado

- Norma E.040 Vidrio actualizada mediante RM N.° 139-2025-VIVIENDA;
- documentación, cálculo, seguridad frente a impacto y selección de espesores de vidrio;
- perfiles, anclajes, siliconas, cintas, almacenamiento, manipulación e inspección;
- tarrajeos, revoques, enlucidos, fisuras, humedad, planeidad y aplomo;
- contrapisos, impermeabilización previa, cerámicos, porcelanatos, piedra, adhesivos y fragua;
- preparación, imprimación, empaste y pintura de concreto, madera y metal;
- cielorrasos y sistemas constructivos en seco;
- carpinterías, sellos, drenajes, herrajes y acristalamiento;
- inspección, muestras, trazabilidad, protección y recepción de acabados.

## Fuentes

- Norma Técnica E.040 Vidrio — RM N.° 139-2025-VIVIENDA.
- Publicaciones oficiales de formación técnica SENCICO sobre pintura, enchapado, drywall y carpintería de acabados.

## Resultado

- Versión normativa: `2.3.0`.
- Parámetros totales: `{total_parametros}`.
- Registros `validado_con_numeral`: `{total_validados}`.
- Criterios técnicos revisados: `{total_criterios}`.
- Preguntas técnicas: `{total_preguntas}`.

## Criterios editoriales

- Se conservaron las reglas existentes de A.010 y A.020 para zonas húmedas, pisos antideslizantes, cocinas y cerramientos exteriores.
- No se asignaron espesores universales a tarrajeos, contrapisos, adhesivos, juntas, capas de pintura ni perfilería drywall cuando dependen del sistema y del fabricante.
- Las buenas prácticas se identifican como `criterio_tecnico_revisado`; no se presentan como mínimos del RNE.
- Los límites cuantitativos de vidrio se reservaron a cláusulas confirmadas de la E.040 vigente.
- La información no reemplaza planos, especificaciones, fichas técnicas, ensayos ni supervisión profesional.
""",
        encoding="utf-8",
    )

    print(
        f"Ampliación aplicada: {len(nuevos_parametros)} parámetros, "
        f"{len(nuevas_preguntas)} preguntas, versión {base['version']}."
    )


if __name__ == "__main__":
    main()
