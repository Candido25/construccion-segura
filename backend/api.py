from fastapi import FastAPI, HTTPException
import json
import os

# Inicializamos la aplicación de la API con metadatos profesionales
app = FastAPI(
    title="API de Consultas Técnicas - Construcción Segura",
    description="Servidor backend para responder preguntas técnicas sobre ingeniería civil y normativas.",
    version="1.0.0"
)

# Ruta del archivo JSON que contiene las 1519 preguntas
RUTA_JSON = "backend/preguntas_tecnicas.json"

def cargar_base_datos():
    """Función de soporte para leer de forma segura el archivo JSON en el servidor."""
    if not os.path.exists(RUTA_JSON):
        raise HTTPException(status_code=500, detail="Base de datos JSON no encontrada en el servidor.")
    
    with open(RUTA_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/")
def home():
    """Ruta raíz para verificar que el servidor de la API está en línea."""
    return {
        "estado": "activo",
        "proyecto": "Construcción Segura API",
        "mensaje": "Servidor backend operando correctamente."
    }

@app.get("/categorias")
def obtener_categorias():
    """Endpoint para listar todas las categorías de ingeniería civil disponibles."""
    datos = cargar_base_datos()
    # Extraemos solo los nombres de las categorías para una vista rápida
    lista_categorias = [cat["nombre"] for cat in datos.get("categorias", [])]
    return {"total_categorias": len(lista_categorias), "categorias": lista_categorias}

@app.get("/buscar")
def buscar_preguntas(termino: str):
    """
    Endpoint principal del motor de búsqueda.
    Ejemplo de uso: /buscar?termino=zapatas
    """
    datos = cargar_base_datos()
    termino = termino.lower().strip()
    resultados = []

    # Recorremos la estructura jerárquica del JSON buscando coincidencias
    for cat in datos.get("categorias", []):
        nombre_cat = cat["nombre"]
        for item in cat.get("preguntas", []):
            preg = item.get("pregunta", "")
            resp = item.get("respuesta", "")
            
            # Si el término coincide en la pregunta o respuesta, lo guardamos
            if termino in preg.lower() or termino in resp.lower():
                resultados.append({
                    "categoria": nombre_cat,
                    "id": item.get("id"),
                    "pregunta": preg,
                    "respuesta": resp
                })

    if not resultados:
        return {"mensaje": f"No se encontraron resultados para el término: '{termino}'"}

    return {
        "termino_buscado": termino,
        "total_encontrados": len(resultados),
        "resultados": resultados
    }