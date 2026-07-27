from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
NORMATIVA = BACKEND / "normativa_tecnica.json"
PREGUNTAS = BACKEND / "preguntas_tecnicas.json"
CHECK = ROOT / "scripts" / "check_normativa.py"
DOC = ROOT / "docs" / "VALIDACION_PUERTAS_VENTANAS_SEGURIDAD_2026-07-27.md"

RNE = "https://www.gob.pe/institucion/vivienda/informes-publicaciones/2309793-reglamento-nacional-de-edificaciones-rne"
SENCICO = "https://www.gob.pe/institucion/sencico/informes-publicaciones/2879048-carpinteria-de-acabados-de-obras-de-edificacion"


def valor_texto(texto: str) -> dict:
    return {
        "tipo": "texto", "valor": None, "minimo": None, "maximo": None,
        "unidad": None, "formula": None, "texto": texto,
    }


def valor_numero(valor: float, unidad: str, texto: str) -> dict:
    return {
        "tipo": "numero", "valor": valor, "minimo": None, "maximo": None,
        "unidad": unidad, "formula": None, "texto": texto,
    }


def norma(
    identificador: str,
    categoria: str,
    elemento: str,
    parametro: str,
    texto: str,
    norma_nombre: str,
    numeral: str,
    dispositivo: str,
    pregunta: str,
    valor: float | None = None,
    unidad: str | None = None,
    clasificacion: str = "condicion_normativa",
) -> dict:
    return {
        "id": identificador,
        "categoria": categoria,
        "elemento": elemento,
        "parametro": parametro,
        "clasificacion": clasificacion,
        "valor": valor_numero(valor, unidad or "", texto) if valor is not None else valor_texto(texto),
        "condiciones": [
            "Aplicar junto con los planos, el cuadro de vanos, las especificaciones del proyecto y las normas de seguridad correspondientes."
        ],
        "fuente": {
            "tipo": "RNE",
            "norma": norma_nombre,
            "denominacion": "Reglamento Nacional de Edificaciones",
            "dispositivo": dispositivo,
            "numeral": numeral,
            "numeral_confirmado": True,
            "url_oficial": RNE,
        },
        "estado_revision": "validado_con_numeral",
        "advertencia": "El ancho, sentido de apertura, resistencia y herrajes pueden requerir condiciones adicionales por accesibilidad, evacuación, incendio o uso específico.",
        "faq_relacionadas": [],
        "fecha_revision": "2026-07-27",
        "faq_categoria": categoria,
        "pregunta": pregunta,
        "respuesta": texto + " Debe verificarse en el vano terminado y en coordinación con el uso real del ambiente.",
    }


def criterio(
    identificador: str,
    categoria: str,
    elemento: str,
    parametro: str,
    texto: str,
    pregunta: str | None = None,
) -> dict:
    pregunta_final = pregunta or f"¿Qué debo revisar sobre {parametro.lower()} en {elemento.lower()}?"
    return {
        "id": identificador,
        "categoria": categoria,
        "elemento": elemento,
        "parametro": parametro,
        "clasificacion": "recomendacion",
        "valor": {
            "tipo": "sin_valor_universal", "valor": None, "minimo": None,
            "maximo": None, "unidad": None, "formula": None, "texto": texto,
        },
        "condiciones": [
            "La solución final depende del material, dimensiones, exposición, fabricante, sistema de anclaje y especificaciones del proyecto."
        ],
        "fuente": {
            "tipo": "manual_oficial",
            "norma": "Formación técnica SENCICO",
            "denominacion": "Carpintería de acabados de obras de edificación",
            "dispositivo": None,
            "numeral": "Aplicación práctica supervisada",
            "numeral_confirmado": False,
            "url_oficial": SENCICO,
        },
        "estado_revision": "criterio_tecnico_revisado",
        "advertencia": "No sustituye el detalle del fabricante, la certificación del producto, las pruebas ni la supervisión profesional.",
        "faq_relacionadas": [],
        "fecha_revision": "2026-07-27",
        "faq_categoria": categoria,
        "pregunta": pregunta_final,
        "respuesta": texto + " No debe aceptarse una instalación que funcione solo después de forzar, golpear o deformar el elemento.",
    }


def reemplazar_unico(texto: str, anterior: str, nuevo: str) -> str:
    if texto.count(anterior) != 1:
        raise SystemExit(f"No se encontró una única coincidencia para: {anterior}")
    return texto.replace(anterior, nuevo, 1)


