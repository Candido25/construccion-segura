from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
NORMATIVA = BACKEND / "normativa_tecnica.json"
PREGUNTAS = BACKEND / "preguntas_tecnicas.json"
CHECK = ROOT / "scripts" / "check_normativa.py"
DOC = ROOT / "docs" / "VALIDACION_IMPERMEABILIZACION_HUMEDAD_2026-07-27.md"

SENCICO = "https://eventos.sencico.gob.pe/Evento/Inscripcion/8nWdRNNA0kY%3D"


def criterio(
    identificador: str,
    elemento: str,
    parametro: str,
    texto: str,
    pregunta: str | None = None,
    categoria: str = "Impermeabilización, Humedad y Drenaje",
) -> dict:
    pregunta_final = pregunta or f"¿Qué debo revisar sobre {parametro.lower()} en {elemento.lower()}?"
    return {
        "id": identificador,
        "categoria": categoria,
        "elemento": elemento,
        "parametro": parametro,
        "clasificacion": "recomendacion",
        "valor": {
            "tipo": "sin_valor_universal",
            "valor": None,
            "minimo": None,
            "maximo": None,
            "unidad": None,
            "formula": None,
            "texto": texto,
        },
        "condiciones": [
            "La solución depende del origen del agua, exposición, presión hidrostática, movimiento, sustrato, sistema especificado y fabricante."
        ],
        "fuente": {
            "tipo": "criterio_tecnico",
            "norma": "Formación técnica SENCICO",
            "denominacion": "Impermeabilización de techo, cimientos, tanques cisternas, piscinas y zonas húmedas",
            "dispositivo": None,
            "numeral": "Aplicación práctica supervisada",
            "numeral_confirmado": False,
            "url_oficial": SENCICO,
        },
        "estado_revision": "criterio_tecnico_revisado",
        "advertencia": "No sustituye el diagnóstico de la causa, el diseño del sistema, las fichas técnicas, las pruebas ni la supervisión profesional.",
        "faq_relacionadas": [],
        "fecha_revision": "2026-07-27",
        "pregunta": pregunta_final,
        "respuesta": texto + " La reparación debe verificarse antes de cubrirla o entregarla.",
    }


def rep(texto: str, anterior: str, nuevo: str) -> str:
    if texto.count(anterior) != 1:
        raise SystemExit(f"Coincidencia inesperada para: {anterior}")
    return texto.replace(anterior, nuevo, 1)


