# Declaraciones preliminares para Play Console
## Mi Casa Segura: Guía de Obra — MVP 1.0

**Estado:** borrador de trabajo. Debe contrastarse con el comportamiento de la compilación final y con las preguntas exactas que muestre Play Console antes de enviarlo.

---

## 1. Acceso a la aplicación

- Las funciones educativas principales son accesibles sin crear una cuenta.
- No existe inicio de sesión, contraseña, membresía ni contenido restringido.
- No se requieren credenciales de prueba para la revisión de Google.
- “Mi obra”, las listas y el progreso se guardan localmente en el dispositivo.

**Respuesta prevista:** todas las funciones están disponibles sin acceso especial.

---

## 2. Anuncios y monetización

- La versión 1.0 no muestra anuncios.
- No cobra por descargar la aplicación.
- No contiene compras integradas ni suscripciones.
- El enlace voluntario a orientación profesional no constituye una compra dentro de Google Play.

**Respuesta prevista sobre anuncios:** No.

---

## 3. Público objetivo

- La aplicación está diseñada para propietarios y responsables adultos de una vivienda.
- No está dirigida específicamente a niños.
- No utiliza personajes, juegos, recompensas ni contenidos diseñados para atraer a menores.
- El contenido trata sobre construcción, ampliación, remodelación y mantenimiento de viviendas.

**Selección preliminar:** público adulto, con exclusión de grupos infantiles. La selección exacta se realizará dentro del formulario disponible en Play Console.

---

## 4. Categoría y tipo de contenido

Categoría sugerida para la ficha:

- **Casa y hogar**, si aparece disponible y describe mejor el uso del propietario.
- Alternativa: **Educación**, si la clasificación de Casa y hogar no se adapta al formulario vigente.

La aplicación no debe declararse como:

- aplicación gubernamental;
- noticia o revista;
- aplicación médica o de telemedicina;
- producto financiero;
- aplicación electoral;
- aplicación para niños;
- servicio de emergencia.

---

## 5. Permisos Android

La primera versión solicita únicamente:

```text
android.permission.INTERNET
```

No solicita:

- ubicación;
- cámara;
- micrófono;
- contactos;
- archivos o fotografías;
- teléfono o SMS;
- calendario;
- actividad física;
- Bluetooth;
- notificaciones.

Las declaraciones deben actualizarse antes de publicar una versión que incorpore un permiso nuevo.

---

## 6. Seguridad de datos — inventario preliminar

### Información guardada únicamente en el dispositivo

- perfil “Mi obra”;
- terreno, pisos, etapa y documentos declarados;
- avance y fechas de listas de verificación;
- búsquedas sin resultado registradas localmente;
- preferencias y caché necesarias para funcionamiento sin conexión.

Estos datos no se envían automáticamente a Construcción Segura.

### Información que puede transmitirse

- palabras o frases escritas en el buscador, cuando se consulta la API remota;
- datos que el usuario decide incluir al abrir WhatsApp, enviar un correo o usar un formulario;
- información técnica del dispositivo, seguridad, descarga, rendimiento o fallos tratada por Google Play o por el navegador conforme a sus servicios;
- analítica del sitio únicamente cuando esté activa y exista el consentimiento correspondiente.

### Finalidades previstas

- funcionamiento de la aplicación y búsqueda de respuestas;
- atención de consultas iniciadas voluntariamente;
- seguridad, diagnóstico de fallos y mejora del servicio cuando corresponda;
- cumplimiento de obligaciones legales o contractuales en servicios solicitados.

### Transmisión y protección

- La aplicación usa HTTPS para el dominio y la API.
- No se vende información personal.
- La aplicación no incorpora publicidad comportamental.
- Las búsquedas locales sin resultado no se transmiten automáticamente.

### Eliminación

- El perfil “Mi obra” puede eliminarse desde la aplicación.
- Cada lista puede reiniciarse y el almacenamiento completo puede borrarse desde el dispositivo.
- Para datos enviados voluntariamente por canales de contacto, el usuario puede solicitar acceso, rectificación o eliminación mediante el correo de privacidad publicado.

**Advertencia:** la sección “Seguridad de los datos” debe completarse revisando cada pregunta y cada definición de “recopilado”, “compartido”, “obligatorio” y “opcional”. No debe enviarse únicamente copiando este documento.

---

## 7. Política de privacidad

URL pública:

```text
https://www.construccionsegura.org.pe/politica-privacidad.html
```

La política declara:

- responsable del tratamiento;
- funcionamiento de “Mi obra”;
- datos locales y transmisiones posibles;
- proveedores tecnológicos;
- finalidad;
- conservación;
- derechos del usuario;
- alcance educativo de la aplicación.

Debe permanecer accesible sin iniciar sesión y coincidir con el comportamiento real de la versión enviada.

---

## 8. Contenido y seguridad física

- El evaluador es orientativo y no confirma diagnósticos.
- Las respuestas indican cuándo detener una actividad y solicitar evaluación.
- No se presentan cálculos estructurales universales como sustituto de planos.
- No se instruye al usuario a manipular instalaciones energizadas, fugas de gas o estructuras inestables.
- En situaciones rojas se prioriza proteger el área y contactar a una persona competente o al servicio correspondiente.

---

## 9. Cuestionario de clasificación de contenido

Criterios preliminares:

- no contiene violencia gráfica;
- no contiene contenido sexual;
- no contiene lenguaje ofensivo;
- no contiene apuestas;
- no contiene drogas, alcohol o tabaco como temática;
- no permite interacción pública entre usuarios;
- no comparte ubicación en tiempo real;
- no ofrece compras digitales.

La clasificación definitiva será la que resulte del cuestionario oficial; no debe seleccionarse una edad manualmente para intentar obtener una calificación determinada.

---

## 10. Verificación antes de enviar

Antes de confirmar las declaraciones:

1. instalar exactamente el AAB que se enviará;
2. revisar permisos efectivos en el manifiesto fusionado;
3. probar enlaces externos, buscador, WhatsApp y modo sin conexión;
4. confirmar si existe analítica en la versión Android;
5. comparar la política de privacidad con el comportamiento real;
6. revisar todas las preguntas que muestre Play Console;
7. guardar capturas o un registro de las respuestas enviadas;
8. actualizar este documento cuando cambie una función.
