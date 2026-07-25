# Construcción Segura

Sitio web de asesoría técnica para propietarios y familias que construyen, amplían o corrigen viviendas en el Perú.

## Cobertura

- Consultas remotas en todo el Perú.
- Visitas técnicas presenciales en Lima, previa coordinación.

## Responsable técnico

**Omar Oswaldo Alcantara Aquino**  
Ingeniero civil — CIP N.° 364395  
Técnico en Edificaciones — SENCICO

## Desarrollo local

El sitio es estático. Puede revisarse con cualquier servidor HTTP local, por ejemplo:

```bash
python -m http.server 8000
```

Luego abre `http://localhost:8000`.

## Verificaciones

Ejecuta:

```bash
python scripts/check_site.py
```

El script revisa enlaces y recursos locales faltantes, referencias que salen del repositorio e identificadores duplicados.

## Flujo de cambios

1. Crear una rama desde `main`.
2. Realizar cambios de contenido o código.
3. Ejecutar las verificaciones.
4. Abrir un pull request.
5. Fusionar solo después de revisar el resultado.

Las reglas de identidad, alcance, SEO y seguridad técnica están en `AGENTS.md`.
