# Arquitectura de Construcción Segura

## Capas

1. **Web institucional estática:** archivos HTML, CSS, JavaScript y recursos ubicados en la raíz.
2. **Cliente dinámico:** `frontend/app/`, actualmente publicado como `/app/` y preparado para evolucionar hacia una aplicación independiente.
3. **Backend API First:** `backend/`, desplegado en Render y consumido por los clientes mediante HTTPS.
4. **Paquete de publicación:** `public/`, generado por `scripts/prepare_frontend.py` y excluido de Git.

## Flujo de publicación

- GitHub Pages ejecuta `scripts/prepare_frontend.py` y publica exclusivamente `public/`.
- Render despliega únicamente el backend y sus dependencias.
- La raíz completa del repositorio nunca se utiliza como artefacto de GitHub Pages.

## Regla para la futura aplicación

La lógica de interfaz reutilizable debe permanecer dentro de `frontend/app/`. La web institucional puede enlazar al aplicativo, pero no debe absorber su lógica de negocio.
