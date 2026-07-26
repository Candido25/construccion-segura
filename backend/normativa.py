from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal
import json
import unicodedata

from fastapi import HTTPException
from pydantic import BaseModel, Field, HttpUrl, ValidationError, model_validator


BASE_DIR = Path(__file__).resolve().parent
RUTA_NORMATIVA_JSON = BASE_DIR / "normativa_tecnica.json"

ClasificacionParametro = Literal[
    "minimo_normativo",
    "maximo_normativo",
    "formula_normativa",
    "condicion_normativa",
    "depende_calculo",
    "prohibicion",
    "recomendacion",
]

EstadoRevision = Literal[
    "piloto_verificado",
    "validado_con_numeral",
    "borrador",
    "retirado",
]


class ValorTecnico(BaseModel):
    tipo: Literal["numero", "rango", "formula", "texto", "sin_valor_universal"]
    valor: float | int | None = None
    minimo: float | int | None = None
    maximo: float | int | None = None
    unidad: str | None = None
    formula: str | None = None
    texto: str

    @model_validator(mode="after")
    def validar_contenido(self) -> "ValorTecnico":
        if self.tipo == "numero" and self.valor is None:
            raise ValueError("Un valor numérico requiere el campo 'valor'.")
        if self.tipo == "rango" and (self.minimo is None or self.maximo is None):
            raise ValueError("Un rango requiere 'minimo' y 'maximo'.")
        if self.tipo == "formula" and not self.formula:
            raise ValueError("Un valor de tipo fórmula requiere el campo 'formula'.")
        return self


class FuenteTecnica(BaseModel):
    tipo: Literal["RNE", "criterio_tecnico", "fuente_interna"]
    norma: str
    denominacion: str
    dispositivo: str | None = None
    numeral: str | None = None
    numeral_confirmado: bool = False
    url_oficial: HttpUrl | None = None


class ParametroNormativo(BaseModel):
    id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    categoria: str
    elemento: str
    parametro: str
    clasificacion: ClasificacionParametro
    valor: ValorTecnico
    condiciones: list[str] = Field(default_factory=list)
    fuente: FuenteTecnica
    estado_revision: EstadoRevision
    advertencia: str
    faq_relacionadas: list[str] = Field(default_factory=list)
    fecha_revision: str

    @model_validator(mode="after")
    def validar_trazabilidad(self) -> "ParametroNormativo":
        if self.fuente.tipo == "RNE" and not self.fuente.url_oficial:
            raise ValueError("Todo parámetro atribuido al RNE requiere una URL oficial.")
        if self.clasificacion in {
            "minimo_normativo",
            "maximo_normativo",
            "formula_normativa",
            "condicion_normativa",
            "prohibicion",
        } and self.fuente.tipo != "RNE":
            raise ValueError("Los requisitos normativos deben apuntar a una fuente RNE.")
        if not self.faq_relacionadas:
            raise ValueError("Cada parámetro debe conservar trazabilidad con al menos una FAQ.")
        return self


class BaseNormativa(BaseModel):
    version: str
    pais: str
    descripcion: str
    fecha_revision: str
    advertencia_general: str
    parametros: list[ParametroNormativo]


def normalizar_texto(texto: str) -> str:
    texto_normalizado = unicodedata.normalize("NFD", str(texto or "").lower().strip())
    sin_tildes = "".join(
        caracter
        for caracter in texto_normalizado
        if unicodedata.category(caracter) != "Mn"
    )
    return " ".join(sin_tildes.split())


@lru_cache(maxsize=1)
def cargar_normativa_tecnica() -> BaseNormativa:
    """Carga y valida una sola vez la base normativa estructurada."""
    if not RUTA_NORMATIVA_JSON.is_file():
        raise HTTPException(
            status_code=500,
            detail="Base de normativa técnica no encontrada en el servidor.",
        )

    try:
        with RUTA_NORMATIVA_JSON.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        return BaseNormativa.model_validate(datos)
    except json.JSONDecodeError as error:
        raise HTTPException(
            status_code=500,
            detail="La base de normativa técnica no tiene un JSON válido.",
        ) from error
    except ValidationError as error:
        raise HTTPException(
            status_code=500,
            detail="La base de normativa técnica no cumple el contrato de datos.",
        ) from error
    except OSError as error:
        raise HTTPException(
            status_code=500,
            detail="No se pudo leer la base de normativa técnica.",
        ) from error


def parametros_visibles(incluir_borradores: bool = False) -> tuple[ParametroNormativo, ...]:
    parametros = cargar_normativa_tecnica().parametros
    if incluir_borradores:
        return tuple(parametro for parametro in parametros if parametro.estado_revision != "retirado")
    return tuple(
        parametro
        for parametro in parametros
        if parametro.estado_revision not in {"borrador", "retirado"}
    )


def buscar_parametros(
    *,
    consulta: str | None = None,
    categoria: str | None = None,
    elemento: str | None = None,
    clasificacion: ClasificacionParametro | None = None,
    incluir_borradores: bool = False,
) -> tuple[ParametroNormativo, ...]:
    consulta_normalizada = normalizar_texto(consulta or "")
    categoria_normalizada = normalizar_texto(categoria or "")
    elemento_normalizado = normalizar_texto(elemento or "")

    resultados: list[ParametroNormativo] = []
    for parametro in parametros_visibles(incluir_borradores):
        if clasificacion and parametro.clasificacion != clasificacion:
            continue
        if categoria_normalizada and categoria_normalizada not in normalizar_texto(parametro.categoria):
            continue
        if elemento_normalizado and elemento_normalizado not in normalizar_texto(parametro.elemento):
            continue
        if consulta_normalizada:
            texto = normalizar_texto(
                " ".join(
                    [
                        parametro.id,
                        parametro.categoria,
                        parametro.elemento,
                        parametro.parametro,
                        parametro.valor.texto,
                        " ".join(parametro.condiciones),
                    ]
                )
            )
            if consulta_normalizada not in texto:
                continue
        resultados.append(parametro)

    return tuple(sorted(resultados, key=lambda item: (item.categoria, item.elemento, item.parametro)))


def obtener_parametro(
    parametro_id: str,
    *,
    incluir_borradores: bool = False,
) -> ParametroNormativo | None:
    for parametro in parametros_visibles(incluir_borradores):
        if parametro.id == parametro_id:
            return parametro
    return None
