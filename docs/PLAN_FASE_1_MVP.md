# Fase 1 — MVP de Mi Casa Segura

## Objetivo

Completar una versión funcional, coherente y suficientemente útil para prueba interna antes de generar el paquete Android.

## Estado general

**En ejecución.** La base funcional principal ya existe; quedan pruebas, ajustes de contenido, experiencia y preparación Android.

## Componentes implementados

1. Inicio organizado por tres necesidades del propietario.
2. Navegación principal: Inicio, Guía, Consultar, Mi obra y Ayuda.
3. Perfil local “Mi obra”, sin registro obligatorio.
4. Guía estructurada en doce etapas.
5. Buscador híbrido con preguntas destacadas y API ampliada.
6. Consulta de parámetros técnicos y normativos.
7. Plantilla común de respuestas.
8. Riesgo explícito verde, amarillo o rojo en preguntas revisadas.
9. Evaluador guiado de problemas de obra.
10. Listas de verificación y progreso local.
11. Acceso contextual a orientación profesional.
12. Política de privacidad adaptada a la aplicación.
13. Service worker y recursos esenciales para funcionamiento degradado sin conexión.
14. Validaciones automáticas de arquitectura, sintaxis y contrato normativo.

## Trabajo pendiente del MVP

### 1. Pruebas de regresión

- verificar las tres rutas principales;
- probar creación, edición, persistencia y eliminación de “Mi obra”;
- abrir las doce etapas y marcar controles;
- buscar preguntas con tildes, sin tildes y sinónimos;
- probar API disponible, lenta y no disponible;
- comprobar semáforos y enlaces de orientación;
- probar el evaluador de problemas en verde, amarillo y rojo;
- comprobar instalación y uso sin conexión;
- revisar pantallas pequeñas y accesibilidad por teclado.

### 2. Contenido mínimo de lanzamiento

- revisar las preguntas destacadas iniciales;
- seleccionar preguntas esenciales por cada etapa;
- asegurar cobertura de escaleras, cimentaciones, concreto, albañilería, sanitarias, eléctricas, humedad, ampliaciones y seguridad;
- asignar riesgo y metadatos a los registros de mayor consulta de la base ampliada;
- evitar respuestas duplicadas, extranjeras o demasiado técnicas.

### 3. Experiencia y ayuda

- convertir la sección Ayuda en un centro de alcance, privacidad, fuentes y contacto;
- incorporar preguntas relacionadas al final de cada respuesta;
- mostrar el contexto de “Mi obra” en las recomendaciones pertinentes;
- revisar que los llamados profesionales sean útiles y no invasivos;
- preparar mensaje contextual para WhatsApp.

### 4. Preparación para Google Play

- confirmar identidad de desarrollador y teléfono en Play Console;
- definir definitivamente el identificador `pe.org.construccionsegura.app`;
- crear y custodiar la clave de firma;
- generar proyecto Android mediante Trusted Web Activity;
- publicar Digital Asset Links en el dominio;
- producir APK de prueba y Android App Bundle;
- probar instalación en un dispositivo Android real;
- crear ficha, descripción, capturas, ícono y gráfico promocional;
- subir la primera compilación a prueba interna.

## Criterios de salida de la Fase 1

La Fase 1 se considera terminada cuando:

1. las pruebas automáticas y manuales críticas no presentan errores bloqueantes;
2. las doce etapas pueden abrirse y guardar progreso;
3. buscador, parámetros y evaluador funcionan con conexión y muestran respaldo útil sin ella;
4. la política de privacidad coincide con el comportamiento real;
5. existe una compilación Android firmada e instalable;
6. la aplicación fue subida a la pista de prueba interna de Google Play;
7. se conserva una versión de reversión del código y de la firma.

## Orden de ejecución

1. integrar y validar las doce etapas;
2. consolidar Ayuda y preguntas relacionadas;
3. ejecutar pruebas de regresión y corregir fallos;
4. congelar el MVP web;
5. generar el proyecto Android;
6. firmar y probar;
7. subir a prueba interna.
