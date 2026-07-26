from functools import lru_cache
from pathlib import Path
import json
import unicodedata

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parent
RUTA_JSON = BASE_DIR / "preguntas_tecnicas.json"

app = FastAPI(
    title="API de Consultas Técnicas - Construcción Segura",
    description="Servidor backend para responder preguntas técnicas sobre construcción y normativa peruana.",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.construccionsegura.org.pe",
        "https://construccionsegura.org.pe",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


def normalizar(texto: str) -> str:
    """Convierte texto a una forma comparable, sin tildes y en minúsculas."""
    descompuesto = unicodedata.normalize("NFD", texto or "")
    sin_tildes = "".join(
        caracter for caracter in descompuesto if unicodedata.category(caracter) != "Mn"
    )
    return " ".join(sin_tildes.lower().split())


@lru_cache(maxsize=1)
def cargar_base_datos() -> dict:
    """Carga la base una sola vez y valida su estructura principal."""
    if not RUTA_JSON.is_file():
        raise RuntimeError(f"Base de datos JSON no encontrada: {RUTA_JSON}")

    with RUTA_JSON.open("r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    if not isinstance(datos, dict) or not isinstance(datos.get("categorias"), list):
        raise RuntimeError("La base JSON no contiene una lista válida de categorías.")

    return datos


def obtener_datos() -> dict:
    try:
        return cargar_base_datos()
    except (OSError, json.JSONDecodeError, RuntimeError) as error:
        raise HTTPException(
            status_code=500,
            detail="La base de preguntas no está disponible temporalmente.",
        ) from error


@app.get("/")
def home():
    return {
        "estado": "activo",
        "proyecto": "Construcción Segura API",
        "version": app.version,
        "mensaje": "Servidor backend operando correctamente.",
    }


@app.get("/salud")
def salud():
    datos = obtener_datos()
    total_preguntas = sum(
        len(categoria.get("preguntas", []))
        for categoria in datos.get("categorias", [])
    )
    return {
        "estado": "activo",
        "categorias": len(datos.get("categorias", [])),
        "preguntas": total_preguntas,
    }


@app.get("/categorias")
def obtener_categorias():
    datos = obtener_datos()
    categorias = [
        categoria.get("nombre", "Sin categoría")
        for categoria in datos.get("categorias", [])
    ]
    return {"total_categorias": len(categorias), "categorias": categorias}


@app.get("/buscar")
def buscar_preguntas(
    termino: str = Query(min_length=2, max_length=100),
    limite: int = Query(default=10, ge=1, le=50),
):
    datos = obtener_datos()
    termino_normalizado = normalizar(termino)
    resultados = []

    for categoria in datos.get("categorias", []):
        nombre_categoria = categoria.get("nombre", "Sin categoría")
        categoria_normalizada = normalizar(nombre_categoria)

        for item in categoria.get("preguntas", []):
            pregunta = str(item.get("pregunta", "")).strip()
            respuesta = str(item.get("respuesta", "")).strip()
            texto_busqueda = " ".join(
                [normalizar(pregunta), normalizar(respuesta), categoria_normalizada]
            )

            if termino_normalizado not in texto_busqueda:
                continue

            resultados.append(
                {
                    "categoria": nombre_categoria,
                    "id": item.get("id"),
                    "pregunta": pregunta,
                    "respuesta": respuesta,
                }
            )

            if len(resultados) >= limite:
                break

        if len(resultados) >= limite:
            break

    return {
        "termino_buscado": termino.strip(),
        "total_encontrados": len(resultados),
        "limite": limite,
        "resultados": resultados,
    }
