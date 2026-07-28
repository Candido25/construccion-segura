# Plan de prueba cerrada
## Mi Casa Segura: Guía de Obra

**Estado:** preparación previa a Google Play  
**Objetivo operativo:** probar instalación, comprensión, estabilidad y utilidad antes de solicitar acceso a producción.

---

## 1. Grupo mínimo

Preparar como mínimo doce personas con una cuenta de Google activa. Para reducir el riesgo de quedar por debajo del mínimo por abandono, la meta interna será invitar entre quince y dieciocho personas.

Los testers no deben compartir contraseñas ni códigos. Cada persona se inscribirá con su propia cuenta mediante el enlace oficial de Google Play.

### Perfiles recomendados

- propietarios que estén construyendo o ampliando;
- personas que hayan realizado una autoconstrucción;
- maestros de obra o técnicos;
- estudiantes de construcción o ingeniería;
- familiares sin conocimientos técnicos;
- usuarios con teléfonos Android de distintas marcas y antigüedad.

---

## 2. Registro interno

Mantener una relación privada con estos campos:

| Campo | Propósito |
|---|---|
| Código del tester | Identificarlo sin publicar datos personales |
| Correo de Google | Añadirlo al grupo de prueba |
| Marca y modelo | Revisar compatibilidad |
| Versión de Android | Detectar fallos por sistema |
| Fecha de inscripción | Controlar continuidad |
| Última versión instalada | Confirmar actualización |
| Pruebas completadas | Medir cobertura |
| Incidencias | Dar seguimiento |
| Estado | Invitado, inscrito, activo o retirado |

El archivo no debe publicarse en el repositorio.

---

## 3. Preparación antes del día 1

1. Crear la aplicación en Play Console.
2. Subir un AAB firmado al canal cerrado.
3. Crear la lista o grupo de testers.
4. Obtener el enlace de inscripción.
5. Confirmar que la ficha de prueba muestre nombre, icono y descripción correctos.
6. Enviar instrucciones sencillas.
7. Comprobar que más de doce personas se hayan inscrito antes de iniciar el conteo interno.

---

## 4. Guion para cada tester

### Instalación

- abrir el enlace de inscripción;
- aceptar participar;
- instalar desde Google Play;
- abrir la aplicación desde su icono;
- indicar si aparece una barra de navegador inesperada o una pantalla en blanco.

### Prueba básica

1. Abrir Inicio, Guía, Consultar, Mi obra y Ayuda.
2. Configurar una obra de prueba.
3. Abrir la etapa recomendada.
4. Marcar por lo menos tres controles de una lista.
5. Cerrar y abrir la aplicación para comprobar que se conserve el avance.
6. Buscar “zapata”, “escalera”, “rajadura”, “cable” y “desagüe”.
7. Probar una búsqueda sin resultado.
8. Abrir el evaluador de problemas y completar un caso.
9. Revisar el botón de orientación profesional sin necesidad de enviar el mensaje.
10. Probar la aplicación con conexión y luego sin conexión.

### Prueba de comprensión

El tester responderá:

- ¿Entendiste para qué sirve la aplicación al verla por primera vez?
- ¿Encontraste fácilmente la opción que necesitabas?
- ¿Qué término te resultó confuso?
- ¿El semáforo verde, amarillo y rojo fue claro?
- ¿Qué pregunta buscaste y no encontraste?
- ¿En qué momento pedirías ayuda profesional?

---

## 5. Cronograma de catorce días

### Día 1

- confirmar inscripción e instalación;
- registrar dispositivo y versión;
- completar la prueba básica.

### Días 2 a 4

- probar “Mi obra” y una etapa diferente;
- revisar persistencia del progreso;
- comunicar errores de navegación o pantalla.

### Días 5 a 7

- probar búsquedas y parámetros técnicos;
- registrar preguntas no encontradas;
- revisar textos confusos.

### Días 8 a 10

- probar el evaluador de problemas;
- comparar resultados verde, amarillo y rojo;
- revisar acciones inmediatas.

### Días 11 a 13

- probar actualización de una nueva versión cuando exista;
- repetir pruebas en conexión lenta o sin conexión;
- confirmar que no se perdió información local.

### Día 14

- completar encuesta final;
- confirmar que la aplicación continúa instalada y que el tester sigue inscrito;
- cerrar incidencias bloqueantes o registrar su corrección pendiente.

El conteo válido dependerá de la inscripción continua que muestre Play Console, no únicamente de este cronograma interno.

---

## 6. Clasificación de incidencias

### Bloqueante

Impide instalar, abrir o usar una ruta principal; pérdida generalizada de datos; cierre repetido; pantalla en blanco; riesgo de seguridad.

### Alta

Una función principal falla, el semáforo muestra una orientación incoherente o una respuesta peligrosa puede interpretarse como receta.

### Media

Problema de navegación, texto, visualización, persistencia parcial o resultado de búsqueda deficiente con alternativa disponible.

### Baja

Detalle visual, redacción mejorable o sugerencia que no impide el uso.

No se solicitará producción con una incidencia bloqueante o alta abierta.

---

## 7. Informe de incidencia

Cada reporte debe incluir:

```text
Código del tester:
Fecha y hora aproximada:
Modelo del teléfono:
Versión de Android:
Versión de la aplicación:
Pantalla o función:
Pasos realizados:
Resultado esperado:
Resultado observado:
¿Se repite siempre?:
Captura sin datos personales, cuando sea posible:
```

No enviar contraseñas, códigos, documentos de identidad, datos bancarios ni información privada de una obra real.

---

## 8. Criterios internos para concluir

- al menos doce testers permanecen inscritos durante todo el periodo exigido;
- todos pudieron instalar desde Google Play;
- las cinco rutas principales funcionan;
- no existen cierres repetidos ni pantallas en blanco;
- “Mi obra” y las listas conservan información;
- el buscador ofrece resultados útiles y registra brechas;
- el evaluador diferencia correctamente los niveles;
- el modo sin conexión no rompe la interfaz;
- no hay incidencias bloqueantes o altas abiertas;
- existe evidencia de comentarios y mejoras realizadas.

---

## 9. Mensaje de invitación sugerido

```text
Hola. Estoy realizando la prueba cerrada de Mi Casa Segura: Guía de Obra, una aplicación gratuita de Construcción Segura para propietarios que construyen, amplían o remodelan su vivienda.

Necesito que te inscribas con tu propia cuenta de Google, instales la aplicación desde el enlace oficial y la mantengas instalada y activa durante el periodo de prueba. Te enviaré un guion breve y un formulario para comentarios.

No debes compartir conmigo tu contraseña ni ningún código de Google.
```
