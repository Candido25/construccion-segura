# Cierre de la Fase 1 — MVP funcional
## Mi Casa Segura: Guía de Obra

**Fecha:** 27 de julio de 2026  
**Estado:** completada técnicamente y pendiente de aprobación funcional del propietario  
**Documento rector:** `docs/ARQUITECTURA_MI_CASA_SEGURA.md`  
**Plan de ejecución:** `docs/PLAN_FASE_1_MVP_FUNCIONAL.md`

---

## 1. Objetivo de la fase

Convertir la base estabilizada de la Fase 0 en un producto mínimo útil para pruebas reales con propietarios que construyen, amplían, remodelan o mantienen una vivienda.

La Fase 1 no genera todavía un APK o AAB. Su resultado es la versión web/PWA funcional que servirá como base única para la futura aplicación Android.

---

## 2. Resultado alcanzado

### 2.1 Guía por etapas

La aplicación mantiene doce etapas navegables:

1. Antes de construir.
2. Terreno y movimiento de tierras.
3. Cimentaciones.
4. Columnas y muros.
5. Vigas, escaleras y techos.
6. Instalaciones sanitarias.
7. Instalaciones eléctricas.
8. Impermeabilización y humedad.
9. Acabados.
10. Ampliaciones y remodelaciones.
11. Seguridad durante la obra.
12. Recepción, mantenimiento y vida útil.

Cada etapa dispone de introducción, temas, controles verificables y bloques de información, advertencia y criterio de diseño. La Fase 1 añade además un panel final con:

- señales de alerta específicas;
- acceso a una lista crítica relacionada;
- búsqueda de dudas relacionadas;
- acceso a parámetros técnicos vinculados.

### 2.2 Listas de verificación críticas

Se incorporaron ocho listas guardables:

1. Antes de excavar.
2. Antes de vaciar concreto.
3. Antes de tapar instalaciones.
4. Antes de retirar puntales.
5. Antes de tarrajear o revestir.
6. Antes de energizar.
7. Antes de recibir una etapa.
8. Después de sismo, incendio o inundación.

Cada lista:

- contiene por lo menos cinco controles;
- guarda el avance localmente;
- registra la fecha de la última revisión;
- muestra controles completos y pendientes;
- puede reiniciarse individualmente;
- se encuentra disponible sin conexión después de la primera carga.

### 2.3 Evaluador guiado de problemas

El evaluador cubre diez categorías:

1. Grietas, fisuras o deformaciones.
2. Hundimiento, terreno o ladera.
3. Viga, columna, muro o acero intervenido.
4. Humedad, filtración o salitre.
5. Concreto con vacíos, rajaduras o acero visible.
6. Retorno, atoros u olor de desagüe.
7. Chispas, calentamiento o disparo de protecciones.
8. Olor a gas o combustión deficiente.
9. Desprendimiento o riesgo de caída.
10. Daños después de sismo, incendio o inundación.

El resultado usa reglas explícitas y puede mostrar:

- verde: orientación preventiva;
- amarillo: revisar antes de continuar;
- rojo: detener y solicitar evaluación.

La herramienta mantiene el aviso de que no confirma causas ni sustituye un diagnóstico profesional.

### 2.4 Personalización mediante “Mi obra”

El perfil local ahora recomienda una siguiente acción según la etapa declarada. Puede sugerir:

- una etapa de la guía;
- una lista crítica;
- controles pendientes;
- advertencias por terreno en ladera o relleno;
- advertencias por tres pisos o más sin planos confirmados;
- advertencias por obra nueva o ampliación sin información de suelos confirmada.

La personalización se actualiza al guardar, editar o eliminar el perfil y cuando cambia el avance de las listas.

### 2.5 Buscador y brechas de contenido

La búsqueda conserva:

- contenido destacado local;
- consulta de la base técnica ampliada;
- sinónimos y expresiones cotidianas;
- normalización de tildes;
- funcionamiento local cuando la API no responde.

La Fase 1 añade:

- correcciones simples para errores frecuentes de escritura;
- registro local de búsquedas sin respuesta;
- límite de cien consultas locales recientes para evitar crecimiento indefinido;
- ausencia de envío automático de esas brechas a Construcción Segura.

### 2.6 Ayuda profesional contextual

Los mensajes de WhatsApp pueden incluir:

- origen de la consulta;
- tema consultado;
- etapa relacionada;
- nivel de riesgo;
- servicio sugerido;
- etapa y ubicación referencial guardadas en “Mi obra”, cuando existen.

Los servicios sugeridos pueden ser consulta remota, revisión antes de vaciado, evaluación de grietas, orientación para ampliaciones o inspección técnica prioritaria.

### 2.7 Privacidad y funcionamiento sin conexión

La política de privacidad y el centro de ayuda informan que se guardan localmente:

- el perfil “Mi obra”;
- el avance y fechas de las listas;
- las búsquedas sin resultado.

Estos datos no se envían automáticamente a Construcción Segura.

El service worker utiliza la caché:

```text
mi-casa-segura-pwa-v25
```

La precarga incluye los módulos, estilos, listas, personalización, ayuda, política de privacidad y recursos principales del MVP.

