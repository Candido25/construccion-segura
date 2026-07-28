# Plan de la Fase 2 — Android y Google Play
## Mi Casa Segura: Guía de Obra

**Fecha:** 28 de julio de 2026  
**Fase anterior:** Fase 1 aprobada funcionalmente por el propietario  
**Estado:** en ejecución

---

## 1. Objetivo

Convertir la PWA aprobada en una aplicación Android instalable y preparar su ingreso ordenado a Google Play, sin duplicar la lógica del producto ni comprometer la clave de firma.

La aplicación Android abrirá la PWA oficial mediante una Trusted Web Activity (TWA). La asociación entre el paquete Android y el dominio se verificará mediante Digital Asset Links.

---

## 2. Decisiones fijadas

- Nombre completo: **Mi Casa Segura: Guía de Obra**.
- Nombre corto: **Mi Casa Segura**.
- Marca desarrolladora: **Construcción Segura**.
- Identificador de paquete: `pe.org.construccionsegura.app`.
- URL inicial: `https://www.construccionsegura.org.pe/app/`.
- Distribución inicial: gratuita.
- Primera versión Android: `1.0.0`.
- Código de versión inicial: `1`.
- Tecnología: Trusted Web Activity con Android Browser Helper.
- API objetivo: Android 16, API 36.
- API mínima: Android 6.0, API 23.
- Firma: una clave de carga privada, nunca almacenada en el repositorio público.
- Firma de distribución: Play App Signing.

---

## 3. Alcance de la fase

### Bloque A — Proyecto Android reproducible

- Crear el proyecto bajo `android/`.
- Configurar Gradle, Android Gradle Plugin y Java 17.
- Definir paquete, versión, API mínima y API objetivo.
- Crear manifest, tema, splash e icono adaptativo.
- Abrir únicamente el dominio oficial mediante HTTPS.
- No solicitar permisos sensibles.

### Bloque B — Compilación técnica

- Añadir una automatización para compilar APK de depuración y AAB de revisión sin firma de publicación.
- Ejecutar lint y validaciones de estructura.
- Guardar artefactos de compilación en GitHub Actions.
- No confundir el AAB sin firma con el archivo final para Play Console.

### Bloque C — Firma y asociación con el dominio

- Generar una clave de carga en un entorno controlado por el propietario.
- Guardar la clave, alias y contraseñas fuera del repositorio.
- Obtener la huella SHA-256 de la clave de firma de aplicación proporcionada por Google Play.
- Publicar `/.well-known/assetlinks.json` con el paquete y la huella correcta.
- Verificar que la TWA abra sin barra del navegador.

### Bloque D — Play Console

- Crear el registro de la aplicación.
- Activar Play App Signing.
- Subir el AAB firmado a prueba interna.
- Completar ficha, privacidad, contenido, acceso, público objetivo y seguridad de datos.
- Probar en el HONOR 400 Lite y otros dispositivos disponibles.

### Bloque E — Prueba cerrada

- Preparar al menos doce cuentas de Google de testers.
- Mantener su participación continua durante catorce días.
- Registrar incidencias y comentarios.
- Corregir y subir nuevas versiones cuando corresponda.
- Solicitar acceso a producción después de cumplir el requisito.

---

## 4. Fuera del alcance

No se desarrollará en esta fase:

- una segunda aplicación nativa distinta de la PWA;
- cuentas de usuario;
- pagos, suscripciones o anuncios;
- carga de fotografías o planos;
- diagnóstico automático por imágenes;
- publicación directa sin pruebas;
- almacenamiento de la clave de firma dentro del repositorio;
- recolección de permisos o datos que la aplicación no necesita.

---

## 5. Puertas de control

### Puerta 1 — Proyecto compila

Debe existir un APK de depuración generado automáticamente y un informe sin errores bloqueantes.

### Puerta 2 — Firma bajo control

La clave de carga debe existir, estar respaldada y no aparecer en GitHub.

### Puerta 3 — Dominio verificado

La huella de Play App Signing debe estar publicada en Digital Asset Links y la aplicación debe abrir en modo TWA verificado.

### Puerta 4 — Prueba interna

El AAB firmado debe ser aceptado por Play Console e instalarse desde el canal interno.

### Puerta 5 — Prueba cerrada

Doce testers deben permanecer inscritos durante catorce días continuos y aportar evidencia de uso y comentarios.

### Puerta 6 — Producción

Se solicitará acceso a producción solo después de corregir fallos, completar declaraciones y revisar la ficha pública.

---

## 6. Acciones que requieren intervención del propietario

El desarrollo puede avanzar automáticamente hasta la generación del proyecto y la compilación de depuración. Se solicitará intervención del propietario únicamente para:

1. terminar la verificación de la cuenta de Play Console;
2. crear el registro de la aplicación;
3. generar y custodiar la clave de carga;
4. configurar secretos privados cuando proceda;
5. obtener la huella de Play App Signing;
6. introducir información o declaraciones en Play Console;
7. facilitar las cuentas de los testers;
8. aprobar cada subida y publicación.

---

## 7. Criterio de cierre

La Fase 2 se considerará terminada cuando:

- el proyecto Android esté versionado;
- exista APK de prueba funcional;
- exista AAB firmado aceptado por Play Console;
- Digital Asset Links esté verificado;
- la app se instale desde prueba interna;
- la ficha y declaraciones estén completas;
- la prueba cerrada de doce testers por catorce días haya terminado;
- se haya solicitado o conseguido acceso a producción.

No se publicará en producción sin una aprobación final expresa del propietario.
