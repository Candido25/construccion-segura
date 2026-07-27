# Arquitectura funcional y técnica
## Mi Casa Segura: Guía de Obra

**Marca responsable:** Construcción Segura  
**Producto:** aplicación educativa y preventiva para propietarios que construyen, amplían, remodelan o mantienen una vivienda en el Perú.  
**Plataformas:** web app/PWA y aplicación Android publicada mediante Google Play.  
**Estado del documento:** arquitectura base aprobable para ordenar el desarrollo.  
**Versión:** 1.0  
**Fecha:** 27 de julio de 2026

---

## 1. Propósito del producto

Mi Casa Segura no será una enciclopedia técnica ni un sustituto del ingeniero. Será un acompañante práctico para el propietario que necesita comprender qué revisar, qué no permitir y cuándo detener una actividad para solicitar ayuda profesional.

### Propuesta de valor

> Antes de construir, consulta. Antes de tapar, verifica. Ante una señal de riesgo, detén y pide ayuda.

### Resultado esperado para el usuario

Al terminar una consulta, el usuario debe saber una de estas cuatro cosas:

1. qué criterio mínimo debe respetarse;
2. qué debe revisar antes de continuar;
3. qué práctica no debe aceptar;
4. cuándo necesita un profesional.

---

## 2. Público objetivo

### Usuario principal

Propietario, familiar o responsable de una vivienda que:

- construirá una casa nueva;
- ampliará uno o más ambientes;
- levantará otro piso;
- realizará una remodelación;
- está supervisando una obra sin formación técnica;
- observa una falla, grieta, humedad, problema eléctrico o sanitario;
- necesita entender lo que le propone el maestro de obra.

### Usuarios secundarios

- dirigentes vecinales;
- maestros de obra y albañiles que deseen verificar buenas prácticas;
- estudiantes y técnicos que busquen una guía introductoria;
- clientes que posteriormente requieran orientación, inspección o revisión profesional.

### Exclusión principal

La aplicación no estará dirigida a sustituir el diseño estructural, el estudio de suelos, los planos, la supervisión profesional, la licencia de edificación ni la evaluación presencial de una patología.

---

## 3. Principios de diseño

1. **Lenguaje cotidiano primero.** El usuario puede escribir “rajadura”, “breaker”, “techo”, “maestro” o “glup glup”.
2. **Respuesta útil, no evasiva.** No se responderá únicamente “depende”; se explicará de qué depende y qué puede revisar el propietario.
3. **Norma peruana como fuente principal.** El Reglamento Nacional de Edificaciones, el Código Nacional de Electricidad y otras fuentes oficiales peruanas prevalecen.
4. **El plano manda.** Cuando una medida depende del diseño, la aplicación debe decirlo claramente.
5. **Seguridad antes que receta.** No se publicarán indicaciones universales que puedan inducir una ejecución peligrosa.
6. **Valor antes que venta.** La orientación profesional aparecerá cuando sea pertinente, no como publicidad invasiva.
7. **Móvil primero.** Toda función debe poder usarse cómodamente desde un teléfono económico y con conexión irregular.
8. **Funcionamiento degradado.** Las funciones esenciales deben conservar un respaldo local cuando la API no responda.
9. **Contenido versionado.** Toda respuesta debe poder auditarse, corregirse y retirarse sin rehacer la aplicación completa.
10. **Accesibilidad.** Botones grandes, contraste suficiente, lenguaje claro y navegación compatible con teclado y lectores de pantalla.

---

## 4. Arquitectura de experiencia del usuario

La pantalla principal se organizará alrededor de tres necesidades, no alrededor de categorías técnicas.

### Ruta A. Voy a construir o ampliar

Objetivo: acompañar al propietario por etapas y evitar que avance sin revisar controles básicos.

Flujo:

1. seleccionar tipo de proyecto;
2. completar perfil básico de la obra;
3. elegir etapa actual;
4. revisar temas y listas de verificación;
5. marcar controles revisados;
6. recibir advertencias personalizadas;
7. acceder a orientación profesional cuando corresponda.

### Ruta B. Tengo una duda

Objetivo: responder preguntas escritas en lenguaje natural.

Flujo:

