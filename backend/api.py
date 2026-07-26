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

from pydantic import BaseModel
from typing import List, Dict, Optional

class ParametrosMinimos(BaseModel):
    f_c_minimo: Optional[str] = None
    dimension_menor_minima: Optional[str] = None
    recubrimiento_libre: Optional[str] = None
    peralte_minimo: Optional[str] = None
    concreto_ciclopeo_cimiento: Optional[str] = None

class ToleranciasAdmisibles(BaseModel):
    plumb_verticalidad: Optional[str] = None
    posicion_acero: Optional[str] = None
    nivelacion_fondo: Optional[str] = None
    recubrimiento_inferior: Optional[str] = None

class ElementoNormativo(BaseModel):
    id: str
    categoria: str
    elemento: str
    codigo_normativo: str
    parametros_minimos: ParametrosMinimos
    tolerancias_admisibles: ToleranciasAdmisibles
    recomendacion_tecnica: str
    nivel_riesgo_si_se_ignora: str


def normalizar(texto: str) -> str:
    """Normaliza mayúsculas, tildes y espacios para mejorar las búsquedas."""
    texto_normalizado = unicodedata.normalize("NFD", str(texto or "").lower().strip())
    sin_tildes = "".join(
        caracter
        for caracter in texto_normalizado
        if unicodedata.category(caracter) != "Mn"
    )
    return " ".join(sin_tildes.split())

RUTA_NORMATIVA_JSON = BASE_DIR / "normativa_tecnica.json"

@lru_cache(maxsize=1)
def cargar_normativa_tecnica() -> dict:
    """Carga y valida el archivo de parámetros y tolerancias técnicas."""
    if not RUTA_NORMATIVA_JSON.is_file():
        raise HTTPException(
            status_code=500,
            detail="Base de datos de normativa técnica no encontrada en el servidor.",
        )
    try:
        with RUTA_NORMATIVA_JSON.open("r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Error al procesar la base de datos normativa.",
        ) from error

@app.get("/normativa")
def obtener_normativa(
    elemento_id: Annotated[
        Optional[str],
        Query(description="Filtrar por ID específico del elemento estructural")
    ] = None
):
    """
    Expone los parámetros mínimos, normativas y tolerancias para la autoconstrucción.
    Consumido tanto por la web estática como por el futuro aplicativo Android.
    """
    datos = cargar_normativa_tecnica()
    elementos = datos.get("elementos", [])
    
    if elemento_id:
        filtrados = [el for el in elementos if el.get("id") == elemento_id]
        if not filtrados:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró el elemento con ID '{elemento_id}'."
            )
        return {"total": len(filtrados), "resultados": filtrados}
    
    return {
        "version": datos.get("version", "1.0.0"),
        "descripcion": datos.get("descripcion"),
        "total_elementos": len(elementos),
        "resultados": elementos
    }

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
