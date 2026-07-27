# Validación normativa de azoteas, cubiertas, drenaje pluvial y estacionamientos — 27 de julio de 2026

## Alcance

Se incorporaron **96 parámetros** y **96 preguntas** sin fijar una cuota artificial. El inventario se obtuvo del contraste de las reglas aplicables a vivienda y autoconstrucción contenidas en A.010, A.020 y CE.040.

## Contenido incorporado

- azoteas: usos, accesos, porcentaje techable, retranques, parapetos y barandas;
- cubiertas ligeras: fijación, hermeticidad, pendiente, comportamiento térmico y mantenimiento;
- impermeabilización y acabados exteriores expuestos a agua;
- drenaje pluvial: pendientes por zona climática, canaletas, montantes y tubería de entrega;
- instalaciones exteriores y elementos permitidos en retiros;
- estacionamientos: dotación, accesos, rampas, cajones, maniobras, ventilación, bicicletas, motos y señalización.

## Fuentes oficiales

- A.010 Condiciones Generales de Diseño — RM N.° 191-2021-VIVIENDA.
- A.020 Vivienda — RM N.° 188-2021-VIVIENDA.
- CE.040 Drenaje Pluvial — RM N.° 126-2021-VIVIENDA.
- Se revisó la RM N.° 431-2024-VIVIENDA; su modificación del numeral 21.2.1 de CE.040 no altera los artículos 8, 9, 11, 12 y 13 utilizados en este bloque.

## Resultado

- Versión normativa: `2.1.0`.
- Parámetros totales: `982`.
- Registros `validado_con_numeral`: `948`.
- Preguntas técnicas: `2445`.

## Criterios editoriales

- Se separaron valores mínimos, máximos, fórmulas, condiciones, dependencias de cálculo y prohibiciones.
- Se descartó `a020-piso-exterior-antideslizante` porque ya estaba incorporado correctamente en la versión 2.0.0.
- Las pendientes de techo de 12%, 30% y 45% se condicionaron expresamente a la clasificación climática de SENAMHI.
- Se distinguió el parapeto general de A.010 (1.80 m hacia colindantes) del requisito específico de vivienda de A.020 (2.10 m).
- Se evitó presentar impermeabilizantes, espesores de membrana o marcas comerciales como mínimos del RNE.
- Las dimensiones mínimas de canaletas y montantes se acompañaron de la advertencia de que el cálculo hidráulico puede exigir secciones mayores.
- La aplicación automatizada y la validación de la API se ejecutaron correctamente antes de retirar los archivos temporales.