1. escribir una palabra o pregunta;
2. mostrar sugerencias en tiempo real;
3. elegir una pregunta;
4. mostrar respuesta rápida, controles, prohibiciones, fuente y nivel de riesgo;
5. ofrecer preguntas relacionadas;
6. registrar búsquedas sin resultado de forma anónima.

### Ruta C. Tengo un problema

Objetivo: ayudar a decidir si se puede observar, si debe revisarse antes de continuar o si es necesario detener la actividad.

Flujo:

1. seleccionar el tipo de problema;
2. responder preguntas de descarte;
3. clasificar el caso en verde, amarillo o rojo;
4. indicar acciones inmediatas seguras;
5. impedir que el usuario interprete el resultado como diagnóstico definitivo;
6. ofrecer orientación o evaluación profesional.

---

## 5. Mapa de navegación

### Navegación principal recomendada

1. **Inicio**
2. **Guía**
3. **Consultar**
4. **Mi obra**
5. **Ayuda**

La biblioteca institucional, los casos de obra y la web corporativa deben quedar como contenidos secundarios. No deben ocupar el centro de la navegación de la aplicación.

### Pantallas principales

1. Pantalla de inicio.
2. Perfil inicial de la obra.
3. Guía por etapas.
4. Detalle de una etapa.
5. Lista de verificación.
6. Buscador general.
7. Detalle de una respuesta.
8. Buscador de parámetros técnicos.
9. Evaluador de problemas.
10. Resultado de riesgo.
11. Mi obra y progreso.
12. Solicitud de orientación profesional.
13. Acerca de, alcance, privacidad y fuentes.

---

## 6. Módulos funcionales

### 6.1 Inicio

Debe mostrar:

- las tres rutas principales;
- alerta o recomendación personalizada según el perfil de la obra;
- avance de listas de verificación;
- acceso al diagnóstico inicial;
- acceso discreto a ayuda profesional.

### 6.2 Perfil “Mi obra”

Datos mínimos:

- nombre opcional de la obra;
- distrito y departamento;
- obra nueva, ampliación, remodelación o mantenimiento;
- terreno plano, ladera, relleno o desconocido;
- pisos actuales;
- pisos proyectados;
- etapa actual;
- estudio de suelos: sí/no/no sabe;
- planos estructurales: sí/no/no sabe;
- licencia o trámite municipal: sí/no/no sabe.

Regla de privacidad: en la primera versión estos datos se almacenarán localmente en el dispositivo y no requerirán una cuenta de usuario.

### 6.3 Guía por etapas

Estructura recomendada:

1. antes de construir;
2. terreno y movimiento de tierras;
3. cimentaciones;
4. columnas y muros;
5. vigas, escaleras y techos;
6. instalaciones sanitarias;
7. instalaciones eléctricas;
8. impermeabilización y humedad;
9. acabados;
10. ampliaciones y remodelaciones;
11. seguridad durante la obra;
12. recepción, mantenimiento y vida útil.

Cada etapa contendrá:

- explicación breve;
- temas principales;
- lista de verificación;
- señales de alerta;
- preguntas relacionadas;
- acceso a parámetros normativos vinculados.

### 6.4 Buscador de preguntas

El buscador debe combinar:

- preguntas destacadas revisadas editorialmente;
- base técnica ampliada mediante API;
- sinónimos y regionalismos;
- tolerancia a tildes y errores simples;
- resultados relacionados por etapa, sistema y riesgo;
- respaldo local si la API no está disponible.

No debe responder generando texto técnico libre en la primera versión. Las respuestas publicadas deben haber sido previamente revisadas.

### 6.5 Parámetros técnicos

Objetivo: responder consultas como “ancho de escalera”, “garganta”, “cimiento corrido”, “calicata” o “baranda”.

Cada parámetro debe indicar:

- nombre;
- valor o regla;
- unidad;
- clasificación;
- condiciones de aplicación;
- excepciones;
- fuente y numeral;
- advertencia cuando depende del cálculo;
- fecha y estado de revisión.

Clasificaciones oficiales de contenido:

- Mínimo RNE;
- Máximo RNE;
- Fórmula normativa;
- Condición normativa;
- Prohibición;
- Recomendación práctica;
- El plano manda;
- Criterio técnico revisado.

### 6.6 Evaluador de problemas

Categorías iniciales:

- grietas, fisuras y deformaciones;
- hundimientos y movimientos de tierra;
- columnas, vigas o muros intervenidos;
- humedad, filtraciones y salitre;
- concreto defectuoso;
- desagüe lento, retorno u olores;
- calentamiento, chispas o disparo de protecciones;
- olor a gas o combustión deficiente;
- desprendimientos y riesgo de caída;
- daños después de sismo, incendio, inundación o excavación vecina.

La clasificación no se basará únicamente en palabras clave. Cada contenido tendrá un nivel de riesgo definido y reglas de escalamiento.

### 6.7 Listas de verificación

Tipos:

- antes de excavar;
- antes de vaciar concreto;
- antes de tapar instalaciones;
- antes de retirar puntales;
- antes de tarrajear;
- antes de energizar;
- antes de recibir una etapa;
- revisión después de un evento.

Funciones:

- marcar controles;
- guardar fecha;
- mostrar pendientes;
- reiniciar etapa;
- conservar avance sin conexión.

### 6.8 Ayuda profesional

Servicios vinculados:

- consulta remota;
- revisión de fotografías y planos;
- inspección técnica;
- revisión antes de un vaciado;
- evaluación de grietas y daños;
- orientación para ampliaciones;
- elaboración o revisión de planos.

Reglas de presentación:

- CTA discreta en contenidos verdes;
- CTA visible en contenidos amarillos;
- CTA prioritaria en contenidos rojos;
- mensaje de WhatsApp contextualizado con la consulta y el nivel de riesgo;
- nunca afirmar que la contratación es obligatoria para acceder a información básica.

---

## 7. Modelo de riesgo

### Verde — Orientación preventiva

Uso: mantenimiento, revisión general o criterio que puede entenderse sin detener la obra.

Mensaje: “Puedes usar esta orientación para revisar y preguntar antes de ejecutar.”

### Amarillo — Revisar antes de continuar

Uso: decisión que debe verificarse en planos, mediciones, condiciones reales o por una persona competente.

Mensaje: “No avances hasta comprobar este punto.”

### Rojo — Detener y solicitar evaluación

Uso: señales que pueden comprometer estabilidad, seguridad eléctrica, sanitaria, gas, incendio, caída o integridad de personas.

Mensaje: “Detén la actividad, protege el área y solicita evaluación.”

### Regla de arquitectura

El nivel de riesgo debe pertenecer al contenido, no inferirse únicamente en el navegador mediante coincidencias de palabras. El sistema de palabras clave puede ayudar a buscar, pero no debe decidir por sí solo el nivel final.

---

## 8. Plantilla editorial de cada respuesta

Cada respuesta publicada tendrá esta estructura:

1. **Pregunta principal**
2. **Respuesta rápida**
3. **Nivel de riesgo**
4. **Qué debes revisar**
5. **No permitas esto**
6. **Mínimo RNE / Recomendación práctica / El plano manda**
7. **Condiciones y excepciones**
8. **Cuándo consultar**
9. **Preguntas relacionadas**
10. **Fuente y fecha de revisión**
11. **Aviso de alcance**

### Campos mínimos del registro

```json
{
  "id": "faq-ejemplo",
  "pregunta": "¿A qué profundidad deben ir las zapatas?",
  "aliases": ["cuánto cavar", "profundidad de cimiento"],
  "categoria": "Suelos y cimentaciones",
  "etapa": "Cimentaciones",
  "sistema": "Estructuras",
  "respuesta_rapida": "No existe una profundidad universal.",
  "que_revisar": [],
  "no_permitir": "",
  "clasificacion_contenido": "el_plano_manda",
  "riesgo": "amarillo",
  "condiciones": [],
  "fuente": {},
  "fecha_revision": "2026-07-27",
  "estado_editorial": "aprobado"
}
```

---

## 9. Taxonomía del conocimiento

Todo contenido debe poder localizarse por estas dimensiones:

### Por intención del usuario

- construir;
- ampliar;
- remodelar;
- reparar;
- mantener;
- contratar;
- presupuestar;
- verificar;
- resolver un problema.

### Por etapa

- preconstrucción;
- excavación;
- cimentación;
- estructura;
- albañilería;
- instalaciones;
- acabados;
- entrega;
- mantenimiento.

### Por sistema

- suelos;
- estructuras;
- arquitectura;
- albañilería;
- sanitarias;
- eléctricas;
- gas;
- impermeabilización;
- seguridad;
- gestión y contratación.

