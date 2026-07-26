# Construcción Segura

Sitio web de asesoría técnica para propietarios y familias que construyen, amplían o corrigen viviendas en el Perú.

## Responsable técnico

**Ing. Omar Oswaldo Alcantara Aquino · CIP N.° 364395**

## Arquitectura

- La web institucional estática vive en la raíz del repositorio.
- `frontend/app/` contiene Mi Casa Segura, el cliente dinámico que consume la API.
- `backend/` contiene FastAPI y las bases técnicas desplegadas en Render.
- `public/` se genera automáticamente y es el único contenido que GitHub Pages publica.

## Desarrollo local

```bash
python scripts/prepare_frontend.py
python -m http.server 8000 --directory public
```

Luego abre `http://localhost:8000`.

## Verificaciones

```bash
python scripts/prepare_frontend.py
python scripts/run_frontend_validator.py check_site
```

## Flujo de cambios

1. Crear una rama desde `main`.
2. Realizar cambios de contenido o código.
3. Ejecutar las verificaciones.
4. Abrir un pull request.
5. Fusionar solo después de revisar el resultado.

Las reglas permanentes están en `AGENTS.md`.
