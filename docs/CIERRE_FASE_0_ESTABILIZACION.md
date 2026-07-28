# Cierre de la Fase 0 — Estabilización
## Mi Casa Segura: Guía de Obra

**Fecha:** 27 de julio de 2026  
**Estado:** completada técnicamente y pendiente de aprobación funcional del propietario  
**Documento rector:** `docs/ARQUITECTURA_MI_CASA_SEGURA.md`

---

## 1. Objetivo de la fase

Dejar una base ordenada, modular y verificable antes de ampliar funciones o preparar el paquete Android.

La fase no tuvo como objetivo agregar grandes cantidades de contenido, sino reducir improvisación, duplicaciones y riesgos de regresión.

---

## 2. Resultado alcanzado

### Navegación

La aplicación conserva cinco accesos principales:

1. Inicio.
2. Guía.
3. Consultar.
4. Mi obra.
5. Ayuda.

La portada mantiene las tres rutas de necesidad:

- Voy a construir o ampliar.
- Tengo una duda.
- Tengo un problema.

### Perfil local “Mi obra”

- Guarda los datos en `localStorage` mediante una clave versionada.
- Permite crear, editar y eliminar el perfil.
- No exige registro ni contraseña.
- No envía los datos del perfil a Construcción Segura.
- Muestra advertencias iniciales según terreno, pisos y documentación declarada.

### Respuestas y buscador

- Las preguntas destacadas usan el esquema editorial unificado `faq-data-v2.js`.
- Cada registro contiene etapa, sistema, clasificación, riesgo, fecha y estado editorial.
- El buscador estable es `faq-search-v3.js`.
- Las respuestas incorporan controles, prohibiciones, condiciones, fuente, ayuda profesional y preguntas relacionadas.
- La base ampliada de la API se conserva como complemento del contenido destacado.

### Riesgo

- El nivel verde, amarillo o rojo se obtiene del contenido revisado.
- El evaluador visual no clasifica una respuesta únicamente por coincidencias de palabras.
- El evaluador guiado de problemas usa preguntas y reglas explícitas.
- Los llamados a orientación profesional dependen del nivel de riesgo mostrado.

### Guía por etapas

La estructura contempla doce etapas:

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

### Funcionamiento sin conexión

- Existe un único service worker público en la raíz.
- El `APP_SHELL` utiliza la caché `mi-casa-segura-pwa-v24`.
- Los módulos estables, estilos, política de privacidad y recursos principales se incluyen en la precarga.
- Se eliminaron del flujo público los cargadores y copias provisionales.

---

## 3. Limpieza realizada

Se retiraron los archivos que habían sido reemplazados por módulos estables:

- `frontend/app/app-experience.js`
- `frontend/app/faq-data.js`
- `frontend/app/faq-risk-data.js`
- `frontend/app/faq-search.js`
- `frontend/app/faq-search-bootstrap.js`
- `frontend/app/problem-data.js`
- `frontend/app/risk-data.css`

La recuperación de estos archivos sigue disponible en las ramas de respaldo si fuera necesaria.

---

## 4. Validaciones automáticas

La aplicación dispone de cuatro controles independientes:

```bash
node scripts/check_app_architecture.mjs
node scripts/check_app_content.mjs
node scripts/check_phase0_cleanup.mjs
python scripts/check_normative_frontend.py
```

Estos controles verifican, entre otros puntos:

- módulos y estilos obligatorios;
- orden de carga;
- navegación principal;
- doce etapas;
- IDs únicos;
- estructura editorial completa;
- riesgo válido;
- ausencia de clasificación por palabras clave;
- perfil local versionado;
- evaluador guiado;
- ayuda y contacto contextual;
- política de privacidad;
- recursos disponibles sin conexión;
- ausencia de archivos provisionales y recursos duplicados.

El flujo `.github/workflows/phase0-validation.yml` ejecutará estas validaciones en cada envío a `main` y en cada solicitud de cambio.

---

## 5. Prueba funcional para aprobación

La aprobación del propietario debe revisar en un teléfono y, de ser posible, también en una computadora:

### Inicio y navegación

- Los cinco accesos inferiores responden.
- Las tres rutas principales llevan al módulo correcto.
- Al volver desde una etapa no se pierde el contexto.

### Mi obra

- Se puede guardar un perfil.
- El perfil permanece después de cerrar y abrir la aplicación.
- Se puede editar.
- Se puede eliminar.
- La aplicación no solicita crear una cuenta.

### Consultar

- Buscar “zapata”, “rajadura”, “salitre”, “cable” y “desagüe”.
- Abrir una respuesta destacada.
- Verificar nivel de riesgo, controles y preguntas relacionadas.
- Comprobar que el contacto profesional aparece de forma coherente.

### Tengo un problema

- Abrir el evaluador.
- Seleccionar una categoría.
- Responder sus preguntas.
- Confirmar que el resultado diferencia verde, amarillo y rojo.

### Sin conexión

- Abrir la aplicación una vez con Internet.
- Cerrar la aplicación.
- Desactivar temporalmente Internet.
- Volver a abrir la aplicación y comprobar que inicio, guía y contenido precargado siguen disponibles.
- La consulta de la API puede mostrar una limitación de conexión, pero no debe romper la interfaz.

---

## 6. Límites conocidos

No forman parte de la Fase 0:

- completar todo el contenido de las doce etapas;
- almacenar varias obras;
- cuentas de usuario;
- carga de fotografías o planos;
- diagnóstico automático por imágenes;
- informes descargables;
- generación del AAB de Android;
- publicación en Google Play.

Estos elementos se evaluarán en fases posteriores según la arquitectura aprobada.

---

## 7. Respaldo y reversión

Rama de respaldo creada antes del cierre:

```text
respaldo-fase-0-estabilizada-2026-07-27
```

También se conservan respaldos anteriores de navegación, PWA y buscador.

---

## 8. Criterio para pasar a la Fase 1

La Fase 1 podrá comenzar únicamente después de que el propietario confirme que:

- la navegación es comprensible;
- Mi obra funciona correctamente;
- las respuestas se presentan de forma ordenada;
- el semáforo es entendible;
- el aplicativo abre y conserva sus funciones esenciales.

La aprobación funcional no significa que todo el producto esté terminado. Significa que la base sobre la que se construirá la siguiente fase es aceptada.
