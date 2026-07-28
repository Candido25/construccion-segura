# Mi Casa Segura para Android

Este directorio contiene la envoltura Android de la PWA oficial mediante Trusted Web Activity.

## Identidad

- Aplicación: Mi Casa Segura: Guía de Obra
- Paquete: `pe.org.construccionsegura.app`
- URL: `https://www.construccionsegura.org.pe/app/`
- Versión: `1.0.0` (`versionCode` 1)
- API mínima: 23
- API objetivo: 36

## Compilación de prueba

Requisitos:

- JDK 17
- Android SDK Platform 36
- Android SDK Build Tools 35.0.0 o compatible
- Gradle 8.13

Desde la raíz del repositorio:

```bash
gradle -p android clean lint assembleDebug bundleRelease
```

Resultados esperados:

```text
android/app/build/outputs/apk/debug/app-debug.apk
android/app/build/outputs/bundle/release/app-release.aab
```

El APK de depuración se firma automáticamente con una clave de depuración y sirve solo para pruebas. El AAB de `bundleRelease` permanecerá sin firma mientras no se configuren las variables privadas de firma.

## Firma de publicación

No agregues claves, contraseñas ni `signing.properties` al repositorio.

La compilación firmada lee estas variables de entorno:

```text
MCS_KEYSTORE_PATH
MCS_KEYSTORE_PASSWORD
MCS_KEY_ALIAS
MCS_KEY_PASSWORD
```

Ejemplo de ejecución local después de definirlas de forma segura:

```bash
gradle -p android clean bundleRelease
```

La clave de carga debe respaldarse en por lo menos dos ubicaciones privadas controladas por el propietario.

## Digital Asset Links

El archivo `assetlinks.template.json` no debe publicarse con el texto de reemplazo. Después de crear la app en Play Console y activar Play App Signing:

1. abre la sección de integridad de la app;
2. copia la huella SHA-256 del certificado de firma de aplicación;
3. reemplaza el marcador de la plantilla;
4. publica el resultado como `/.well-known/assetlinks.json` en el dominio;
5. verifica que responda por HTTPS, sin redirecciones y con tipo JSON.

La huella de Play App Signing es la que debe permitir que la versión instalada desde Google Play abra como TWA verificada. Para pruebas locales también puede añadirse temporalmente la huella de la clave de depuración o de carga, sin retirar la huella de producción.

## Incremento de versiones

Cada AAB nuevo que se suba a Play Console debe aumentar `versionCode`. Ejemplo:

- 1.0.0 → `versionCode = 1`
- 1.0.1 → `versionCode = 2`
- 1.1.0 → `versionCode = 3`

El nombre visible puede cambiar con `versionName`, pero Google Play identifica cada carga por `versionCode`.

## Seguridad

La app solo solicita permiso de Internet. No solicita ubicación, cámara, micrófono, contactos, almacenamiento ni teléfono. El perfil “Mi obra” y las listas continúan bajo el comportamiento definido por la PWA.