---

## 3. Nuevos módulos principales

- `frontend/app/phase1-bootstrap.js`
- `frontend/app/phase1-mvp.css`
- `frontend/app/critical-checklists.js`
- `frontend/app/work-personalization.js`
- `frontend/app/stage-enhancements.js`
- `frontend/app/search-insights.js`

Módulos actualizados:

- `frontend/app/problem-evaluator.js`
- `frontend/app/professional-help.js`
- `frontend/app/help-center.js`
- `frontend/app/stage-view-controller.js`
- `service-worker.js`
- `politica-privacidad.html`

---

## 4. Controles automáticos

La automatización del repositorio ejecuta:

```bash
node scripts/check_app_architecture.mjs
node scripts/check_app_content.mjs
node scripts/check_phase0_cleanup.mjs
node scripts/check_phase1_mvp.mjs
python scripts/check_normative_frontend.py
```

Estos controles revisan arquitectura, contenido editorial, archivos provisionales, ocho listas críticas, diez categorías de problemas, personalización, vínculos por etapas, brechas de búsqueda, privacidad, ayuda contextual, parámetros técnicos y caché PWA v25.

La disponibilidad de los archivos y la configuración de los controles están verificadas en el repositorio. La aprobación final de la fase requiere además la prueba funcional del propietario en navegador y teléfono.

---

## 5. Prueba funcional para aprobación

### 5.1 Actualización inicial

1. Abrir `https://www.construccionsegura.org.pe/app/`.
2. Actualizar la página.
3. Si la aplicación instalada mantiene una versión anterior, cerrarla por completo y volver a abrirla.

### 5.2 Mi obra y personalización

1. Crear o editar un perfil.
2. Elegir una etapa, por ejemplo “Cimentaciones”.
3. Verificar que aparezca una siguiente acción relacionada.
4. Abrir la lista recomendada.
5. Marcar controles y confirmar que el conteo cambia.
6. Cerrar y abrir la aplicación para comprobar persistencia.
7. Eliminar el perfil y comprobar que la recomendación vuelva a solicitar configuración.

### 5.3 Listas críticas

1. Abrir las ocho listas.
2. Marcar y desmarcar controles.
3. Confirmar que se muestra la fecha de revisión.
4. Reiniciar una lista y comprobar que las demás conservan su avance.

### 5.4 Guía por etapas

1. Abrir cada una de las doce etapas.
2. Revisar que aparezcan temas y controles.
3. En el panel final, probar:
   - Abrir lista crítica.
   - Consultar dudas relacionadas.
   - Ver parámetros técnicos.
4. Confirmar que “Volver a las etapas” restaura la pantalla normal.

### 5.5 Evaluador de problemas

Probar por lo menos tres escenarios:

- Todas las respuestas “No” en una categoría de base verde.
- Una respuesta amarilla.
- Una señal roja, como corte de acero, olor a gas o deformación.

Confirmar que el resultado y la acción inmediata cambian de manera coherente.

### 5.6 Buscador

Buscar:

- `escalra` para comprobar corrección a “escalera”;
- `zapata`;
- `rajadura`;
- `desagüe`;
- una frase deliberadamente inexistente para comprobar el mensaje sin resultado.

### 5.7 Ayuda profesional

Abrir un resultado amarillo o rojo y pulsar el contacto. El mensaje preparado debe incluir tema, etapa, riesgo y servicio sugerido.

### 5.8 Sin conexión

1. Abrir la aplicación con Internet.
2. Recorrer una etapa y una lista.
3. Cerrar la aplicación.
4. Desactivar temporalmente Internet.
5. Abrir nuevamente la aplicación.
6. Confirmar que inicio, guía, listas, preguntas destacadas y ayuda permanecen disponibles.

La API remota puede no responder sin conexión, pero la interfaz no debe romperse.

---

## 6. Límites conocidos

No forman parte de esta fase:

- APK o AAB;
- proyecto Android;
- publicación en Google Play;
- cuentas de usuario;
- sincronización entre dispositivos;
- varias obras guardadas;
- carga de fotografías o planos;
- diagnóstico automático por imágenes;
- informes descargables;
- pagos, suscripciones o anuncios;
- red de profesionales.

---

## 7. Respaldo

Rama creada antes de iniciar la fase:

```text
respaldo-inicio-fase-1-2026-07-27
```

Rama creada al finalizar el desarrollo técnico:

```text
respaldo-fase-1-mvp-funcional-2026-07-27
```

---

## 8. Criterio para pasar a la Fase 2

La Fase 2 — Android y Google Play — solo podrá comenzar después de que el propietario confirme que:

- las doce etapas son comprensibles;
- las listas guardan y reinician correctamente;
- el evaluador diferencia los tres niveles;
- “Mi obra” personaliza la siguiente acción;
- el buscador y los vínculos funcionan;
- la ayuda profesional muestra mensajes correctos;
- el modo sin conexión conserva las funciones esenciales.

La aprobación funcional no significa que todo el contenido futuro esté terminado. Significa que el MVP web/PWA está aceptado como base para empaquetar Android.