### Por tipo de respuesta

- medida;
- procedimiento;
- prohibición;
- señal de alerta;
- lista de verificación;
- explicación;
- criterio contractual;
- mantenimiento.

### Por nivel de riesgo

- verde;
- amarillo;
- rojo.

---

## 10. Arquitectura técnica

### 10.1 Capa de presentación

Ubicación principal: `frontend/app/`

Responsabilidades:

- interfaz móvil;
- navegación;
- buscadores;
- listas de verificación;
- almacenamiento local;
- modo sin conexión;
- accesibilidad;
- integración con contacto profesional.

Tecnologías actuales:

- HTML, CSS y JavaScript;
- manifest PWA;
- service worker;
- almacenamiento local;
- futura envoltura Android mediante Trusted Web Activity.

### 10.2 Capa de aplicación

Responsabilidades:

- orquestar búsquedas;
- combinar resultados locales y remotos;
- personalizar advertencias según “Mi obra”;
- aplicar reglas de riesgo;
- registrar progreso;
- gestionar fallos de red;
- preparar solicitudes de orientación profesional.

Los módulos de interfaz deben permanecer separados:

- `home-navigation.js`;
- `faq-search.js`;
- `normative-module.js`;
- `work-profile.js`;
- `risk-evaluator.js`;
- `checklists.js`;
- `professional-help.js`.

### 10.3 Capa de API

Tecnología actual: FastAPI desplegada en Render.

Responsabilidades:

- búsqueda ampliada;
- entrega de preguntas y respuestas;
- consulta de parámetros normativos;
- filtros por categoría, elemento y clasificación;
- versionado de contrato;
- estado de servicio;
- futura recepción anónima de búsquedas sin resultado.

Rutas existentes que deben conservar versionado:

- búsqueda general;
- `/api/v1/normativa/elementos`;
- `/api/v1/normativa/parametros`;
- `/api/v1/normativa/parametros/{id}`.

Regla: cualquier cambio incompatible debe publicarse en una nueva versión de API.

### 10.4 Capa de conocimiento

Fuentes actuales:

- preguntas técnicas estructuradas;
- parámetros normativos;
- preguntas destacadas locales;
- criterios técnicos revisados.

Evolución recomendada:

1. mantener JSON versionado mientras el volumen sea manejable;
2. definir esquemas estrictos y validaciones automáticas;
3. migrar a base de datos cuando se necesite edición multiusuario, historial o panel administrativo;
4. conservar exportación completa a archivos para respaldo y auditoría.

### 10.5 Capa Android

Modelo recomendado:

- paquete: `pe.org.construccionsegura.app`;
- distribución inicial mediante Trusted Web Activity;
- firma permanente bajo control del propietario;
- Digital Asset Links para vincular dominio y aplicación;
- Android App Bundle para Google Play;
- canal interno, cerrado y producción;
- misma base funcional que la PWA.

La aplicación Android no debe duplicar la lógica de negocio. Debe consumir la misma interfaz y API, evitando dos productos distintos.

---

## 11. Privacidad y seguridad

### Primera versión

- sin registro obligatorio;
- sin contraseña;
- perfil de obra almacenado localmente;
- sin ubicación GPS obligatoria;
- sin diagnóstico automático por fotografías;
- sin recolección de planos o imágenes salvo acción expresa del usuario;
- contacto por WhatsApp o formulario con consentimiento.

### Analítica permitida

- término buscado;
- existencia o ausencia de resultados;
- módulo visitado;
- nivel de riesgo mostrado;
- tipo de dispositivo de forma agregada.

No registrar en analítica:

- nombres;
- direcciones exactas;
- teléfonos;
- fotografías;
- planos;
- texto enviado a un profesional.

### Documentos obligatorios

- política de privacidad;
- términos y alcance de la orientación;
- información del responsable;
- fuente y revisión de contenidos;
- procedimiento para solicitar corrección o eliminación de datos.

---

## 12. Arquitectura editorial y gobierno del contenido

### Estados editoriales

1. borrador;
2. revisión técnica;
3. revisión normativa;
4. aprobado;
5. publicado;
6. observado;
7. archivado.

### Regla de publicación

Ninguna respuesta pasa a “publicado” si no tiene:

