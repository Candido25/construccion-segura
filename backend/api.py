from functools import lru_cache
from pathlib import Path
from typing import Annotated
import json
import unicodedata

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

try:
    from .normativa import (
        ClasificacionParametro,
        buscar_parametros,
        cargar_normativa_tecnica,
        obtener_parametro,
        parametros_visibles,
    )
except ImportError:
    from normativa import (
        ClasificacionParametro,
        buscar_parametros,
        cargar_normativa_tecnica,
        obtener_parametro,
        parametros_visibles,
    )


BASE_DIR = Path(__file__).resolve().parent
RUTA_JSON = BASE_DIR / "preguntas_tecnicas.json"

ORIGENES_PERMITIDOS = [
    "https://www.construccionsegura.org.pe",
    "https://construccionsegura.org.pe",
    "https://candido25.github.io",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

app = FastAPI(
    title="API de Consultas Técnicas - Construcción Segura",
    description="Servidor backend para preguntas técnicas y parámetros estructurados de normativa peruana.",
    version="1.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGENES_PERMITIDOS,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


def normalizar(texto: str) -> str:
    """Normaliza mayúsculas, tildes y espacios para mejorar las búsquedas."""
    texto_normalizado = unicodedata.normalize("NFD", str(texto or "").lower().strip())
    sin_tildes = "".join(
        caracter
        for caracter in texto_normalizado
        if unicodedata.category(caracter) != "Mn"
    )
    return " ".join(sin_tildes.split())


@lru_cache(maxsize=1)
def cargar_base_datos() -> dict:
    """Carga y valida una sola vez la base JSON incluida en el despliegue."""
    if not RUTA_JSON.is_file():
        raise HTTPException(
            status_code=500,
            detail="Base de datos JSON no encontrada en el servidor.",
        )

    try:
        with RUTA_JSON.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except json.JSONDecodeError as error:
        raise HTTPException(
            status_code=500,
            detail="La base de datos JSON no tiene un formato válido.",
        ) from error
    except OSError as error:
        raise HTTPException(
            status_code=500,
            detail="No se pudo leer la base de datos técnica.",
        ) from error

    if not isinstance(datos, dict) or not isinstance(datos.get("categorias"), list):
        raise HTTPException(
            status_code=500,
            detail="La estructura de la base de datos técnica no es válida.",
        )

    return datos


@lru_cache(maxsize=1)
def obtener_indice() -> tuple[dict, ...]:
    """Prepara un índice normalizado para evitar reprocesar el JSON en cada consulta."""
    indice: list[dict] = []

    for categoria in cargar_base_datos().get("categorias", []):
        if not isinstance(categoria, dict):
            continue

        nombre_categoria = str(categoria.get("nombre", "")).strip()
        preguntas = categoria.get("preguntas", [])
        if not isinstance(preguntas, list):
            continue

        for item in preguntas:
            if not isinstance(item, dict):
                continue

            pregunta = str(item.get("pregunta", "")).strip()
            respuesta = str(item.get("respuesta", "")).strip()
            if not pregunta or not respuesta:
                continue

            indice.append(
                {
                    "categoria": nombre_categoria or "Sin categoría",
                    "id": str(item.get("id", "")).strip(),
                    "pregunta": pregunta,
                    "respuesta": respuesta,
                    "categoria_normalizada": normalizar(nombre_categoria),
                    "pregunta_normalizada": normalizar(pregunta),
                    "respuesta_normalizada": normalizar(respuesta),
                }
            )

    return tuple(indice)


def puntuar_resultado(item: dict, termino: str) -> int:
    pregunta = item["pregunta_normalizada"]
    respuesta = item["respuesta_normalizada"]
    categoria = item["categoria_normalizada"]
    texto_completo = f"{pregunta} {categoria} {respuesta}"
    palabras = termino.split()

    puntaje = 0
    if pregunta == termino:
        puntaje += 120
    if pregunta.startswith(termino):
        puntaje += 70
    if termino in pregunta:
        puntaje += 50
    if termino in categoria:
        puntaje += 25
    if termino in respuesta:
        puntaje += 12

    coincidencias = sum(1 for palabra in palabras if palabra in texto_completo)
    puntaje += coincidencias * 8
    if palabras and coincidencias == len(palabras):
        puntaje += 20

    return puntaje


@app.get("/")
def home():
    """Ruta raíz para verificar el estado general del servicio."""
    return {
        "estado": "activo",
        "proyecto": "Construcción Segura API",
        "version": app.version,
        "total_preguntas": len(obtener_indice()),
        "total_parametros_normativos": len(parametros_visibles()),
        "documentacion": "/docs",
        "normativa": "/api/v1/normativa/parametros",
    }


@app.get("/salud")
def salud():
    """Comprobación ligera para monitoreo y diagnóstico del despliegue."""
    base_normativa = cargar_normativa_tecnica()
    return {
        "estado": "activo",
        "total_preguntas": len(obtener_indice()),
        "total_parametros_normativos": len(parametros_visibles()),
        "archivo_preguntas": RUTA_JSON.name,
        "archivo_normativa": "normativa_tecnica.json",
        "version_normativa": base_normativa.version,
    }


@app.get("/categorias")
def obtener_categorias():
    """Lista las categorías disponibles en la base técnica."""
    categorias = sorted({item["categoria"] for item in obtener_indice()})
    return {"total_categorias": len(categorias), "categorias": categorias}


@app.get("/buscar")
def buscar_preguntas(
    termino: Annotated[
        str,
        Query(min_length=2, max_length=120, description="Texto que desea buscar"),
    ],
    limite: Annotated[
        int,
        Query(ge=1, le=50, description="Número máximo de resultados"),
    ] = 10,
):
    """Busca en pregunta, respuesta y categoría, ignorando tildes y mayúsculas."""
    termino_normalizado = normalizar(termino)
    if len(termino_normalizado) < 2:
        raise HTTPException(
            status_code=422,
            detail="Escriba al menos dos caracteres para buscar.",
        )

    encontrados: list[tuple[int, dict]] = []
    for item in obtener_indice():
        puntaje = puntuar_resultado(item, termino_normalizado)
        if puntaje > 0:
            encontrados.append((puntaje, item))

    encontrados.sort(
        key=lambda resultado: (-resultado[0], resultado[1]["pregunta"])
    )
    seleccionados = encontrados[:limite]

    resultados = [
        {
            "categoria": item["categoria"],
            "id": item["id"],
            "pregunta": item["pregunta"],
            "respuesta": item["respuesta"],
        }
        for _, item in seleccionados
    ]

    return {
        "termino_buscado": termino.strip(),
        "total_encontrados": len(encontrados),
        "mostrados": len(resultados),
        "resultados": resultados,
    }


@app.get("/api/v1/normativa/elementos")
def listar_elementos_normativos(
    incluir_borradores: Annotated[
        bool,
        Query(description="Incluye registros editoriales todavía no publicables"),
    ] = False,
):
    """Lista los elementos y categorías disponibles en la base normativa."""
    parametros = parametros_visibles(incluir_borradores)
    elementos = sorted(
        {
            (parametro.categoria, parametro.elemento)
            for parametro in parametros
        }
    )
    return {
        "version": cargar_normativa_tecnica().version,
        "total_elementos": len(elementos),
        "elementos": [
            {"categoria": categoria, "elemento": elemento}
            for categoria, elemento in elementos
        ],
    }


@app.get("/api/v1/normativa/parametros")
def listar_parametros_normativos(
    consulta: Annotated[
        str | None,
        Query(max_length=120, description="Texto libre para filtrar parámetros"),
    ] = None,
    categoria: Annotated[
        str | None,
        Query(max_length=80, description="Filtro parcial por categoría"),
    ] = None,
    elemento: Annotated[
        str | None,
        Query(max_length=120, description="Filtro parcial por elemento"),
    ] = None,
    clasificacion: Annotated[
        ClasificacionParametro | None,
        Query(description="Tipo de regla o parámetro técnico"),
    ] = None,
    incluir_borradores: Annotated[
        bool,
        Query(description="Incluye registros editoriales todavía no publicables"),
    ] = False,
    limite: Annotated[
        int,
        Query(ge=1, le=100, description="Número máximo de resultados"),
    ] = 50,
):
    """Consulta parámetros estructurados con filtros reutilizables por web y app."""
    resultados = buscar_parametros(
        consulta=consulta,
        categoria=categoria,
        elemento=elemento,
        clasificacion=clasificacion,
        incluir_borradores=incluir_borradores,
    )
    mostrados = resultados[:limite]
    return {
        "version": cargar_normativa_tecnica().version,
        "advertencia_general": cargar_normativa_tecnica().advertencia_general,
        "total_encontrados": len(resultados),
        "mostrados": len(mostrados),
        "resultados": [
            parametro.model_dump(mode="json", exclude_none=True)
            for parametro in mostrados
        ],
    }


@app.get("/api/v1/normativa/parametros/{parametro_id}")
def detalle_parametro_normativo(
    parametro_id: str,
    incluir_borradores: Annotated[
        bool,
        Query(description="Permite consultar un registro editorial en borrador"),
    ] = False,
):
    """Devuelve un parámetro por su identificador estable."""
    parametro = obtener_parametro(
        parametro_id,
        incluir_borradores=incluir_borradores,
    )
    if parametro is None:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el parámetro '{parametro_id}'.",
        )
    return parametro.model_dump(mode="json", exclude_none=True)


@app.get("/normativa", deprecated=True)
def normativa_compatibilidad(
    elemento_id: Annotated[
        str | None,
        Query(description="Compatibilidad con el prototipo anterior"),
    ] = None,
):
    """Alias temporal del prototipo; los clientes nuevos deben usar /api/v1."""
    if elemento_id:
        resultados = buscar_parametros(elemento=elemento_id)
    else:
        resultados = parametros_visibles()
    return {
        "version": cargar_normativa_tecnica().version,
        "total_elementos": len(resultados),
        "resultados": [
            parametro.model_dump(mode="json", exclude_none=True)
            for parametro in resultados
        ],
    }
