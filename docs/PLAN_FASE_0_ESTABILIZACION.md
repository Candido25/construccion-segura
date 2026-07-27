# Fase 0 — Estabilización de Mi Casa Segura

## Estado

**Desarrollo completado.** La arquitectura quedó aplicada al código y protegida por validaciones automáticas. La ejecución de integración continua debe confirmarse en GitHub Actions después de cada cambio en `main`.

## Objetivo

Alinear la aplicación existente con la arquitectura aprobada antes de ampliar funciones o preparar el paquete Android.

## Bloques completados

1. **Perfil Mi obra y navegación principal** — completado.
2. **Esquema único de respuestas** — completado.
3. **Riesgo definido en los datos** — completado para las preguntas destacadas y respuestas estructuradas.
4. **Separación de navegación, perfil y riesgo** — completado mediante módulos independientes.
5. **Navegación inferior y accesibilidad básica** — completado.
6. **Pruebas de arquitectura y modo sin conexión** — incorporadas al flujo de integración continua.
7. **API compatible con metadatos editoriales** — completado sin retirar los campos históricos.
8. **Rama de reversión** — creada antes de la integración final.

## Resultado técnico

- `home-navigation.js`: navegación y rutas principales.
- `work-profile.js`: perfil local “Mi obra”.
- `faq-search-v3.js`: buscador y plantilla común de respuestas.
- `risk-evaluator.js`: presentación del riesgo definido en los datos.
- `problem-evaluator.js`: evaluación guiada mediante reglas explícitas.
- `stage-expander.js`: doce etapas de la guía de obra.
- `check_app_architecture.mjs`: validación automática de la arquitectura.
- service worker versionado para conservar la aplicación esencial sin conexión.

## Criterios de cierre alcanzados

- ninguna respuesta destacada usa palabras clave del navegador para decidir el nivel final de riesgo;
- las preguntas destacadas contienen riesgo, clasificación, etapa, sistema y fecha de revisión;
- la API admite campos editoriales opcionales sin romper clientes existentes;
- las respuestas utilizan una plantilla visual común;
- la navegación principal coincide con Inicio, Guía, Consultar, Mi obra y Ayuda;
- la guía contiene las doce etapas establecidas por la arquitectura;
- la aplicación conserva respaldo local y caché actualizada;
- existe una rama de reversión previa a los cambios.

## Observación de validación

La validación está configurada en GitHub Actions. En este entorno no fue posible clonar el repositorio para una ejecución local por una falla de resolución DNS externa; por ello no debe darse por aprobada una ejecución concreta hasta revisar el resultado del flujo remoto.
