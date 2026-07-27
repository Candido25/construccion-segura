# Contrato de normativa técnica

## Objetivo

`backend/normativa_tecnica.json` contiene parámetros estructurados que pueden ser
consumidos por la web y por la futura aplicación Mi Casa Segura. No reemplaza a
`preguntas_tecnicas.json`: la base de preguntas explica; la base normativa
estructura valores, condiciones, fórmulas y reglas.

## Principios

1. Cada registro representa un solo parámetro o regla.
2. Un valor normativo se distingue de una recomendación o de un dato sujeto a cálculo.
3. Toda atribución oficial conserva tipo de fuente, norma o manual, dispositivo, referencia y URL oficial.
4. Cada registro enlaza las preguntas de las que fue extraído.
5. Los numerales no se inventan. Mientras no estén confirmados, se conserva
   `numeral: null`, `numeral_confirmado: false` y el estado piloto.
6. Un parámetro retirado no se entrega por la API.
7. La interfaz futura debe mostrar siempre la advertencia y las condiciones.

## Clasificaciones

- `minimo_normativo`
- `maximo_normativo`
- `formula_normativa`
- `condicion_normativa`
- `depende_calculo`
- `prohibicion`
- `recomendacion`

## Tipos de fuente

- `RNE`: norma integrante del Reglamento Nacional de Edificaciones.
- `normativa_nacional`: ley, decreto, reglamento o trámite oficial distinto del RNE.
- `manual_oficial`: manual o guía aprobada por una entidad pública.
- `criterio_tecnico`: criterio profesional que no se presenta como obligación normativa.
- `fuente_interna`: contenido editorial interno.

## Estados editoriales

- `piloto_verificado`: valor revisado para el piloto; numeral aún pendiente.
- `validado_con_numeral`: cláusula del RNE y numeral confirmados.
- `validado_con_fuente_oficial`: referencia confirmada de normativa nacional o manual oficial.
- `criterio_tecnico_revisado`: recomendación o decisión sujeta a diagnóstico o cálculo profesional.
- `borrador`: no se entrega por defecto.
- `retirado`: excluido incluso de consultas editoriales.

## API

- `GET /api/v1/normativa/elementos`
- `GET /api/v1/normativa/parametros`
- `GET /api/v1/normativa/parametros/{id}`

`GET /normativa` queda temporalmente como alias del prototipo anterior y está
marcado como obsoleto.
