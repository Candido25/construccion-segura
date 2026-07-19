# Clasificación de recursos del repositorio

Este documento define qué archivos pueden permanecer en el repositorio público de Construcción Segura.

## 1. Producción pública

- Páginas HTML, CSS y JavaScript necesarios para el sitio.
- La aplicación ubicada en `/app/`.
- Recursos optimizados y efectivamente utilizados desde `/assets/site-photos/web/`.
- Fotografías de casos publicadas con autorización y sin datos identificables.
- Logotipos oficiales ubicados en `/assets/brand/`.
- Manifest, service worker, sitemap, robots y archivos de verificación.

## 2. Fuentes de marca autorizadas

Las fuentes maestras del logotipo pueden conservarse en `/assets/brand/` siempre que no contengan datos personales ni material de terceros. La identidad pública debe respetar `AGENTS.md`.

## 3. Material privado o de revisión

No debe subirse al repositorio público:

- fotografías o videos brutos de clientes, obras o lugares de trabajo;
- archivos con ubicación GPS, rostros, placas, direcciones o documentos;
- carpetas de recepción como `review_photos/` o `_incoming/`;
- archivos enviados únicamente para revisión temporal.

El material privado debe almacenarse fuera de GitHub público. Antes de publicar una imagen se debe eliminar metadata EXIF y confirmar autorización.

## 4. Archivos temporales y generados

No deben versionarse:

- logs y archivos de depuración;
- exportaciones, respaldos locales y archivos temporales;
- cachés de Python o del sistema operativo;
- credenciales, archivos `.env` o secretos.

Las exclusiones preventivas están registradas en `.gitignore`.

## 5. Regla para recursos nuevos

Todo recurso nuevo debe cumplir simultáneamente:

1. tener una función pública concreta;
2. estar enlazado desde HTML, CSS, JavaScript, manifest o service worker;
3. superar la validación de formato y dimensiones;
4. no contener datos personales innecesarios;
5. ser revisado en una rama y pull request antes de llegar a `main`.