REGISTROS = [
    # Planeamiento y selección del sistema
    criterio("criterio-impermeabilizacion-diagnostico-origen", "Área con humedad", "Diagnóstico de la fuente", "Identificar si el agua proviene de lluvia, fuga de tubería, capilaridad, presión del terreno, condensación o falla de junta antes de elegir la reparación.", "¿Toda mancha de humedad se repara con el mismo impermeabilizante?"),
    criterio("criterio-impermeabilizacion-presion-positiva-negativa", "Elemento expuesto al agua", "Cara de aplicación", "Definir si el sistema trabajará por la cara de ingreso del agua o por la cara opuesta y comprobar que el producto sea apto para esa condición.", "¿Es igual impermeabilizar por donde entra el agua que desde el lado interior?"),
    criterio("criterio-impermeabilizacion-sistema-exposicion", "Superficie a impermeabilizar", "Selección por exposición", "Elegir el sistema considerando tránsito, radiación solar, agua permanente, inmersión, presión, temperatura, químicos y posibilidad de mantenimiento."),
    criterio("criterio-impermeabilizacion-compatibilidad-capases", "Sistema multicapa", "Compatibilidad entre productos", "Comprobar compatibilidad entre imprimante, membrana, adhesivo, mortero de protección, sellante y acabado; no combinar productos solo por apariencia similar."),
    criterio("criterio-impermeabilizacion-detalle-proyecto", "Proyecto de impermeabilización", "Detalles constructivos", "Definir previamente encuentros, remates, penetraciones, juntas, desagües, umbrales y cambios de material, porque las fallas suelen comenzar en esos puntos."),
    criterio("criterio-impermeabilizacion-muestra-sistema", "Sistema de impermeabilización", "Área de muestra", "Ejecutar una muestra o tramo de prueba cuando el soporte, acabado o procedimiento no hayan sido comprobados en la obra."),
    criterio("criterio-impermeabilizacion-clima-aplicacion", "Aplicación exterior", "Condiciones ambientales", "No aplicar durante lluvia, sobre agua empozada, con condensación o fuera de los rangos de temperatura, viento y humedad indicados por el fabricante."),
    criterio("criterio-impermeabilizacion-secuencia-oficios", "Obra con varias especialidades", "Coordinación de trabajos", "Programar instalaciones, anclajes, albañilería y acabados para evitar perforar o cortar posteriormente la impermeabilización."),
    criterio("criterio-impermeabilizacion-material-almacenamiento", "Productos impermeabilizantes", "Almacenamiento", "Conservar envases cerrados, identificados y protegidos de sol, lluvia, congelamiento, calor y contaminación según la ficha técnica."),
    criterio("criterio-impermeabilizacion-lote-vencimiento", "Producto impermeabilizante", "Trazabilidad del material", "Verificar lote, fecha de vencimiento, estado del envase y homogeneidad antes de usar el producto."),

    # Preparación del soporte
    criterio("criterio-impermeabilizacion-sustrato-firme", "Sustrato", "Resistencia y cohesión", "Retirar partes sueltas, lechada débil, tarrajeos desprendidos y recubrimientos sin adherencia hasta encontrar una base firme."),
    criterio("criterio-impermeabilizacion-sustrato-limpio", "Sustrato", "Limpieza", "Eliminar polvo, aceite, grasa, desmoldante, pintura, sales y residuos que impidan la adherencia."),
    criterio("criterio-impermeabilizacion-sustrato-humedad", "Sustrato", "Condición de humedad", "Comprobar si el sistema requiere soporte seco, húmedo sin brillo superficial o una humedad máxima específica antes de aplicar."),
    criterio("criterio-impermeabilizacion-concreto-curado", "Concreto o mortero nuevo", "Maduración del soporte", "Respetar el curado y la maduración exigidos antes de cerrar la humedad con una membrana o revestimiento."),
    criterio("criterio-impermeabilizacion-poros-oquedades", "Concreto o tarrajeo", "Reparación de defectos", "Rellenar cangrejeras, poros abiertos, nidos, huecos y desprendimientos con material compatible antes de impermeabilizar."),
    criterio("criterio-impermeabilizacion-fisura-clasificar", "Sustrato fisurado", "Clasificación de fisuras", "Determinar si la fisura está activa, estabilizada, estructural o solo superficial antes de decidir entre sellado flexible, reparación rígida o evaluación estructural."),
    criterio("criterio-impermeabilizacion-fisura-no-puente-rigido", "Fisura con movimiento", "Tratamiento flexible", "No cubrir una fisura activa con una capa rígida esperando que deje de abrirse; usar un detalle capaz de admitir el movimiento o corregir la causa."),
    criterio("criterio-impermeabilizacion-aristas-suavizar", "Esquina o arista", "Geometría del soporte", "Redondear o biselar aristas agudas cuando el sistema pueda cortarse, adelgazarse o despegarse sobre ellas."),
    criterio("criterio-impermeabilizacion-media-cana", "Encuentro piso-muro", "Media caña", "Formar una media caña o detalle equivalente compatible para evitar un quiebre brusco de la membrana en el ángulo interior."),
    criterio("criterio-impermeabilizacion-pendiente-soporte", "Piso o cubierta", "Formación de pendientes", "Construir las pendientes en el soporte o capa prevista; no pretender corregir depresiones importantes aumentando el espesor del impermeabilizante."),
    criterio("criterio-impermeabilizacion-depresiones-corregir", "Superficie con empozamientos", "Regularización", "Corregir depresiones, lomos y contrapendientes antes de aplicar el sistema para conducir el agua hacia los puntos de drenaje."),
    criterio("criterio-impermeabilizacion-imprimante-compatible", "Sustrato preparado", "Imprimación", "Usar el imprimante previsto para el soporte y la membrana, con la dilución, rendimiento y tiempo de espera indicados."),

    # Juntas, encuentros y penetraciones
    criterio("criterio-impermeabilizacion-junta-movimiento-respetar", "Junta estructural o de movimiento", "Continuidad funcional", "Mantener la junta y resolverla con un sistema flexible diseñado para su movimiento; no rellenarla rígidamente ni puentearla sin detalle."),
    criterio("criterio-impermeabilizacion-junta-fondo-sellante", "Junta sellada", "Geometría del sellante", "Controlar ancho y profundidad con fondo de junta compatible cuando corresponda y evitar la adhesión del sellante en tres caras."),
    criterio("criterio-impermeabilizacion-junta-bordes-firmes", "Bordes de junta", "Preparación", "Asegurar bordes firmes, limpios y secos o imprimados según el sellante antes de ejecutar la junta."),
    criterio("criterio-impermeabilizacion-cambio-material-refuerzo", "Encuentro de materiales distintos", "Refuerzo", "Incorporar banda, malla o detalle flexible cuando el cambio de material pueda concentrar fisuración o movimiento."),
    criterio("criterio-impermeabilizacion-penetracion-manga", "Paso de tubería", "Manga y holgura", "Prever una manga o detalle que permita sellar el espacio alrededor de la tubería sin dejarla aprisionada por un relleno frágil."),
    criterio("criterio-impermeabilizacion-penetracion-refuerzo-sello", "Penetración en zona impermeabilizada", "Refuerzo perimetral", "Reforzar y sellar alrededor de tuberías, pernos, soportes y cajas con componentes compatibles y continuidad visible."),
    criterio("criterio-impermeabilizacion-anclaje-posterior-prohibir", "Membrana terminada", "Perforaciones posteriores", "No perforar la impermeabilización para fijar equipos, barandas o tuberías sin un detalle de sellado diseñado y autorizado."),
    criterio("criterio-impermeabilizacion-umbral-continuidad", "Umbral de puerta", "Continuidad del sistema", "Resolver la continuidad bajo y alrededor del umbral sin crear un punto bajo que permita el ingreso de agua al ambiente contiguo."),
    criterio("criterio-impermeabilizacion-muro-piso-subida", "Encuentro de piso y muro", "Retorno vertical", "Prolongar la impermeabilización por el paramento vertical hasta la altura definida por la exposición y el detalle del proyecto; no usar una altura universal para todos los casos."),
    criterio("criterio-impermeabilizacion-remate-regata", "Remate superior de membrana", "Terminación", "Fijar y sellar el borde superior mediante regata, perfil, tapajunta o detalle compatible para que el agua no ingrese detrás de la membrana."),
    criterio("criterio-impermeabilizacion-sumidero-brida", "Sumidero o dren", "Integración con la membrana", "Conectar la membrana con la brida, aro de apriete o accesorio previsto por el sistema, sin limitarse a aplicar sellante alrededor de la rejilla."),
    criterio("criterio-impermeabilizacion-sumidero-perimetro-reforzar", "Encuentro con sumidero", "Refuerzo localizado", "Reforzar el perímetro del dren y mantener libre la sección de descarga durante todas las capas de trabajo."),

    # Mezcla y aplicación
    criterio("criterio-impermeabilizacion-mezcla-proporcion", "Producto de varios componentes", "Dosificación", "Mezclar componentes completos o medirlos con precisión en la proporción indicada; no dosificar a ojo."),
    criterio("criterio-impermeabilizacion-mezcla-herramienta", "Mezcla impermeabilizante", "Homogeneización", "Usar la herramienta y velocidad recomendadas para obtener una mezcla uniforme sin incorporar aire excesivo."),
    criterio("criterio-impermeabilizacion-no-diluir", "Producto listo o dosificado", "Dilución", "No agregar agua, solvente, cemento u otro material salvo que la ficha técnica lo autorice expresamente."),
    criterio("criterio-impermeabilizacion-pot-life", "Mezcla preparada", "Tiempo útil", "Desechar la mezcla que superó su vida útil; no recuperarla añadiendo agua o solvente."),
    criterio("criterio-impermeabilizacion-capas-cruzadas", "Membrana líquida", "Dirección de capas", "Aplicar el número de capas y la orientación indicados, procurando cobertura uniforme y evitando poros o zonas transparentes."),
    criterio("criterio-impermeabilizacion-secado-entre-capas", "Sistema multicapa", "Tiempo entre manos", "Respetar el intervalo mínimo y máximo entre capas y preparar nuevamente la superficie si se excede la ventana de repintado."),
    criterio("criterio-impermeabilizacion-consumo-control", "Membrana aplicada", "Rendimiento", "Controlar el consumo por área y los envases utilizados para comprobar que se alcanzó la cantidad especificada."),
    criterio("criterio-impermeabilizacion-espesor-control", "Membrana", "Espesor", "Medir o verificar el espesor húmedo o seco mediante el método aplicable y corregir zonas insuficientes antes de cubrir."),
    criterio("criterio-impermeabilizacion-malla-sin-arrugas", "Membrana reforzada", "Colocación de malla", "Embeber la malla o banda sin arrugas, bolsas, pliegues ni sectores secos y mantener los traslapes definidos."),
    criterio("criterio-impermeabilizacion-solape-membrana", "Membrana en rollo", "Traslapes", "Ejecutar traslapes limpios, continuos y del ancho indicado, orientados para no favorecer el ingreso de agua."),
    criterio("criterio-impermeabilizacion-soplete-seguridad", "Membrana aplicada con calor", "Control de llama y fuego", "Aplicar sistemas con soplete solo por personal capacitado, retirando combustibles y manteniendo extintor y vigilancia de incendio."),
    criterio("criterio-impermeabilizacion-sin-burbujas", "Membrana terminada", "Defectos de aplicación", "Revisar ampollas, burbujas, poros, pliegues, bordes levantados y falta de adherencia antes de proteger el sistema."),

    # Cubiertas, azoteas y terrazas
    criterio("criterio-cubierta-pendiente-antes-membrana", "Azotea o terraza", "Pendiente previa", "Comprobar con nivel o instrumento que la pendiente conduce hacia los drenajes antes de impermeabilizar."),
    criterio("criterio-cubierta-empozamiento-prueba", "Cubierta terminada", "Control de empozamientos", "Realizar una descarga o prueba controlada para detectar zonas donde el agua permanece retenida más allá de lo aceptable para el sistema."),
    criterio("criterio-cubierta-parapeto-retorno", "Encuentro de cubierta con parapeto", "Retorno y remate", "Dar continuidad a la membrana en el encuentro, reforzar el ángulo y proteger el remate superior contra ingreso posterior de agua."),
    criterio("criterio-cubierta-coronacion-goteron", "Coronación o borde", "Goterón", "Disponer pendiente, goterón o remate que aleje el agua de la fachada y evite que retorne por la cara inferior."),
    criterio("criterio-cubierta-penetracion-refuerzo-sello", "Tubería o soporte en cubierta", "Sellado de penetración", "Resolver cada penetración con manguito, banda o pieza compatible, evitando depender únicamente de un cordón superficial de silicona."),
    criterio("criterio-cubierta-equipo-base-elevada", "Equipo sobre azotea", "Base y apoyo", "Coordinar bases, apoyos y recorridos para que el equipo no perfore, aplaste ni bloquee el drenaje de la impermeabilización."),
    criterio("criterio-cubierta-membrana-uv", "Membrana expuesta", "Protección ultravioleta", "Verificar que la membrana sea apta para exposición solar o instalar la protección superficial exigida por el sistema."),
    criterio("criterio-cubierta-proteccion-mecanica", "Membrana no transitable", "Capa de protección", "Colocar protección compatible antes de tránsito, mantenimiento, contrapiso, grava o instalación de equipos."),
    criterio("criterio-cubierta-proteccion-no-bloquear-drenaje", "Capa de protección de cubierta", "Continuidad del drenaje", "Evitar que mortero, grava, geotextil o protección obstruyan sumideros, reboses o canales de evacuación."),
    criterio("criterio-cubierta-rebose-emergencia", "Azotea con parapetos", "Ruta de rebose", "Verificar la solución de rebose o alivio prevista por el proyecto para que una obstrucción no produzca acumulación peligrosa de agua."),
    criterio("criterio-cubierta-sumidero-mantenimiento", "Sumidero de azotea", "Acceso", "Mantener rejillas, canastillas y registros accesibles para retirar hojas, residuos y sedimentos."),
    criterio("criterio-cubierta-canaleta-no-perforar", "Canaleta impermeabilizada", "Fijaciones", "Ubicar soportes y tornillos sin crear perforaciones no selladas en la zona que conduce agua."),
    criterio("criterio-cubierta-trafico-rutas", "Azotea con equipos", "Rutas de mantenimiento", "Definir pasos o losetas de protección para que el mantenimiento no desgaste ni punzone la membrana."),
    criterio("criterio-cubierta-no-tapar-fuga", "Filtración en techo", "Reparación localizada", "No extender producto al azar sobre toda la superficie sin localizar primero el punto de ingreso, el recorrido del agua y el detalle fallado."),

    # Baños, duchas y zonas húmedas
    criterio("criterio-zona-humeda-enchape-no-impermeabiliza", "Baño o ducha", "Función del enchape", "No considerar la cerámica, la fragua o la pintura como sustitutos de una impermeabilización cuando el sistema la requiera."),
    criterio("criterio-zona-humeda-area-expuesta", "Muro de ducha", "Extensión del tratamiento", "Definir la extensión vertical y lateral de la impermeabilización según salpicadura, ducha, tina, nichos y proyecto; no aplicar una franja arbitraria."),
    criterio("criterio-zona-humeda-esquina-banda", "Esquina de baño", "Refuerzo flexible", "Reforzar esquinas interiores, encuentros con muros y cambios de plano con la banda o malla del sistema."),
    criterio("criterio-zona-humeda-paso-griferia", "Paso de grifería", "Sellado", "Sellar las penetraciones de mezcladoras, duchas, llaves y accesorios sin impedir su mantenimiento."),
    criterio("criterio-zona-humeda-nicho-ducha", "Nicho de ducha", "Pendiente y continuidad", "Dar pendiente hacia el interior de la ducha y mantener continuidad en esquinas, fondo, laterales y borde del nicho."),
    criterio("criterio-zona-humeda-sardinel-continuidad", "Sardinel o umbral de ducha", "Continuidad", "Impermeabilizar de forma continua el sardinel, sus caras y encuentros, evitando terminar la membrana justo en la arista."),
    criterio("criterio-zona-humeda-ducha-sin-sardinel", "Ducha sin sardinel", "Contención del agua", "Coordinar pendientes, longitud de drenaje, mampara y continuidad de la membrana para impedir que el agua alcance áreas secas."),
    criterio("criterio-zona-humeda-sumidero-cota", "Piso de baño", "Cota del dren", "Comprobar que el dren quede en el punto bajo considerando impermeabilización, adhesivo, enchape y rejilla terminada."),
    criterio("criterio-zona-humeda-no-perforar-piso", "Piso impermeabilizado", "Fijaciones", "No fijar mamparas, muebles o accesorios atravesando el piso impermeabilizado sin un detalle aprobado de sellado."),
    criterio("criterio-zona-humeda-sello-elastico-cambios", "Encuentro de enchapes", "Sello de movimiento", "Usar un sello elástico compatible en cambios de plano y juntas previstas, en vez de rellenarlos rígidamente con fragua."),

    # Jardineras, cisternas, piscinas y elementos enterrados
    criterio("criterio-jardinera-sistema-raices", "Jardinera", "Resistencia a raíces", "Usar una barrera o membrana apta para contacto con raíces y suelo húmedo cuando corresponda."),
    criterio("criterio-jardinera-proteccion-membrana", "Jardinera", "Protección mecánica", "Proteger la impermeabilización antes de colocar drenaje, piedras, sustrato o herramientas de jardinería."),
    criterio("criterio-jardinera-capa-drenante", "Jardinera", "Drenaje", "Incorporar una capa drenante y salida funcional para evitar presión permanente de agua contra la membrana."),
    criterio("criterio-jardinera-geotextil-filtro", "Jardinera", "Filtro", "Separar el sustrato de la capa drenante con un filtro compatible para reducir el arrastre de finos y la obstrucción."),
    criterio("criterio-jardinera-rebose", "Jardinera", "Rebose", "Prever una descarga o rebose verificable para lluvias o riego excesivo sin afectar fachadas ni ambientes interiores."),
    criterio("criterio-cisterna-revestimiento-agua-potable", "Cisterna o tanque", "Compatibilidad sanitaria", "Usar un revestimiento autorizado para contacto con agua potable cuando el depósito almacene agua de consumo."),
    criterio("criterio-cisterna-sustrato-curado", "Cisterna de concreto", "Preparación estructural", "Esperar el curado, reparar cangrejeras y tratar juntas y penetraciones antes de aplicar el revestimiento impermeable."),
    criterio("criterio-cisterna-junta-construccion", "Junta de cisterna", "Tratamiento", "Resolver juntas de vaciado y construcción con el sistema previsto, considerando presión de agua y posibles movimientos."),
    criterio("criterio-cisterna-pasamuros", "Paso de tubería en cisterna", "Sello hidráulico", "Usar pasamuros, bridas o sellos diseñados para presión y contacto permanente, sin depender de mortero suelto alrededor del tubo."),
    criterio("criterio-cisterna-prueba-hidrostatica", "Cisterna o tanque terminado", "Prueba de estanqueidad", "Realizar una prueba hidrostática controlada antes de desinfectar y poner en servicio, observando niveles y superficies exteriores accesibles."),
    criterio("criterio-cisterna-reparar-reprobar", "Cisterna con fuga", "Reprueba", "Reparar el detalle fallado y repetir la prueba completa del volumen afectado antes de aceptar el depósito."),
    criterio("criterio-cisterna-no-recubrimiento-toxico", "Depósito de agua", "Producto de revestimiento", "No usar pinturas, solventes o recubrimientos sin aptitud para inmersión y para el uso sanitario previsto."),
    criterio("criterio-enterrado-agua-lado-positivo", "Muro enterrado", "Impermeabilización exterior", "Cuando sea accesible, preferir el control del agua por el lado de ingreso y complementar con drenaje y protección del sistema."),
    criterio("criterio-enterrado-proteccion-membrana", "Muro enterrado impermeabilizado", "Protección durante relleno", "Instalar lámina o tablero de protección para impedir que piedras y compactación perforen la membrana."),
    criterio("criterio-enterrado-dren-perimetral", "Muro o cimentación enterrada", "Drenaje perimetral", "Diseñar el dren, filtro, pendiente y punto de descarga; no colocar tubería perforada sin una salida funcional."),
    criterio("criterio-enterrado-napa-evaluacion", "Elemento bajo nivel del terreno", "Presión hidrostática", "Evaluar nivel freático, presión, flotación y continuidad del sistema antes de decidir una impermeabilización interior o exterior."),

    # Pruebas y control de calidad
    criterio("criterio-impermeabilizacion-curado-antes-prueba", "Sistema recién aplicado", "Espera antes de ensayo", "Respetar el curado mínimo del sistema antes de llenarlo, inundarlo, transitarlo o someterlo a presión."),
    criterio("criterio-impermeabilizacion-prueba-tapon-seguro", "Prueba de inundación", "Cierre del dren", "Usar un tapón que permita ensayar el encuentro con el dren cuando corresponda y que pueda retirarse sin dañar la instalación."),
    criterio("criterio-impermeabilizacion-prueba-nivel-registro", "Prueba de inundación", "Registro del nivel", "Marcar y registrar nivel inicial, hora, área ensayada y nivel final, controlando pérdidas ajenas a una filtración."),
    criterio("criterio-impermeabilizacion-prueba-evaporacion", "Prueba prolongada", "Control de evaporación", "Usar un recipiente testigo o método equivalente cuando la evaporación pueda alterar la interpretación del descenso de nivel."),
    criterio("criterio-impermeabilizacion-prueba-observar-inferior", "Área sometida a prueba", "Inspección de caras", "Revisar cielorrasos, muros, juntas y ambientes inferiores o colindantes durante y después del ensayo."),
    criterio("criterio-impermeabilizacion-prueba-no-sobrecargar", "Losa o cubierta", "Carga de agua", "No acumular una altura de agua que exceda la carga prevista por la estructura o el procedimiento de prueba."),
    criterio("criterio-impermeabilizacion-defecto-reparar-reensayar", "Membrana con defecto", "Reparación y reprueba", "Preparar el área, ejecutar el parche con traslape compatible y repetir el ensayo del sector afectado."),
    criterio("criterio-impermeabilizacion-inspeccion-antes-proteger", "Membrana terminada", "Inspección previa", "Inspeccionar continuidad, remates, drenajes, juntas y penetraciones antes de colocar mortero, enchape o capa protectora."),
    criterio("criterio-impermeabilizacion-registro-fotografico", "Trabajo oculto", "Evidencia", "Fotografiar soporte, refuerzos, penetraciones, remates y pruebas antes de cubrirlos."),
    criterio("criterio-impermeabilizacion-registro-productos", "Control de calidad", "Trazabilidad", "Registrar producto, lote, consumo, superficie, condiciones ambientales, aplicador, fecha y resultado de pruebas."),

    # Protección y entrega
    criterio("criterio-impermeabilizacion-proteger-transito", "Membrana fresca", "Restricción de tránsito", "Delimitar el área y evitar tránsito, herramientas, escaleras y almacenamiento hasta alcanzar el curado y protección requeridos."),
    criterio("criterio-impermeabilizacion-oficios-posteriores", "Membrana protegida", "Control de otros oficios", "Informar la ubicación del sistema y supervisar instalaciones posteriores para evitar cortes, quemaduras y perforaciones."),
    criterio("criterio-impermeabilizacion-drenes-proteger-residuos", "Sumideros y canaletas durante obra", "Protección temporal", "Evitar el ingreso de mortero, fragua, pintura, empaques y residuos sin sellar permanentemente los drenajes."),
    criterio("criterio-impermeabilizacion-limpieza-compatible", "Membrana expuesta", "Limpieza", "Usar herramientas y productos que no corten, ablanden ni degraden la superficie impermeable."),
    criterio("criterio-impermeabilizacion-residuo-no-desague", "Residuos de aplicación", "Disposición", "No verter imprimantes, resinas, solventes, lechadas o restos de recubrimiento en sumideros o redes sanitarias."),
    criterio("criterio-impermeabilizacion-entrega-garantia", "Sistema terminado", "Documentación de entrega", "Entregar fichas, garantía, planos o croquis, zonas reparadas, resultados de pruebas y restricciones de mantenimiento."),

    # Diagnóstico, salitre, condensación y reparación
    criterio("criterio-humedad-salitre-no-pintar", "Muro con salitre", "Reparación superficial", "No lijar y pintar como única solución; primero detener la fuente de humedad y luego retirar y tratar las sales y materiales degradados."),
    criterio("criterio-humedad-capilaridad-diagnosticar", "Muro húmedo desde el piso", "Capilaridad", "Confirmar el patrón, fuente de agua, continuidad de barreras y sales antes de proponer inyección química, zócalo impermeable o drenaje."),
    criterio("criterio-humedad-capilaridad-no-encerrar", "Muro con humedad ascendente", "Revestimiento impermeable interior", "No encerrar la humedad con un revestimiento poco permeable sin evaluar hacia dónde migrará el agua y las sales."),
    criterio("criterio-humedad-condensacion-diferenciar", "Mancha o moho", "Condensación o filtración", "Relacionar la aparición con lluvia, uso del baño, temperatura, ventilación y superficie fría para diferenciar condensación de ingreso de agua."),
    criterio("criterio-humedad-condensacion-corregir-causa", "Ambiente con condensación", "Control ambiental", "Mejorar ventilación, extracción, aislamiento o puente térmico según el diagnóstico, en lugar de cubrir repetidamente la mancha."),
    criterio("criterio-humedad-moho-proteccion", "Superficie con moho", "Limpieza segura", "Eliminar la fuente de humedad, ventilar y limpiar con protección personal y procedimiento compatible; retirar materiales porosos que hayan perdido integridad."),
    criterio("criterio-humedad-fuga-sectorizar", "Filtración de origen incierto", "Pruebas por sectores", "Ensayar sucesivamente tuberías, juntas, cubierta, fachada y drenajes para localizar la causa antes de demoler extensamente."),
    criterio("criterio-humedad-trazado-agua", "Filtración", "Recorrido del agua", "Considerar que la mancha interior puede aparecer lejos del punto de ingreso debido a pendientes, juntas, vacíos y capilaridad."),
    criterio("criterio-humedad-inyeccion-fisura-evaluar", "Fisura con ingreso de agua", "Inyección", "Elegir resina o lechada según humedad, apertura, movimiento y función estructural; no inyectar sin conocer el comportamiento de la fisura."),
    criterio("criterio-humedad-parche-compatible", "Reparación localizada", "Compatibilidad del parche", "Preparar bordes y usar un material compatible en adherencia, rigidez, permeabilidad y movimiento con el soporte existente."),
    criterio("criterio-humedad-reparacion-no-desviar", "Ingreso de agua", "Efecto de la reparación", "Verificar que el sellado no desvíe el agua hacia otro ambiente, junta, instalación o propiedad vecina."),
    criterio("criterio-humedad-secado-antes-acabado", "Elemento reparado", "Secado", "Permitir el secado y comprobar la condición del soporte antes de tarrajear, empastar, pintar o colocar revestimientos sensibles."),
    criterio("criterio-humedad-eflorescencia-retirar-seco", "Superficie con sales", "Retiro de eflorescencia", "Retirar sales sueltas con el método compatible después de controlar la humedad y evitar lavados que vuelvan a disolverlas dentro del muro."),
    criterio("criterio-humedad-corrosion-evaluar", "Concreto con humedad y óxido", "Corrosión del refuerzo", "Evaluar desprendimientos, profundidad de carbonatación o cloruros y pérdida de sección antes de limitarse a resanar el acabado."),

    # Mantenimiento preventivo
    criterio("criterio-mantenimiento-cubierta-inspeccion-periodica", "Techo o azotea", "Inspección", "Revisar periódicamente membranas, juntas, remates, penetraciones, bases de equipos y zonas reparadas, especialmente antes de lluvias."),
    criterio("criterio-mantenimiento-drenes-limpieza", "Canaletas y sumideros", "Limpieza preventiva", "Retirar hojas, polvo, nidos y residuos sin dañar rejillas, sellos o membranas."),
    criterio("criterio-mantenimiento-sellantes-renovar", "Juntas y sellos exteriores", "Renovación", "Revisar pérdida de adherencia, endurecimiento, fisuras y desprendimiento y renovar el sellante con preparación completa de la junta."),
    criterio("criterio-mantenimiento-no-perforar-techo", "Azotea impermeabilizada", "Nuevas instalaciones", "Consultar los detalles existentes antes de instalar antenas, tendales, paneles, tanques o equipos que requieran fijación."),
    criterio("criterio-mantenimiento-jardinera-dren", "Jardinera impermeabilizada", "Control del drenaje", "Revisar rebose, salida, raíces y asentamiento del sustrato para evitar presión de agua y daño oculto."),
    criterio("criterio-mantenimiento-cisterna-inspeccion", "Cisterna", "Inspección interior", "Durante la limpieza programada revisar juntas, fisuras, revestimiento, pasamuros, tapa y signos de pérdida de estanqueidad."),
]