- pregunta clara;
- clasificación;
- nivel de riesgo;
- fuente o justificación;
- fecha de revisión;
- responsable de revisión;
- aviso cuando depende del cálculo o del plano.

### Criterios de rechazo

No publicar:

- medidas copiadas de otros países sin adaptación;
- recetas estructurales universales;
- calibres eléctricos sin condiciones;
- plazos de desencofrado universales;
- instrucciones químicas peligrosas;
- diagnóstico definitivo a partir de una descripción breve;
- afirmaciones comerciales no verificadas.

---

## 13. Control de calidad

### Validaciones automáticas

- IDs únicos;
- campos obligatorios completos;
- fuentes válidas;
- fecha de revisión;
- ausencia de etiquetas HTML peligrosas;
- enlaces activos;
- búsqueda sin duplicados fuertes;
- compatibilidad de esquema;
- límites mínimos de contenido y cobertura.

### Pruebas de producto

- búsqueda con y sin tildes;
- búsqueda por sinónimos;
- pérdida de conexión;
- API lenta o caída;
- navegación en Android;
- lectura en pantallas pequeñas;
- contraste y tamaño táctil;
- persistencia de progreso;
- instalación PWA;
- inicio desde Google Play;
- accesos de WhatsApp y contacto.

### Puertas de calidad antes de publicar una versión

1. no hay errores bloqueantes;
2. todas las rutas principales funcionan;
3. el contenido nuevo fue revisado;
4. el service worker usa una versión nueva;
5. el paquete Android incrementa su código de versión;
6. la política de privacidad coincide con el comportamiento real;
7. existe un procedimiento de reversión.

---

## 14. Roadmap ordenado

### Fase 0 — Arquitectura y estabilización

- aprobar este documento;
- congelar navegación y taxonomía;
- separar módulos JavaScript;
- sustituir el semáforo por palabras clave por riesgo definido en datos;
- revisar navegación inferior;
- definir esquema único de respuesta.

### Fase 1 — MVP para prueba interna

- inicio con tres rutas;
- perfil básico “Mi obra”;
- guía por etapas;
- buscador híbrido;
- parámetros técnicos;
- evaluador de problemas;
- listas básicas;
- CTA profesional contextual;
- política de privacidad;
- funcionamiento sin conexión;
- paquete Android instalable.

### Fase 2 — Prueba cerrada

- prueba con usuarios reales;
- búsquedas sin resultado;
- mejoras de lenguaje;
- corrección de navegación;
- ampliación de respuestas destacadas;
- ajustes de rendimiento y accesibilidad;
- capturas y ficha de Google Play.

### Fase 3 — Producción inicial

- publicación gratuita;
- seguimiento de errores;
- actualización periódica de contenido;
- métricas agregadas;
- soporte básico;
- proceso de revisión mensual.

### Fase 4 — Evolución

- historial de varias obras;
- informes descargables;
- registro fotográfico para consulta profesional, no diagnóstico automático;
- servicios premium opcionales;
- red de profesionales verificados;
- panel editorial interno.

---

## 15. Decisiones que quedan fijadas

1. El nombre es **Mi Casa Segura: Guía de Obra**.
2. La marca responsable es **Construcción Segura**.
3. El usuario principal es el propietario no especializado.
4. La navegación comienza por necesidad del usuario.
5. La norma peruana es la base principal.
6. Las respuestas deben distinguir **Mínimo RNE**, **Recomendación práctica** y **El plano manda**.
7. El riesgo se define en los datos y se revisa técnicamente.
8. La PWA y Android comparten la misma base funcional.
9. La primera versión no exige cuenta ni recolecta datos sensibles.
10. La información básica será gratuita.
11. La monetización futura no condicionará el acceso a seguridad esencial.
12. Las mejoras se ejecutarán por fases y con puertas de calidad.

---

## 16. Regla de cambio

Toda nueva función deberá responder estas preguntas antes de desarrollarse:

1. ¿Qué problema concreto del propietario resuelve?
2. ¿En cuál módulo de esta arquitectura pertenece?
3. ¿Qué datos necesita?
4. ¿Qué riesgo introduce?
5. ¿Qué fuente respalda su contenido?
6. ¿Funciona sin conexión o tiene una alternativa?
7. ¿Cómo se probará?
8. ¿Qué versión modifica?

Si una propuesta no tiene respuesta clara, no debe incorporarse todavía.
