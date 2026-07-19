# Protocolo de validación antes de fusionar

Este protocolo complementa las reglas de `AGENTS.md`. Ningún cambio de estructura, recursos o presentación debe llegar a `main` sin superar las pruebas correspondientes.

## 1. Controles de repositorio

La tarea `Repository safety checks` debe comprobar:

- decodificación completa de todas las imágenes raster;
- formato interno y dimensiones declaradas;
- ausencia de ubicación GPS EXIF;
- ausencia de carpetas privadas o temporales;
- rutas `href`, `src`, `srcset` y `poster`;
- referencias `url()` e `@import` de CSS;
- rutas de recursos creadas desde JavaScript;
- sintaxis de CSS;
- contenido y recursos de `site.webmanifest`;
- existencia y ausencia de duplicados en `APP_SHELL`;
- sintaxis de todos los archivos JavaScript;
- enlaces HTML, identificadores e identidad pública.

El informe completo se conserva como artefacto durante siete días.

## 2. Regresión visual

La tarea `Visual regression` compara la propuesta con `backup/estable`.

### Vistas obligatorias

| Vista | Resolución |
|---|---:|
| Portada de escritorio | 1440 × 900 |
| Portada de tableta | 768 × 1024 |
| Portada móvil | 390 × 844 |
| Aplicación de escritorio | 1440 × 900 |
| Aplicación móvil | 390 × 844 |

Para cada vista se generan:

- captura de la primera pantalla;
- captura de página completa;
- registro de consola y errores de página;
- comprobación de solicitudes locales;
- comprobación de imágenes rotas;
- comprobación de desbordamiento horizontal;
- comprobación de elementos `.reveal` que permanezcan invisibles.

Las fuentes y herramientas externas se sustituyen por respuestas vacías durante la prueba para que la comparación sea determinista.

## 3. Criterio de comparación

Las capturas deben conservar exactamente las mismas dimensiones. Además, las tres condiciones siguientes deben cumplirse simultáneamente:

- proporción máxima de píxeles modificados: `0.012`;
- error absoluto medio máximo: `0.35`;
- diferencia máxima permitida en cualquier canal RGB: `24` niveles.

Los dos primeros límites admiten únicamente pequeñas diferencias subpíxel producidas por mecanismos equivalentes de interpolación gráfica, por ejemplo al migrar una fotografía desde un fondo CSS hacia un elemento `<img>` real. El tercer límite impide que esa tolerancia pueda ocultar cambios relevantes: un desplazamiento, recorte, texto modificado, contraste distinto o alteración de color produce diferencias locales mucho mayores y hace fallar la tarea.

Cuando se supera cualquiera de los tres umbrales, o cuando cambian las dimensiones, se genera una imagen de diferencias y la tarea falla.

## 4. Cambios visuales deliberados

Un rediseño intencional, como el futuro reemplazo de la portada, debe seguir este orden:

1. mantener `backup/estable` como referencia de restauración;
2. ejecutar los controles de funcionamiento aunque la comparación visual falle de forma esperada;
3. adjuntar las capturas actuales y las imágenes de diferencia;
4. obtener aprobación expresa del responsable;
5. fusionar el cambio;
6. verificar producción;
7. actualizar `backup/estable` únicamente después de confirmar que la nueva versión es superior y estable.

La referencia visual nunca debe actualizarse para ocultar una regresión.