def main() -> None:
    base = json.loads(NORMATIVA.read_text(encoding="utf-8"))
    banco = json.loads(PREGUNTAS.read_text(encoding="utf-8"))
    if base.get("version") != "2.7.0" or len(base.get("parametros", [])) != 1680:
        raise SystemExit("La rama no parte de la versión 2.7.0 esperada.")

    ids_nuevos = [item["id"] for item in REGISTROS]
    if len(ids_nuevos) != len(set(ids_nuevos)):
        raise SystemExit("El inventario contiene identificadores duplicados.")
    ids_existentes = {item["id"] for item in base["parametros"]}
    repetidos = sorted(ids_existentes.intersection(ids_nuevos))
    if repetidos:
        raise SystemExit("Parámetros ya existentes: " + ", ".join(repetidos))

    todas_preguntas = [
        item
        for categoria in banco.get("categorias", [])
        for item in categoria.get("preguntas", [])
        if isinstance(item, dict)
    ]
    max_q = max(int(item["id"][1:]) for item in todas_preguntas if re.fullmatch(r"q\d+", item.get("id", "")))
    categoria = next(
        (c for c in banco["categorias"] if c["nombre"] == "Impermeabilización, Humedad y Drenaje"),
        None,
    )
    if categoria is None:
        categoria = {"nombre": "Impermeabilización, Humedad y Drenaje", "preguntas": []}
        banco["categorias"].append(categoria)

    for numero, registro in enumerate(REGISTROS, start=1):
        qid = f"q{max_q + numero}"
        parametro = {k: v for k, v in registro.items() if k not in {"pregunta", "respuesta"}}
        parametro["faq_relacionadas"] = [qid]
        base["parametros"].append(parametro)
        categoria["preguntas"].append({
            "id": qid,
            "pregunta": registro["pregunta"],
            "respuesta": registro["respuesta"],
        })

    cantidad = len(REGISTROS)
    base["version"] = "2.8.0"
    base["fecha_revision"] = "2026-07-27"

    total_parametros = len(base["parametros"])
    total_preguntas = sum(len(c.get("preguntas", [])) for c in banco["categorias"])
    total_validados = sum(item.get("estado_revision") == "validado_con_numeral" for item in base["parametros"])
    total_criterios = sum(item.get("estado_revision") == "criterio_tecnico_revisado" for item in base["parametros"])
    esperados = (1680 + cantidad, 3143 + cantidad, 1245, 417 + cantidad)
    recibidos = (total_parametros, total_preguntas, total_validados, total_criterios)
    if recibidos != esperados:
        raise SystemExit(f"Totales inesperados: {recibidos}; esperados: {esperados}")

    ids_finales = [item["id"] for item in base["parametros"]]
    preguntas_finales = [
        item["id"]
        for c in banco["categorias"]
        for item in c.get("preguntas", [])
        if isinstance(item, dict)
    ]
    if len(ids_finales) != len(set(ids_finales)) or len(preguntas_finales) != len(set(preguntas_finales)):
        raise SystemExit("La ampliación produjo identificadores duplicados.")

    NORMATIVA.write_text(json.dumps(base, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    PREGUNTAS.write_text(json.dumps(banco, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    check = CHECK.read_text(encoding="utf-8")
    check = rep(check, "if len(base.parametros) < 1680:", f"if len(base.parametros) < {total_parametros}:")
    check = rep(check, "por lo menos 1680 parámetros revisados", f"por lo menos {total_parametros} parámetros revisados")
    check = rep(check, 'if base.version != "2.7.0":', 'if base.version != "2.8.0":')
    check = rep(check, "La versión normativa esperada es 2.7.0", "La versión normativa esperada es 2.8.0")
    check = rep(check, "if criterios < 417:", f"if criterios < {total_criterios}:")
    check = rep(check, "al menos 417 criterios técnicos revisados", f"al menos {total_criterios} criterios técnicos revisados")
    check = rep(check, "if len(todas) < 3143:", f"if len(todas) < {total_preguntas}:")
    check = rep(check, "por lo menos 3143 preguntas técnicas", f"por lo menos {total_preguntas} preguntas técnicas")

    pruebas = '''
    impermeabilizacion_prueba = api.detalle_parametro_normativo("criterio-impermeabilizacion-prueba-nivel-registro")
    if impermeabilizacion_prueba["estado_revision"] != "criterio_tecnico_revisado":
        raise SystemExit("La prueba de inundación debe conservarse como criterio técnico revisado.")

    impermeabilizacion_salitre = api.detalle_parametro_normativo("criterio-humedad-salitre-no-pintar")
    if "fuente de humedad" not in impermeabilizacion_salitre["valor"]["texto"]:
        raise SystemExit("El tratamiento de salitre debe exigir corregir la fuente de humedad.")

    impermeabilizacion_techo = api.detalle_parametro_normativo("criterio-cubierta-penetracion-refuerzo-sello")
    if impermeabilizacion_techo["fuente"]["tipo"] != "criterio_tecnico":
        raise SystemExit("El sellado de penetraciones debe conservar fuente de criterio técnico.")

    impermeabilizacion_cisterna = api.detalle_parametro_normativo("criterio-cisterna-revestimiento-agua-potable")
    if "agua potable" not in impermeabilizacion_cisterna["valor"]["texto"]:
        raise SystemExit("El revestimiento de cisterna debe conservar compatibilidad con agua potable.")

'''
    check = rep(check, "    preguntas = json.loads(\n", pruebas + "    preguntas = json.loads(\n")
    CHECK.write_text(check, encoding="utf-8")

    DOC.write_text(
        f"""# Validación de impermeabilización y tratamiento de humedad — 27 de julio de 2026

## Alcance

Se incorporaron **{cantidad} parámetros** y **{cantidad} preguntas** después de depurar **371 parámetros relacionados** de la versión 2.7.0.

## Contenido

- diagnóstico de lluvia, fugas, capilaridad, presión de terreno y condensación;
- preparación del soporte, fisuras, poros, pendientes, medias cañas e imprimación;
- juntas, cambios de material, penetraciones, sumideros, umbrales y remates;
- mezcla, capas, consumo, espesor, mallas, traslapes y defectos de aplicación;
- azoteas, terrazas, parapetos, equipos, protección UV, reboses y mantenimiento;
- baños, duchas, nichos, sardineles, griferías y drenajes;
- jardineras, cisternas, muros enterrados y drenaje perimetral;
- pruebas de inundación e hidrostáticas, registros, repruebas y protección;
- salitre, eflorescencia, moho, corrosión y reparación de filtraciones.

## Resultado

- Versión normativa: `2.8.0`.
- Parámetros totales: `{total_parametros}`.
- Registros `validado_con_numeral`: `{total_validados}`.
- Criterios técnicos revisados: `{total_criterios}`.
- Preguntas técnicas: `{total_preguntas}`.

## Criterios editoriales

- Se conservaron sin duplicar los requisitos existentes de A.010, A.020, CE.040, IS.010, EM.080, EM.110 y GE.040.
- La impermeabilidad de cisternas y tanques ya estaba validada en IS.010 2.4.g y no se repitió como un nuevo mínimo.
- No se fijaron espesores, tiempos, alturas de retorno, pendientes o consumos universales cuando dependen del producto, exposición y proyecto.
- Las prácticas de ejecución, prueba, diagnóstico y mantenimiento se identifican como `criterio_tecnico_revisado`.
- La información no sustituye el diagnóstico del origen, el diseño del sistema, las fichas técnicas ni la supervisión profesional.
""",
        encoding="utf-8",
    )

    print(f"Aplicados {cantidad} parámetros y preguntas; versión 2.8.0")


if __name__ == "__main__":
    main()