def construir_registros() -> list[dict]:
    registros: list[dict] = []

    registros.extend([
        norma("a020-vano-puerta-principal-vivienda-ancho-minimo", "Puertas, ventanas y cerrajería", "Puerta principal de vivienda", "Ancho mínimo del vano", "El vano de acceso principal a una unidad de vivienda debe tener como mínimo 0.90 m de ancho.", "A.020", "12.2.b, Cuadro N.° 06", "RM N.° 188-2021-VIVIENDA", "¿Cuál es el ancho mínimo de la puerta principal de una vivienda?", 0.90, "m", "minimo_normativo"),
        norma("a020-vano-puerta-ambientes-principales-ancho-minimo", "Puertas, ventanas y cerrajería", "Puerta de dormitorio, sala, comedor o cocina", "Ancho mínimo del vano", "Los vanos de acceso a ambientes de descanso, reunión y alimentación deben tener como mínimo 0.80 m de ancho.", "A.020", "12.2.b, Cuadro N.° 06", "RM N.° 188-2021-VIVIENDA", "¿Una puerta de dormitorio o cocina puede tener menos de 80 centímetros?", 0.80, "m", "minimo_normativo"),
        norma("a020-vano-puerta-bano-ancho-minimo", "Puertas, ventanas y cerrajería", "Puerta de baño o ambiente de servicio", "Ancho mínimo del vano", "El vano de acceso a baños y ambientes de aseo o servicio debe tener como mínimo 0.70 m de ancho.", "A.020", "12.2.b, Cuadro N.° 06", "RM N.° 188-2021-VIVIENDA", "¿Cuál es el ancho mínimo permitido para la puerta de un baño?", 0.70, "m", "minimo_normativo"),
        norma("a020-vano-puerta-principal-multifamiliar-ancho-minimo", "Puertas, ventanas y cerrajería", "Ingreso principal de vivienda multifamiliar", "Ancho mínimo del vano", "El acceso principal de una vivienda multifamiliar, de uso colectivo o conjunto residencial debe tener como mínimo 1.20 m de ancho.", "A.020", "12.2.b, Cuadro N.° 06", "RM N.° 188-2021-VIVIENDA", "¿Cuánto debe medir como mínimo la puerta principal de un edificio multifamiliar?", 1.20, "m", "minimo_normativo"),
        norma("a020-puerta-varias-hojas-hoja-minima", "Puertas, ventanas y cerrajería", "Puerta residencial de varias hojas", "Ancho mínimo de una hoja", "Cuando el acceso residencial tiene más de una hoja de cierre, una de ellas no debe tener menos de 1.00 m de ancho.", "A.020", "12.3", "RM N.° 188-2021-VIVIENDA", "En una puerta principal de dos hojas, ¿cuánto debe medir por lo menos una de ellas?", 1.00, "m", "minimo_normativo"),
        norma("a020-vano-cierre-clima-material-compatible", "Puertas, ventanas y cerrajería", "Vano de puerta o ventana", "Compatibilidad del cierre", "Los vanos deben tener un cierre adecuado a las condiciones del clima y una carpintería compatible con el material del cerramiento.", "A.020", "12.1", "RM N.° 188-2021-VIVIENDA", "¿Puedo instalar cualquier puerta o ventana sin considerar el clima y el tipo de muro?"),

        norma("a130-salida-emergencia-apertura-simple-empuje", "Evacuación y protección contra incendios", "Salida de emergencia", "Apertura desde el interior", "La puerta de una salida de emergencia debe poder abrirse desde el interior mediante simple empuje.", "A.130", "Artículo 5", "DS N.° 017-2012-VIVIENDA y modificatorias", "¿Una salida de emergencia puede necesitar llave para abrirse desde adentro?"),
        norma("a130-puerta-evacuacion-cerradura-llave-senal", "Evacuación y protección contra incendios", "Puerta de evacuación con cerradura", "Señal de permanencia sin llave", "Cuando una puerta de evacuación tenga cerradura con llave por protección de bienes, debe contar con señal iluminada que indique que permanecerá sin llave durante las horas de trabajo.", "A.130", "Artículo 5", "DS N.° 017-2012-VIVIENDA y modificatorias", "¿Qué condición debe cumplirse si una puerta de evacuación tiene cerradura con llave?"),
        norma("a130-puerta-cortafuego-cierrapuertas-aprobado", "Evacuación y protección contra incendios", "Puerta en cerramiento cortafuego", "Dispositivo de cierre", "Toda puerta que forme parte de un cerramiento contra fuego, incluyendo el ingreso a una escalera de evacuación, debe contar con un cierrapuertas aprobado para ese uso.", "A.130", "Artículo 8.a", "DS N.° 017-2012-VIVIENDA y modificatorias", "¿Una puerta cortafuego puede quedarse sin brazo cierrapuertas?"),
        norma("a130-puerta-doble-hoja-coordinador-cierre", "Evacuación y protección contra incendios", "Puerta de evacuación de doble hoja", "Orden de cierre", "Las puertas de doble hoja con cerrajería de un punto y cierrapuertas independientes deben incorporar un dispositivo que ordene correctamente el cierre de las hojas.", "A.130", "Artículo 8.b", "DS N.° 017-2012-VIVIENDA y modificatorias", "¿Por qué una puerta cortafuego de dos hojas necesita coordinador de cierre?"),
        norma("a130-puerta-evacuacion-manija-certificada", "Evacuación y protección contra incendios", "Puerta de evacuación sin barra antipánico", "Manija de operación", "Las puertas de evacuación que no requieran barra antipánico deben usar cerradura de manija aprobada y certificada para personas con discapacidad.", "A.130", "Artículo 8.c", "DS N.° 017-2012-VIVIENDA y modificatorias", "¿Qué tipo de manija debe tener una puerta de evacuación sin barra antipánico?"),
        norma("a130-puerta-cortafuego-conjunto-certificado", "Evacuación y protección contra incendios", "Puerta cortafuego", "Certificación del conjunto", "La puerta cortafuego debe certificarse como conjunto, incluyendo hoja, marco y cerrajería, para la resistencia al fuego exigida.", "A.130", "Artículo 10", "DS N.° 017-2012-VIVIENDA y modificatorias", "¿Basta con que solo la hoja tenga certificado de resistencia al fuego?"),
        norma("a130-puerta-cortafuego-accesorios-certificados", "Evacuación y protección contra incendios", "Accesorios de puerta cortafuego", "Certificación para uso cortafuego", "Los accesorios instalados en una puerta cortafuego deben estar aprobados y certificados para ese uso.", "A.130", "Artículo 10", "DS N.° 017-2012-VIVIENDA y modificatorias", "¿Puedo colocar cualquier bisagra, cerradura o brazo en una puerta cortafuego?"),
        norma("a130-puerta-cortafuego-autocierre", "Evacuación y protección contra incendios", "Puerta cortafuego", "Cierre automático", "La puerta cortafuego debe poder cerrarse y asegurarse por sí sola en caso de incendio.", "A.130", "Artículo 10", "DS N.° 017-2012-VIVIENDA y modificatorias", "¿Una puerta cortafuego puede permanecer abierta sin un sistema de cierre automático?"),
        norma("a130-puerta-cortahumo-sellos-contorno", "Evacuación y protección contra incendios", "Puerta cortahumo", "Sellos de humo", "La puerta cortahumo debe incorporar dispositivo de cierre y sellos corta humo en el borde superior y en los laterales de la hoja.", "A.130", "Artículo 10", "DS N.° 017-2012-VIVIENDA y modificatorias", "¿Dónde deben colocarse los sellos de una puerta cortahumo?"),
        norma("a130-puerta-cortafuego-resistencia-relativa", "Evacuación y protección contra incendios", "Puerta cortafuego", "Resistencia respecto del cerramiento", "La resistencia al fuego de la puerta debe ser equivalente al 75 % de la resistencia del muro, corredor o escalera a la que sirve.", "A.130", "Artículo 10", "DS N.° 017-2012-VIVIENDA y modificatorias", "¿La puerta cortafuego debe tener la misma resistencia que la pared?", 75, "%", "formula_normativa"),
        norma("a130-puerta-cortafuego-alteracion-certificacion", "Evacuación y protección contra incendios", "Puerta cortafuego certificada", "Conservación de la certificación", "La puerta cortafuego no debe ser perforada, recortada ni modificada de forma que invalide la certificación del conjunto.", "A.130", "Artículo 10", "DS N.° 017-2012-VIVIENDA y modificatorias", "¿Puedo perforar una puerta cortafuego para instalar otro accesorio?", clasificacion="prohibicion"),

        norma("a120-bano-accesible-espacio-giro-puerta", "Servicios higiénicos accesibles", "Puerta de baño accesible", "Espacio de maniobra", "La ubicación y apertura de la puerta deben conservar un espacio de maniobra con diámetro de giro de 1.50 m.", "A.120", "Artículo 13.1.b", "RM N.° 075-2023-VIVIENDA", "¿Qué espacio debe quedar libre junto a la puerta de un baño accesible?", 1.50, "m", "minimo_normativo"),
        norma("a120-bano-accesible-apertura-compatible", "Servicios higiénicos accesibles", "Puerta de baño accesible", "Tipo y sentido de apertura", "La puerta puede abrir hacia el exterior, hacia el interior o ser corrediza, siempre que no elimine el espacio de maniobra accesible.", "A.120", "Artículo 13.1.b", "RM N.° 075-2023-VIVIENDA", "¿La puerta de un baño accesible tiene que abrir obligatoriamente hacia afuera?"),
        norma("a120-marco-bano-no-invadir-ruta", "Servicios higiénicos accesibles", "Marco de puerta accesible", "Invasión de la ruta", "El marco y los elementos de la puerta no deben reducir ni invadir la ruta accesible prevista.", "A.120", "Artículo 13.1.b", "RM N.° 075-2023-VIVIENDA", "¿El marco de una puerta accesible puede sobresalir dentro de la ruta de circulación?"),
    ])

    criterios = [
        ("criterio-vano-verificar-cuadro", "Carpinterías, sellos y herrajes", "Cuadro de vanos", "Verificación documental", "Comparar cada vano con los planos, cuadro de puertas y ventanas, detalles y especificaciones antes de fabricar."),
        ("criterio-vano-medir-acabado-final", "Carpinterías, sellos y herrajes", "Vano terminado", "Medición final", "Medir el ancho y la altura considerando tarrajeo, enchape, contrapiso y piso terminado, no solo la albañilería en bruto."),
        ("criterio-vano-diagonales", "Carpinterías, sellos y herrajes", "Vano", "Escuadra", "Comparar las diagonales para detectar descuadres antes de instalar el marco."),
        ("criterio-vano-aplomo-nivel", "Carpinterías, sellos y herrajes", "Vano y marco", "Aplomo y nivel", "Comprobar aplomo de jambas, nivel del dintel y condición del umbral o alféizar."),
        ("criterio-marco-no-forzar-vano", "Carpinterías, sellos y herrajes", "Marco", "Montaje sin deformación", "No introducir el marco a golpes ni deformarlo para compensar un vano mal ejecutado."),
        ("criterio-marco-anclaje-sustrato", "Carpinterías, sellos y herrajes", "Marco", "Tipo de anclaje", "Seleccionar el anclaje según concreto, albañilería, drywall, madera o estructura metálica y según las cargas de uso."),
        ("criterio-marco-calces-anclajes", "Carpinterías, sellos y herrajes", "Marco", "Ubicación de calces", "Colocar calces firmes próximos a los anclajes para evitar que el apriete deforme el perfil."),
        ("criterio-marco-no-anclar-tarrajeo", "Carpinterías, sellos y herrajes", "Marco", "Base resistente", "No confiar el anclaje únicamente al tarrajeo, espuma o material de relleno sin resistencia suficiente."),
        ("criterio-marco-coordinar-piso", "Carpinterías, sellos y herrajes", "Puerta", "Cota de piso terminado", "Definir la cota del piso terminado antes de fijar el marco para evitar hojas cortas o que rocen."),
        ("criterio-puerta-coordinar-barrido", "Puertas, ventanas y cerrajería", "Puerta batiente", "Área de barrido", "Verificar que el giro no choque con muebles, aparatos sanitarios, interruptores, otras puertas ni rutas de circulación."),
        ("criterio-marco-proteger-obra", "Carpinterías, sellos y herrajes", "Marco instalado", "Protección temporal", "Proteger marcos y acabados frente a mortero, pintura, golpes, soldadura y tránsito de materiales."),
        ("criterio-marco-registro-anclajes", "Control de calidad de acabados", "Anclajes ocultos", "Registro fotográfico", "Fotografiar anclajes, calces y sellos antes de cubrirlos con tapajuntas o acabados."),

        ("criterio-puerta-madera-humedad", "Puertas, ventanas y cerrajería", "Puerta de madera", "Acondicionamiento", "Aclimatar la madera al ambiente de instalación y evitar montar hojas húmedas o almacenadas directamente sobre el piso."),
        ("criterio-puerta-madera-sellar-caras", "Puertas, ventanas y cerrajería", "Puerta de madera", "Protección integral", "Sellar o acabar ambas caras y todos los cantos, incluida la parte superior e inferior, para reducir deformaciones desiguales."),
        ("criterio-puerta-refuerzo-cerradura", "Puertas, ventanas y cerrajería", "Hoja de puerta", "Refuerzo para cerradura", "Comprobar que la zona de cerradura y bisagras tenga refuerzo compatible con el peso y el tipo de herraje."),
        ("criterio-puerta-bisagras-alineadas", "Puertas, ventanas y cerrajería", "Bisagras", "Alineación y capacidad", "Alinear los ejes de las bisagras y elegir cantidad y capacidad acordes con el peso, altura y frecuencia de uso de la hoja."),
        ("criterio-puerta-no-roce-descuelgue", "Puertas, ventanas y cerrajería", "Hoja de puerta", "Funcionamiento", "La hoja debe abrir y cerrar sin rozar el piso, marco o cerradura y sin mostrar descuelgue."),
        ("criterio-puerta-holguras-uniformes", "Puertas, ventanas y cerrajería", "Hoja y marco", "Holguras", "Mantener holguras uniformes y compatibles con el material, el acabado, los sellos y la dilatación prevista."),
        ("criterio-puerta-holgura-inferior-funcion", "Puertas, ventanas y cerrajería", "Borde inferior de puerta", "Holgura funcional", "Definir la holgura inferior según piso, ventilación, aislamiento acústico, humo o fuego; no cortarla arbitrariamente en obra."),
        ("criterio-puerta-bano-material-humedad", "Puertas, ventanas y cerrajería", "Puerta de baño", "Resistencia a humedad", "Usar materiales, cantos y acabados compatibles con vapor, salpicaduras y limpieza frecuente."),
        ("criterio-puerta-exterior-intemperie", "Puertas, ventanas y cerrajería", "Puerta exterior", "Exposición climática", "Seleccionar hoja, adhesivos, sellos, acabado y herrajes aptos para sol, lluvia, humedad y cambios de temperatura."),
        ("criterio-puerta-metal-proteccion", "Puertas, ventanas y cerrajería", "Puerta metálica", "Protección anticorrosiva", "Limpiar soldaduras y cortes y restituir la protección anticorrosiva antes del acabado final."),
        ("criterio-marco-metal-control-soldadura", "Puertas, ventanas y cerrajería", "Marco metálico", "Deformación por soldadura", "Controlar la secuencia de soldado y verificar diagonales para evitar alabeo y cierre defectuoso."),
        ("criterio-porton-topes-seguros", "Puertas, ventanas y cerrajería", "Portón", "Topes y retención", "Instalar topes y dispositivos de retención capaces de impedir recorridos descontrolados por viento, pendiente o impacto."),
        ("criterio-puerta-corredera-antidescarrilamiento", "Puertas, ventanas y cerrajería", "Puerta corrediza", "Antidescarrilamiento", "Incorporar guías, topes y dispositivos que impidan que la hoja se salga del riel o caiga durante el uso."),

        ("criterio-ventana-alfeizar-pendiente", "Puertas, ventanas y cerrajería", "Alféizar exterior", "Evacuación de agua", "Ejecutar pendiente hacia el exterior y un encuentro que aleje el agua del muro y del borde interior."),
        ("criterio-ventana-drenajes-libres", "Puertas, ventanas y cerrajería", "Ventana con drenaje", "Orificios de evacuación", "Mantener libres los orificios de drenaje y comprobar que descarguen al exterior."),
        ("criterio-ventana-no-sellar-drenaje", "Puertas, ventanas y cerrajería", "Perfil de ventana", "Continuidad del drenaje", "No cubrir con silicona, mortero o pintura las cámaras y salidas previstas para evacuar agua."),
        ("criterio-ventana-sello-compatible", "Carpinterías, sellos y herrajes", "Encuentro marco-muro", "Sellante perimetral", "Usar un sellante compatible con el perfil, muro, pintura, movimiento esperado y exposición ambiental."),
        ("criterio-ventana-fondo-junta", "Carpinterías, sellos y herrajes", "Junta perimetral", "Fondo de junta", "Usar fondo de junta cuando corresponda para controlar la profundidad y evitar adhesión del sellante en tres caras."),
        ("criterio-ventana-superficie-sello", "Carpinterías, sellos y herrajes", "Junta de sellado", "Preparación", "Aplicar el sellante sobre superficies limpias, secas, firmes y preparadas según el fabricante."),
        ("criterio-ventana-vidrio-calzos", "Puertas, ventanas y cerrajería", "Vidrio en marco", "Calzos de apoyo", "Apoyar el vidrio en calzos compatibles y ubicados de modo que transmitan las cargas sin concentrar esfuerzos en las esquinas."),
        ("criterio-ventana-vidrio-holgura", "Puertas, ventanas y cerrajería", "Vidrio", "Holgura de borde", "Conservar holgura respecto del marco y de elementos rígidos para permitir tolerancias y movimiento sin contacto directo."),
        ("criterio-ventana-empaques-continuos", "Puertas, ventanas y cerrajería", "Empaques y junquillos", "Continuidad", "Instalar empaques continuos, sin estirarlos excesivamente y con encuentros que no dejen vías de ingreso de agua."),
        ("criterio-ventana-operacion-limpieza", "Puertas, ventanas y cerrajería", "Ventana operable", "Uso y limpieza", "Comprobar que pueda abrirse, cerrarse, bloquearse y limpiarse de forma segura desde el ambiente al que sirve."),
        ("criterio-ventana-restrictor-infantil", "Protección frente a caídas y seguridad", "Ventana en altura", "Limitador de apertura", "Evaluar limitadores de apertura cuando exista riesgo infantil, sin impedir ventilación ni sustituir la protección normativa contra caídas."),
        ("criterio-mosquitero-fijacion", "Puertas, ventanas y cerrajería", "Mosquitero", "Fijación", "Fijar el mosquitero para que no se desprenda con el viento, pero sin considerarlo baranda ni protección contra caídas."),
        ("criterio-ventana-corredera-antielevacion", "Protección frente a caídas y seguridad", "Ventana corrediza", "Antielevación", "Incorporar topes o seguros que eviten levantar accidentalmente la hoja y sacarla del riel."),
        ("criterio-ventana-prueba-rociado", "Control de calidad de acabados", "Ventana exterior", "Prueba de agua", "Realizar una prueba controlada de rociado antes de la entrega y corregir el origen de cualquier filtración, no solo cubrirla con más silicona."),

        ("criterio-cerradura-altura-usuario", "Puertas, ventanas y cerrajería", "Cerradura y manija", "Altura de instalación", "Coordinar la altura con accesibilidad, tipo de usuario, diseño de hoja y cuadro de herrajes antes de perforar."),
        ("criterio-manija-palanca", "Puertas, ventanas y cerrajería", "Manija", "Facilidad de operación", "Preferir mecanismos que puedan accionarse con una mano y sin giro fuerte de muñeca cuando se requiera accesibilidad."),
        ("criterio-cerradura-no-doble-llave-evacuacion", "Evacuación y protección contra incendios", "Puerta en ruta de salida", "Liberación interior", "No instalar mecanismos que obliguen a buscar una llave para salir durante una emergencia."),
        ("criterio-cerradura-cerradero-alineado", "Puertas, ventanas y cerrajería", "Cerradura y cerradero", "Alineación", "Alinear pestillo y cerradero para que la puerta asegure sin levantarla, empujarla con fuerza o golpearla."),
        ("criterio-herraje-tornillo-sustrato", "Puertas, ventanas y cerrajería", "Herraje", "Fijaciones", "Usar tornillos y fijaciones con longitud, material y rosca adecuados al refuerzo y al sustrato."),
        ("criterio-cierrapuerta-ajuste", "Puertas, ventanas y cerrajería", "Cierrapuertas", "Velocidad y golpe final", "Ajustar velocidad y golpe final para que la puerta cierre y trabe sin golpear ni quedar entreabierta."),
        ("criterio-cortafuego-no-perforar", "Evacuación y protección contra incendios", "Puerta cortafuego", "Intervenciones posteriores", "No taladrar, recortar ni agregar accesorios que no formen parte del sistema certificado."),
        ("criterio-barra-antipanico-operacion", "Evacuación y protección contra incendios", "Barra antipánico", "Funcionamiento", "Probar la barra en toda su longitud útil y verificar que libere la puerta sin movimientos adicionales."),
        ("criterio-bisagra-exterior-seguridad", "Protección frente a caídas y seguridad", "Puerta exterior con bisagras expuestas", "Protección contra desmontaje", "Usar pasadores, pernos o herrajes de seguridad cuando el lado de las bisagras quede accesible desde el exterior."),
        ("criterio-seguro-ventana-operable", "Puertas, ventanas y cerrajería", "Cierre de ventana", "Accionamiento", "El seguro debe accionar sin piezas flojas y mantener la hoja cerrada frente a viento y uso normal."),
        ("criterio-seguro-infantil-no-reemplaza-baranda", "Protección frente a caídas y seguridad", "Seguro infantil", "Alcance de protección", "No considerar un seguro infantil como sustituto de barandas, antepechos o vidrios de seguridad exigibles."),
        ("criterio-mirilla-altura-usuarios", "Puertas, ventanas y cerrajería", "Mirilla de puerta", "Altura y campo visual", "Definir la altura y el campo visual según los usuarios; puede requerirse una segunda mirilla accesible."),
        ("criterio-cerradura-no-bloquear-salida", "Evacuación y protección contra incendios", "Cerradura electrónica o control de acceso", "Liberación de emergencia", "Comprobar que la falla eléctrica o emergencia no deje bloqueada la salida cuando esta forma parte de la evacuación."),
        ("criterio-porton-automatizado-deteccion", "Protección frente a caídas y seguridad", "Portón automatizado", "Protección de atrapamiento", "Incorporar dispositivos de detección, parada y reversa acordes con el equipo para reducir riesgo de golpe o atrapamiento."),

        ("criterio-herraje-lubricante-compatible", "Mantenimiento de la vivienda", "Herrajes", "Lubricación", "Usar lubricantes compatibles y evitar productos que atraigan polvo, manchen acabados o deterioren sellos."),
        ("criterio-carpinteria-ciclos-operacion", "Control de calidad de acabados", "Puertas y ventanas", "Prueba funcional", "Abrir, cerrar, asegurar y liberar cada elemento repetidas veces para detectar roce, juego, descuelgue o falla de herrajes."),
        ("criterio-puerta-probar-con-sellos", "Control de calidad de acabados", "Puerta con burletes", "Cierre completo", "Probar la cerradura con los sellos y burletes instalados, porque estos pueden impedir que el pestillo engrane."),
        ("criterio-ventana-infiltracion-revisar-origen", "Control de calidad de acabados", "Ventana exterior", "Diagnóstico de filtración", "Distinguir si el ingreso de agua proviene del sellado, drenaje, perfil, vidrio, alféizar o muro antes de reparar."),
        ("criterio-carpinteria-limpieza-no-abrasiva-final", "Mantenimiento de la vivienda", "Perfiles, vidrio y herrajes", "Limpieza", "Limpiar con productos compatibles y herramientas no abrasivas que no rayen, manchen ni retiren recubrimientos."),
        ("criterio-perfil-retirar-pelicula", "Carpinterías, sellos y herrajes", "Perfil protegido", "Retiro de película", "Retirar la película protectora dentro del plazo indicado para evitar que quede adherida por sol, calor o envejecimiento."),
        ("criterio-metal-retocar-proteccion", "Carpinterías, sellos y herrajes", "Carpintería metálica", "Retoque", "Retocar cortes, perforaciones y daños del recubrimiento antes de la entrega para evitar corrosión prematura."),
        ("criterio-entrega-llaves-cuadro-herrajes", "Control de calidad de acabados", "Cerrajería terminada", "Entrega", "Entregar llaves identificadas, duplicados acordados y relación de cerraduras y herrajes instalados."),
        ("criterio-entrega-manual-mantenimiento", "Mantenimiento de la vivienda", "Puertas y ventanas", "Instrucciones", "Conservar fichas, garantías y frecuencia de limpieza, ajuste, lubricación y renovación de sellos."),
        ("criterio-carpinteria-registro-fotografico", "Control de calidad de acabados", "Carpintería instalada", "Trazabilidad", "Registrar modelos, etiquetas, certificados, anclajes ocultos y pruebas relevantes para futuras reparaciones."),
        ("criterio-carpinteria-lista-observaciones", "Control de calidad de acabados", "Recepción", "Lista de pendientes", "Revisar rayaduras, golpes, filtraciones, cierres, llaves, vidrios, sellos y accesorios antes de dar conformidad."),
        ("criterio-carpinteria-conforme-obra", "Control de calidad de acabados", "Planos conforme a obra", "Actualización", "Actualizar cambios de sentido de apertura, dimensiones, material, tipo de vidrio, cerradura y control de acceso."),
    ]

    for item in criterios:
        registros.append(criterio(*item))

    if len(registros) != 84:
        raise SystemExit(f"Se esperaban 84 registros y se generaron {len(registros)}.")
    return registros


