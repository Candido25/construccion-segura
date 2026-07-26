from functools import lru_cache
from pathlib import Path
from typing import Annotated
import json
import unicodedata

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

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
    description="Servidor backend para responder preguntas técnicas sobre construcción y normativa peruana.",
    version="1.1.1",
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
        "documentacion": "/docs",
    }


@app.get("/salud")
def salud():
    """Comprobación ligera para monitoreo y diagnóstico del despliegue."""
    return {
        "estado": "activo",
        "total_preguntas": len(obtener_indice()),
        "archivo_datos": RUTA_JSON.name,
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
