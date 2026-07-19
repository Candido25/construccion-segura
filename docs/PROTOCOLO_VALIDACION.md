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

La comparación admite únicamente diferencias técnicas mínimas:

- proporción máxima de píxeles modificados: `0.001`;
- error absoluto medio máximo: `0.20`.

Cuando se supera un umbral, se genera una imagen de diferencias y la tarea falla.

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