def main() -> None:
    registros = construir_registros()
    base = json.loads(NORMATIVA.read_text(encoding="utf-8"))
    banco = json.loads(PREGUNTAS.read_text(encoding="utf-8"))

    if base.get("version") != "2.5.0" or len(base.get("parametros", [])) != 1519:
        raise SystemExit("La rama no parte de la versión 2.5.0 esperada.")

    ids_nuevos = [item["id"] for item in registros]
    if len(ids_nuevos) != len(set(ids_nuevos)):
        raise SystemExit("El inventario contiene identificadores duplicados.")
    ids_existentes = {item["id"] for item in base["parametros"]}
    repetidos = sorted(set(ids_nuevos) & ids_existentes)
    if repetidos:
        raise SystemExit("Parámetros ya existentes: " + ", ".join(repetidos))

    todas_preguntas = [
        pregunta
        for categoria in banco.get("categorias", [])
        for pregunta in categoria.get("preguntas", [])
        if isinstance(pregunta, dict)
    ]
    max_q = max(int(item["id"][1:]) for item in todas_preguntas if re.fullmatch(r"q\d+", item.get("id", "")))
    categorias = {categoria["nombre"]: categoria for categoria in banco["categorias"]}

    for indice, registro in enumerate(registros, start=1):
        qid = f"q{max_q + indice}"
        parametro = {k: v for k, v in registro.items() if k not in {"faq_categoria", "pregunta", "respuesta"}}
        parametro["faq_relacionadas"] = [qid]
        base["parametros"].append(parametro)

        nombre_categoria = registro["faq_categoria"]
        categoria = categorias.get(nombre_categoria)
        if categoria is None:
            categoria = {"nombre": nombre_categoria, "preguntas": []}
            banco["categorias"].append(categoria)
            categorias[nombre_categoria] = categoria
        categoria["preguntas"].append({"id": qid, "pregunta": registro["pregunta"], "respuesta": registro["respuesta"]})

    base["version"] = "2.6.0"
    base["fecha_revision"] = "2026-07-27"

    ids_finales = [item["id"] for item in base["parametros"]]
    faq_finales = [
        item["id"]
        for categoria in banco["categorias"]
        for item in categoria.get("preguntas", [])
        if isinstance(item, dict)
    ]
    if len(ids_finales) != len(set(ids_finales)) or len(faq_finales) != len(set(faq_finales)):
        raise SystemExit("La ampliación produjo identificadores duplicados.")

    total_parametros = len(base["parametros"])
    total_preguntas = len(faq_finales)
    total_validados = sum(item.get("estado_revision") == "validado_con_numeral" for item in base["parametros"])
    total_criterios = sum(item.get("estado_revision") == "criterio_tecnico_revisado" for item in base["parametros"])
    if (total_parametros, total_preguntas, total_validados, total_criterios) != (1603, 3066, 1229, 356):
        raise SystemExit(
            f"Totales inesperados: parámetros={total_parametros}, preguntas={total_preguntas}, "
            f"validados={total_validados}, criterios={total_criterios}."
        )

    NORMATIVA.write_text(json.dumps(base, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    PREGUNTAS.write_text(json.dumps(banco, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    check = CHECK.read_text(encoding="utf-8")
    check = reemplazar_unico(check, "if len(base.parametros) < 1519:", "if len(base.parametros) < 1603:")
    check = reemplazar_unico(check, "por lo menos 1519 parámetros revisados", "por lo menos 1603 parámetros revisados")
    check = reemplazar_unico(check, "if validados < 1210:", "if validados < 1229:")
    check = reemplazar_unico(check, "al menos 1210 numerales RNE validados", "al menos 1229 numerales RNE validados")
    check = reemplazar_unico(check, 'if base.version != "2.5.0":', 'if base.version != "2.6.0":')
    check = reemplazar_unico(check, "La versión normativa esperada es 2.5.0", "La versión normativa esperada es 2.6.0")
    check = reemplazar_unico(check, "if criterios < 291:", "if criterios < 356:")
    check = reemplazar_unico(check, "al menos 291 criterios técnicos revisados", "al menos 356 criterios técnicos revisados")
    check = reemplazar_unico(check, "if len(todas) < 2982:", "if len(todas) < 3066:")
    check = reemplazar_unico(
        check,
        "La base ampliada de instalaciones sanitarias requiere por lo menos 2982 preguntas técnicas.",
        "La base ampliada de puertas, ventanas y cerrajería requiere por lo menos 3066 preguntas técnicas.",
    )

    pruebas = '''\n    puerta_vivienda = api.detalle_parametro_normativo("a020-vano-puerta-principal-vivienda-ancho-minimo")\n    if puerta_vivienda["valor"]["valor"] != 0.90:\n        raise SystemExit("La puerta principal de vivienda debe conservar 0.90 m.")\n\n    puerta_fuego = api.detalle_parametro_normativo("a130-puerta-cortafuego-resistencia-relativa")\n    if puerta_fuego["valor"]["valor"] != 75:\n        raise SystemExit("La puerta cortafuego debe conservar la relación de 75%.")\n\n    puerta_corredera = api.detalle_parametro_normativo("criterio-puerta-corredera-antidescarrilamiento")\n    if puerta_corredera["estado_revision"] != "criterio_tecnico_revisado":\n        raise SystemExit("El antidescarrilamiento debe conservarse como criterio técnico revisado.")\n\n'''
    check = reemplazar_unico(check, "    preguntas = json.loads(\n", pruebas + "    preguntas = json.loads(\n")
    CHECK.write_text(check, encoding="utf-8")

    DOC.write_text(
        f"""# Validación de puertas, ventanas, cerrajería y seguridad — 27 de julio de 2026

## Alcance

Se incorporaron **{len(registros)} parámetros** y **{len(registros)} preguntas** después de depurar 306 registros relacionados de la versión 2.5.0.

## Contenido

- anchos mínimos residenciales y puertas de varias hojas;
- compatibilidad de vanos, clima y materiales;
- puertas de evacuación, cortafuego y cortahumo;
- marcos, anclajes, calces, holguras y coordinación con acabados;
- hojas de madera y metal, bisagras, cerraduras y portones;
- ventanas, drenajes, sellos, vidrios, empaques y pruebas de agua;
- seguridad infantil, antidescarrilamiento y control de acceso;
- inspección, mantenimiento, trazabilidad y recepción.

## Fuentes

- Normas A.020 Vivienda, A.120 Accesibilidad Universal y A.130 Requisitos de Seguridad del RNE.
- Norma E.040 Vidrio ya consolidada en la versión 2.3.0.
- Formación oficial SENCICO sobre carpintería de acabados.

## Resultado

- Versión normativa: `2.6.0`.
- Parámetros totales: `{total_parametros}`.
- Registros `validado_con_numeral`: `{total_validados}`.
- Criterios técnicos revisados: `{total_criterios}`.
- Preguntas técnicas: `{total_preguntas}`.

## Criterios editoriales

- Se conservaron sin duplicar las reglas existentes de accesibilidad, evacuación, barandas, ventanas bajas y vidrio de seguridad.
- Los anchos obligatorios se limitaron a cifras expresas de la A.020 y A.120.
- Las prácticas de montaje, ajuste, seguridad y mantenimiento se identifican como `criterio_tecnico_revisado`.
- La propuesta de modificación de la A.130 publicada en julio de 2026 no se trató como norma vigente.
- La información no reemplaza planos, certificaciones de productos, ensayos ni supervisión profesional.
""",
        encoding="utf-8",
    )

    print(f"Ampliación aplicada: {len(registros)} parámetros y preguntas; versión 2.6.0.")


if __name__ == "__main__":
    main()
