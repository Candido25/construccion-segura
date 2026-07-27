# Validación editorial de normativa - 26 de julio de 2026

## Alcance

Se revisaron los 20 registros iniciales de `backend/normativa_tecnica.json`
contra las publicaciones oficiales de las normas A.010, A.020, E.050 y
E.060 del Reglamento Nacional de Edificaciones.

La revisión distingue entre:

- requisitos o fórmulas expresos que pueden marcarse como
  `validado_con_numeral`;
- criterios de aplicación que conservan el estado `piloto_verificado`
  cuando la norma no contiene una regla específica con el mismo nombre.

## Fuentes oficiales revisadas

- A.010 Condiciones Generales de Diseño: RM N.° 191-2021-VIVIENDA.
- A.020 Vivienda: RM N.° 188-2021-VIVIENDA.
- E.050 Suelos y Cimentaciones: RM N.° 406-2018-VIVIENDA.
- E.060 Concreto Armado: DS N.° 010-2009-VIVIENDA.

## Resultado

| Grupo | Numerales confirmados | Registros |
| --- | --- | ---: |
| ITS y cimentaciones E.050 | 5.36; 6.3.1-6.3.4; 22.1-22.2; Art. 23, Fig. 4; 26.2; 27-29 | 6 |
| Geometría de escaleras A.010 | 23.2.a; 23.2.b.i; 23.2.c | 4 |
| Escaleras de vivienda A.020 | 15.1.a; 15.2.b | 4 |
| Barandas A.010 | 35.a; 35.b | 3 |
| Deflexiones E.060 | 9.6.2.1 y Tabla 9.1 | 2 |
| Garganta de escalera | 9.6.1, 9.6.2.1 y Tabla 9.1 como contexto de diseño | 1 piloto |

En total quedaron 19 registros como `validado_con_numeral` y un registro
como `piloto_verificado`. El piloto corresponde al espesor de garganta:
la E.060 regula diseño y control de deflexiones, pero no contiene una regla
específica titulada “espesor mínimo de garganta de escalera”.

## Correcciones editoriales relevantes

- Se precisaron todas las condiciones simultáneas para usar el ITS.
- Se evitó presentar ancho o peralte de un cimiento corrido como medida universal.
- La baranda de 1.00 m en descansos quedó condicionada a la existencia de una
  abertura situada a más de 1.00 m sobre el suelo adyacente.
- Las relaciones L/20 y L/24 se identificaron como referencias para control de
  deflexiones y no como sustitutos del diseño completo.

## Regla para ampliaciones futuras

Ningún registro nuevo puede usar `validado_con_numeral` sin indicar una
cláusula comprobada y una URL oficial. Cuando el dato sea una interpretación
técnica o una aplicación por analogía, debe conservarse como piloto hasta
completar su revisión editorial.
