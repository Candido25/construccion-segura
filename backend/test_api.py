from api import (
    buscar_preguntas,
    cargar_base_datos,
    cargar_normativa_tecnica,
    listar_parametros_normativos,
    obtener_indice,
    salud,
)


def test_backend_data_files_are_valid():
    datos_preguntas = cargar_base_datos()
    datos_normativa = cargar_normativa_tecnica()

    assert isinstance(datos_preguntas["categorias"], list)
    assert len(obtener_indice()) > 0
    assert len(datos_normativa.parametros) > 0


def test_health_endpoint_reports_loaded_data():
    payload = salud()

    assert payload["estado"] == "activo"
    assert payload["total_preguntas"] > 0
    assert payload["total_parametros_normativos"] > 0


def test_search_endpoint_returns_limited_results():
    payload = buscar_preguntas(termino="cimiento", limite=3)

    assert payload["mostrados"] <= 3
    assert payload["total_encontrados"] >= payload["mostrados"]
    assert payload["resultados"]


def test_normative_parameters_endpoint_returns_structured_results():
    payload = listar_parametros_normativos(consulta="escalera", limite=5)

    assert payload["mostrados"] <= 5
    assert payload["resultados"]
