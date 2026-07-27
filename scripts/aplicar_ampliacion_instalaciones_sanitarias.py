from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
NORMATIVA = BACKEND / "normativa_tecnica.json"
PREGUNTAS = BACKEND / "preguntas_tecnicas.json"
CHECK = ROOT / "scripts" / "check_normativa.py"
DOC = ROOT / "docs" / "VALIDACION_INSTALACIONES_SANITARIAS_2026-07-27.md"
FECHA = "2026-07-27"
URL_IS010 = "https://www.gob.pe/institucion/vivienda/informes-publicaciones/2309793-reglamento-nacional-de-edificaciones-rne"
URL_SENCICO = "https://www.gob.pe/institucion/sencico/informes-publicaciones/2879107-instalaciones-sanitarias-en-edificaciones"


def valor_texto(texto: str) -> dict:
    return {"tipo": "texto", "valor": None, "minimo": None, "maximo": None, "unidad": None, "formula": None, "texto": texto}


def valor_numero(valor: float, unidad: str, texto: str) -> dict:
    return {"tipo": "numero", "valor": valor, "minimo": None, "maximo": None, "unidad": unidad, "formula": None, "texto": texto}


def valor_rango(minimo: float, maximo: float, unidad: str, texto: str) -> dict:
    return {"tipo": "rango", "valor": None, "minimo": minimo, "maximo": maximo, "unidad": unidad, "formula": None, "texto": texto}


def norma(id_: str, elemento: str, parametro: str, clasificacion: str, valor: dict, numeral: str, pregunta: str, respuesta: str, condiciones: list[str] | None = None, advertencia: str = "Debe verificarse en planos y ejecutarse bajo dirección técnica competente.") -> dict:
    return {
        "id": id_, "categoria": "Instalaciones sanitarias en ejecución", "elemento": elemento,
        "parametro": parametro, "clasificacion": clasificacion, "valor": valor,
        "condiciones": condiciones or [],
        "fuente": {"tipo": "RNE", "norma": "IS.010", "denominacion": "Instalaciones sanitarias para edificaciones", "dispositivo": "DS N.° 017-2012-VIVIENDA y modificatorias", "numeral": numeral, "numeral_confirmado": True, "url_oficial": URL_IS010},
        "estado_revision": "validado_con_numeral", "advertencia": advertencia,
        "faq_relacionadas": [], "fecha_revision": FECHA,
        "faq_categoria": "Instalaciones sanitarias en obra", "pregunta": pregunta, "respuesta": respuesta,
    }


def criterio(id_: str, elemento: str, parametro: str, pregunta: str, respuesta: str, condiciones: list[str] | None = None, advertencia: str = "La forma exacta de ejecución depende de los planos, el material y las instrucciones del fabricante.") -> dict:
    return {
        "id": id_, "categoria": "Ejecución y control de instalaciones sanitarias", "elemento": elemento,
        "parametro": parametro, "clasificacion": "recomendacion", "valor": valor_texto(respuesta),
        "condiciones": condiciones or [],
        "fuente": {"tipo": "criterio_tecnico", "norma": "Formación técnica SENCICO", "denominacion": "Instalaciones sanitarias en edificaciones", "dispositivo": None, "numeral": None, "numeral_confirmado": False, "url_oficial": None},
        "estado_revision": "criterio_tecnico_revisado", "advertencia": advertencia,
        "faq_relacionadas": [], "fecha_revision": FECHA,
        "faq_categoria": "Instalaciones sanitarias en obra", "pregunta": pregunta, "respuesta": respuesta,
    }


def inventario() -> list[dict]:
    r: list[dict] = []
    r += [
        norma("is010-ejecucion-proyecto-ingeniero-sanitario", "Proyecto sanitario", "Responsable del diseño", "condicion_normativa", valor_texto("El diseño debe ser elaborado y autorizado por un ingeniero sanitario colegiado."), "1.2.b", "¿Quién debe diseñar y autorizar las instalaciones sanitarias?", "La Norma IS.010 exige que el diseño sea elaborado y autorizado por un ingeniero sanitario colegiado."),
        norma("is010-ejecucion-coordinacion-especialidades", "Proyecto sanitario", "Coordinación con especialidades", "condicion_normativa", valor_texto("El diseño sanitario debe coordinarse con arquitectura, estructuras y demás instalaciones."), "1.2.c", "¿Las tuberías sanitarias pueden definirse sin coordinar con estructuras y arquitectura?", "No. El diseño sanitario debe coordinarse con las demás especialidades para evitar interferencias, perforaciones indebidas y recorridos incompatibles."),
        norma("is010-documentacion-memoria-planos", "Expediente sanitario", "Documentación mínima", "condicion_normativa", valor_texto("Debe incluir memoria descriptiva y planos de los sistemas previstos."), "1.3", "¿Qué documentos deben existir antes de ejecutar las instalaciones sanitarias?", "Como mínimo deben existir memoria descriptiva y planos de agua, desagüe, ventilación y los demás sistemas exigibles al proyecto."),
        norma("is010-deposito-preservar-calidad-agua", "Cisterna o tanque", "Protección de la calidad del agua", "condicion_normativa", valor_texto("Los depósitos deben diseñarse y construirse preservando la calidad del agua."), "2.4.a", "¿Una cisterna puede construirse sin medidas para proteger la calidad del agua?", "No. El depósito debe impedir contaminación, ingreso de suciedad y condiciones que deterioren el agua almacenada."),
        norma("is010-deposito-obligatorio-abastecimiento-discontinuo", "Almacenamiento de agua", "Obligación por discontinuidad o baja presión", "condicion_normativa", valor_texto("Se requiere almacenamiento cuando el abastecimiento público no es continuo o carece de presión suficiente."), "2.4.b", "¿Cuándo es obligatorio prever cisterna o tanque?", "Cuando el servicio público no es continuo o no tiene presión suficiente para abastecer adecuadamente todos los aparatos previstos."),
        norma("is010-deposito-material-resistente-impermeable", "Cisterna o tanque", "Material y paredes", "condicion_normativa", valor_texto("El depósito debe ser resistente, con paredes impermeabilizadas y dispositivos de operación y mantenimiento."), "2.4.g", "¿Cómo deben ser las paredes de una cisterna o tanque?", "Deben ser resistentes e impermeabilizadas, y el depósito debe permitir operación, limpieza y mantenimiento adecuados."),
        norma("is010-deposito-entrada-techo-separacion-minima", "Cisterna o tanque", "Separación entre techo y eje de entrada", "minimo_normativo", valor_numero(0.20, "m", "La distancia vertical no puede ser menor de 0.20 m."), "2.4.i", "¿Cuál es la separación vertical mínima entre el techo del depósito y el eje de entrada de agua?", "No puede ser menor de 0.20 m; además debe considerar el diámetro y el dispositivo de control."),
        norma("is010-deposito-rebose-entrada-separacion", "Cisterna o tanque", "Separación entre rebose y entrada", "minimo_normativo", valor_numero(0.15, "m", "Debe ser dos veces el diámetro del rebose y nunca menor de 0.15 m."), "2.4.j", "¿Qué separación debe haber entre los ejes del rebose y la entrada de agua?", "Debe ser igual al doble del diámetro del rebose y, en ningún caso, menor de 0.15 m."),
        norma("is010-deposito-rebose-nivel-maximo-separacion", "Cisterna o tanque", "Separación entre rebose y nivel máximo", "minimo_normativo", valor_numero(0.10, "m", "Debe ser igual al diámetro del rebose y nunca menor de 0.10 m."), "2.4.k", "¿Qué distancia debe quedar entre el rebose y el nivel máximo de agua?", "Debe ser igual al diámetro del tubo de rebose y nunca inferior a 0.10 m."),
        norma("is010-deposito-rebose-brecha-aire", "Rebose de depósito", "Brecha de aire de descarga", "minimo_normativo", valor_numero(0.05, "m", "La descarga indirecta debe conservar una brecha de aire mínima de 0.05 m."), "2.4.l", "¿El rebose de una cisterna puede conectarse directamente al desagüe?", "No. Debe descargar indirectamente, dejando una brecha de aire mínima de 0.05 m sobre el punto receptor."),
        norma("is010-registro-diametro-tuberia", "Registro de desagüe", "Diámetro", "condicion_normativa", valor_texto("El registro debe tener el diámetro de la tubería; si esta supera 100 mm, el registro será como mínimo de 100 mm."), "6.2.j", "¿Qué diámetro debe tener un registro de desagüe?", "Debe ser igual al de la tubería que sirve; para tuberías mayores de 100 mm, el registro debe ser por lo menos de 100 mm."),
        norma("is010-registro-espacio-limpieza-minimo", "Registro de desagüe", "Espacio libre para limpieza", "minimo_normativo", valor_numero(0.10, "m", "Debe quedar al menos 0.10 m entre la tangente del tapón y cualquier obstáculo."), "6.2.j", "¿Cuánto espacio libre necesita un registro para poder destaparse?", "Debe quedar al menos 0.10 m entre la tangente del tapón y una pared, techo u otro elemento que dificulte la limpieza."),
        norma("is010-registro-inicio-ramal", "Ramal horizontal de desagüe", "Registro al inicio", "condicion_normativa", valor_texto("Debe colocarse un registro al comienzo de cada ramal horizontal o colector."), "6.2.j", "¿Debe haber un registro al inicio de cada ramal horizontal?", "Sí. La IS.010 exige un punto de limpieza al comienzo de cada ramal horizontal de desagüe o colector."),
        norma("is010-registro-pie-montante", "Montante de desagüe", "Registro al pie", "condicion_normativa", valor_texto("Debe existir registro al pie, salvo descarga a caja o buzón a no más de 10 m."), "6.2.j", "¿Debe colocarse un registro al pie de una montante?", "Sí, salvo que descargue a una caja de registro o buzón ubicado a no más de 10 m."),
        norma("is010-registro-cada-dos-cambios", "Conducto horizontal de desagüe", "Registro por cambios de dirección", "condicion_normativa", valor_texto("Debe colocarse un registro cada dos cambios de dirección."), "6.2.j", "¿Cuándo se necesita un registro por cambios de dirección?", "Como mínimo, cada dos cambios de dirección en los conductos horizontales de desagüe."),
        norma("is010-caja-registro-cambios-red", "Red exterior de desagüe", "Caja en cambios de trazado", "condicion_normativa", valor_texto("Se requieren cajas en cambios de dirección, pendiente, material o diámetro."), "6.2.k", "¿Dónde deben colocarse cajas de registro en la red exterior?", "En todo cambio de dirección, pendiente, material o diámetro, además del espaciamiento máximo aplicable en tramos rectos."),
        norma("is010-sello-agua-rango", "Trampa o sifón", "Altura del sello de agua", "condicion_normativa", valor_rango(0.05, 0.10, "m", "El sello de agua debe estar entre 0.05 m y 0.10 m."), "6.2.i", "¿Qué altura debe tener el sello hidráulico de una trampa?", "Debe ser como mínimo 0.05 m y como máximo 0.10 m."),
        norma("is010-ventilacion-pendiente-minima", "Tubería de ventilación", "Pendiente", "minimo_normativo", valor_numero(1, "%", "La pendiente debe ser uniforme y no menor de 1% hacia un desagüe o montante."), "6.5.a", "¿La tubería horizontal de ventilación debe tener pendiente?", "Sí. Debe mantener una pendiente uniforme no menor de 1% para evacuar la condensación hacia un conducto de desagüe o montante."),
        norma("is010-ventilacion-montante-sin-reducir-diametro", "Montante de desagüe", "Prolongación al exterior", "prohibicion", valor_texto("La montante debe prolongarse al exterior sin disminuir su diámetro."), "6.5.f", "¿Se puede reducir el diámetro de la montante al convertirla en ventilación sobre el último piso?", "No. La montante debe prolongarse al exterior sin disminuir su diámetro."),
        norma("is010-ventilacion-abertura-distancia-horizontal", "Terminal de ventilación", "Distancia a abertura", "condicion_normativa", valor_numero(3, "m", "Si está a menos de 3 m horizontalmente de una abertura, debe elevarse sobre ella."), "6.5.f", "¿Qué ocurre si la ventilación termina cerca de una ventana o puerta?", "Si la boca queda a menos de 3 m horizontalmente, el extremo debe quedar por encima de la abertura conforme al desnivel normativo."),
        norma("is010-ventilacion-individual-mitad-desague", "Ventilación individual", "Relación con el desagüe", "formula_normativa", {"tipo":"formula","valor":None,"minimo":None,"maximo":None,"unidad":None,"formula":"Dvent = 0.5 × Ddesagüe, con mínimo de 50 mm","texto":"El diámetro de ventilación individual es la mitad del desagüe y no menor de 50 mm."}, "6.5.k", "¿Cómo se determina el diámetro de una ventilación individual?", "Debe ser igual a la mitad del diámetro del conducto de desagüe que ventila y nunca menor de 50 mm."),
    ]

    criterios = [
        ("criterio-sanitaria-probar-antes-tapar", "Tuberías empotradas", "Prueba previa al tapado", "¿Debo probar las tuberías antes de tarrajear o cerrar el piso?", "Sí. Las redes deben probarse por tramos antes de quedar ocultas; taparlas sin ensayo convierte cualquier fuga en una reparación destructiva."),
        ("criterio-sanitaria-tapones-prueba-seguros", "Prueba de tuberías", "Tapones de ensayo", "¿Puedo probar una red usando tapones improvisados?", "No es recomendable. Utiliza tapones compatibles, firmemente asegurados y adecuados para la presión o columna de agua prevista."),
        ("criterio-sanitaria-manometro-calibrado", "Prueba de agua", "Manómetro", "¿Sirve cualquier manómetro para una prueba hidráulica?", "Debe tener rango apropiado, lectura clara y condición verificada; un instrumento defectuoso invalida la prueba."),
        ("criterio-sanitaria-prueba-por-tramos", "Red sanitaria", "Sectorización de pruebas", "¿Conviene probar toda la casa de una sola vez?", "Es más seguro probar por tramos conforme avanza la instalación y realizar luego una prueba general, dejando identificados los sectores ensayados."),
        ("criterio-sanitaria-acta-prueba", "Control de calidad", "Registro de prueba", "¿Qué debo registrar de una prueba sanitaria?", "Fecha, tramo, material, presión o nivel aplicado, duración, instrumento, resultado, correcciones, fotografías y responsable de la conformidad."),
        ("criterio-sanitaria-fotos-antes-cubrir", "Trabajo oculto", "Registro fotográfico", "¿Para qué fotografiar las tuberías antes de cubrirlas?", "Para conservar la ubicación de recorridos, uniones, válvulas y pases; esto reduce perforaciones accidentales y facilita futuras reparaciones."),
        ("criterio-sanitaria-extremos-taponados", "Tubería en obra", "Protección de extremos", "¿Se pueden dejar abiertas las tuberías mientras continúa la obra?", "No. Mantén los extremos temporalmente taponados para impedir ingreso de concreto, mortero, tierra, insectos y residuos."),
        ("criterio-sanitaria-no-echar-cemento-desague", "Red de desagüe", "Protección contra residuos", "¿Puedo lavar herramientas y botar cemento por el desagüe nuevo?", "No. Mortero, yeso, pintura y residuos pueden fraguar u obstruir la red; deben retirarse por medios independientes."),
        ("criterio-sanitaria-pvc-corte-escuadra", "Tubería PVC", "Corte", "¿Cómo debe cortarse una tubería de PVC?", "Con corte perpendicular, borde uniforme y sin deformación, usando herramienta apropiada para permitir una unión completa."),
        ("criterio-sanitaria-pvc-desbarbado", "Tubería PVC", "Desbarbado", "¿Es necesario quitar las rebabas del tubo?", "Sí. Las rebabas dificultan la inserción, retienen residuos y pueden dañar empaques o alterar la unión."),
        ("criterio-sanitaria-pvc-limpieza-union", "Unión de PVC", "Limpieza", "¿Puedo pegar PVC con polvo o humedad en la unión?", "No. Las superficies deben estar limpias y acondicionadas según el sistema de unión y la ficha del fabricante."),
        ("criterio-sanitaria-pvc-adhesivo-compatible", "Unión de PVC", "Adhesivo", "¿Cualquier pegamento sirve para tuberías sanitarias?", "No. Debe ser compatible con el material, diámetro, presión y uso de la tubería, y aplicarse dentro de su vida útil."),
        ("criterio-sanitaria-pvc-marca-insercion", "Unión de PVC", "Profundidad de inserción", "¿Cómo compruebo que el tubo entró completamente en el accesorio?", "Marca previamente la profundidad de inserción y verifica que la unión alcance esa referencia sin forzar ni retirar el tubo durante el curado inicial."),
        ("criterio-sanitaria-pvc-no-calentar-improvisado", "Tubería PVC", "Deformación por calor", "¿Puedo calentar el tubo con fuego para doblarlo o hacer una campana?", "No. El calentamiento improvisado altera el material y produce geometrías débiles; utiliza accesorios o métodos expresamente aprobados."),
        ("criterio-sanitaria-cambios-direccion-suaves", "Red de desagüe", "Cambios de dirección", "¿Conviene usar giros bruscos de 90° en desagüe horizontal?", "Deben emplearse accesorios y combinaciones que faciliten el flujo y la limpieza, respetando el plano y evitando cambios bruscos innecesarios."),
        ("criterio-sanitaria-pendiente-verificar-instrumento", "Desagüe horizontal", "Control de pendiente", "¿La pendiente puede comprobarse solo a simple vista?", "No. Debe verificarse con nivel, láser u otro instrumento apropiado antes de fijar y cubrir la tubería."),
        ("criterio-sanitaria-contrapendiente-prohibida", "Desagüe horizontal", "Contrapendiente", "¿Una pequeña contrapendiente es aceptable?", "No. Las depresiones retienen sólidos y agua; corrige la rasante y los apoyos antes del tapado."),
        ("criterio-sanitaria-soportes-no-deformar", "Tubería suspendida", "Soportes", "¿Puedo sujetar una tubería de cualquier forma?", "Los soportes deben ser compatibles, estar espaciados según material y diámetro, y no estrangular, cortar ni deformar la tubería."),
        ("criterio-sanitaria-soporte-cerca-accesorios", "Tubería suspendida", "Apoyo de accesorios", "¿Los accesorios pesados pueden quedar colgando del tubo?", "No. Válvulas, equipos y conjuntos pesados requieren soporte propio o refuerzo cercano para no cargar las uniones."),
        ("criterio-sanitaria-dilatacion-tuberias", "Tubería larga", "Dilatación", "¿Debo considerar que una tubería cambia de longitud?", "Sí. En recorridos largos o expuestos a temperatura deben respetarse holguras, anclajes y compensaciones indicadas por el sistema."),
        ("criterio-sanitaria-pases-con-manga", "Paso por muro o losa", "Manga o pasatubo", "¿Cómo debe atravesar una tubería un muro o una losa?", "El pase debe estar previsto en planos y ejecutarse con manga o detalle compatible cuando corresponda, sin picar elementos estructurales terminados."),
        ("criterio-sanitaria-no-cortar-acero", "Paso de tuberías", "Interferencia con refuerzo", "¿Puedo cortar una varilla para que pase la tubería?", "No. No se corta ni desplaza acero estructural sin autorización y detalle del proyectista de estructuras."),
        ("criterio-sanitaria-sellar-pasamuros", "Paso de tuberías", "Sellado", "¿Los huecos alrededor de la tubería pueden quedar abiertos?", "No. Deben sellarse con un sistema compatible con movimiento, humedad, acústica y resistencia al fuego cuando sea exigible."),
        ("criterio-sanitaria-proteger-tuberia-concreto", "Tubería embebida", "Protección durante vaciado", "¿Cómo evito que una tubería se mueva durante el vaciado?", "Debe fijarse, protegerse y revisarse antes y durante el vaciado, evitando aplastamientos, flotación y pérdida de pendiente."),
        ("criterio-sanitaria-cama-tuberia-enterrada", "Tubería enterrada", "Cama de apoyo", "¿Puede apoyarse una tubería enterrada sobre piedras o escombros?", "No. Requiere apoyo continuo con material apropiado, sin elementos punzantes y con conformación que no fuerce las uniones."),
        ("criterio-sanitaria-relleno-lateral-uniforme", "Tubería enterrada", "Relleno lateral", "¿Cómo debe rellenarse alrededor de una tubería enterrada?", "De manera uniforme a ambos lados, con material seleccionado y compactación controlada que no desplace ni dañe el tubo."),
        ("criterio-sanitaria-no-compactar-directo-tubo", "Tubería enterrada", "Compactación", "¿Puedo compactar directamente sobre el tubo recién instalado?", "No. Primero debe alcanzar la cobertura protectora especificada; el equipo y energía de compactación deben ser compatibles con el sistema."),
        ("criterio-sanitaria-valvulas-accesibles", "Válvulas de agua", "Accesibilidad", "¿Una válvula puede quedar enterrada dentro del muro sin registro?", "No. Debe quedar identificable y accesible para operación, mantenimiento o reemplazo."),
        ("criterio-sanitaria-valvula-no-soportar-tuberia", "Válvula", "Soporte", "¿La válvula puede sostenerse solo por las tuberías?", "Los conjuntos pesados o sometidos a maniobra deben tener apoyo adecuado para no transmitir esfuerzos perjudiciales a las uniones."),
        ("criterio-sanitaria-purgar-red-agua", "Red de agua", "Purga", "¿Qué se hace después de montar y probar la red de agua?", "Debe purgarse y enjuagarse hasta retirar aire, partículas y residuos antes de conectar o habilitar los aparatos."),
        ("criterio-sanitaria-desinfectar-almacenamiento", "Cisterna o tanque", "Desinfección", "¿Una cisterna nueva puede llenarse y usarse de inmediato?", "Debe limpiarse y desinfectarse mediante procedimiento apropiado antes de ponerse en servicio y después de intervenciones contaminantes."),
        ("criterio-sanitaria-tapa-cisterna-hermetica", "Cisterna", "Tapa de inspección", "¿La tapa de cisterna puede permitir ingreso de polvo o insectos?", "No. Debe ser resistente, segura, ajustada y permitir inspección sin facilitar contaminación."),
        ("criterio-sanitaria-acceso-limpieza-deposito", "Cisterna o tanque", "Acceso de mantenimiento", "¿El depósito necesita acceso para limpieza?", "Sí. El diseño debe permitir inspección, limpieza, desinfección y reparación en condiciones seguras."),
        ("criterio-sanitaria-rebose-visible", "Rebose de depósito", "Detección de falla", "¿Conviene ocultar completamente la descarga del rebose?", "No. Debe disponerse de forma que una falla de la válvula de ingreso sea detectable y no contamine el agua ni dañe la edificación."),
        ("criterio-sanitaria-bomba-base-firme", "Equipo de bombeo", "Base", "¿La bomba puede instalarse directamente sobre un piso irregular?", "Debe montarse sobre una base firme, nivelada y compatible con el equipo, controlando vibraciones y permitiendo mantenimiento."),
        ("criterio-sanitaria-bomba-uniones-desmontables", "Equipo de bombeo", "Mantenimiento", "¿Cómo facilito el reemplazo de una bomba?", "Instala válvulas, uniones desmontables y espacio de maniobra según el diseño, sin obligar a cortar la red para retirarla."),
        ("criterio-sanitaria-bomba-no-trabajar-seco", "Equipo de bombeo", "Protección", "¿Una electrobomba puede funcionar sin agua?", "No, salvo que el fabricante lo permita expresamente. Debe protegerse contra trabajo en seco, sobrepresión y condiciones eléctricas inseguras."),
        ("criterio-sanitaria-ventilacion-no-taponar", "Ventilación sanitaria", "Continuidad", "¿Puedo tapar una ventilación porque produce olor durante la obra?", "No. Debe corregirse la causa del olor y mantener la ventilación continua; taponarla rompe la protección de los sellos hidráulicos."),
        ("criterio-sanitaria-terminal-ventilacion-libre", "Terminal de ventilación", "Área libre", "¿Se puede colocar una malla muy cerrada en la ventilación?", "La protección no debe reducir indebidamente el área libre ni favorecer obstrucciones; debe ser compatible con el diseño y mantenerse limpia."),
        ("criterio-sanitaria-trampas-con-agua", "Aparato sanitario", "Sello hidráulico", "¿Por qué aparece olor en un baño aún no usado?", "Las trampas pueden haberse secado. Mantén agua en los sellos y verifica que la ventilación y las conexiones sean correctas."),
        ("criterio-sanitaria-no-doble-trampa", "Aparato sanitario", "Trampa", "¿Es mejor colocar dos trampas seguidas para evitar olores?", "No. Una doble trampa puede generar mal funcionamiento y obstrucciones; respeta el detalle del sistema y la trampa prevista para cada aparato."),
        ("criterio-sanitaria-aparato-fijacion-firme", "Aparato sanitario", "Fijación", "¿El inodoro o lavatorio puede quedar sostenido solo por el sellador?", "No. Debe fijarse mecánicamente según el aparato y el soporte; el sellador no sustituye anclajes ni una base estable."),
        ("criterio-sanitaria-inodoro-sello-renovar", "Inodoro", "Sello de descarga", "¿Puedo reutilizar el sello del inodoro al desmontarlo?", "Debe evaluarse y normalmente reemplazarse por uno compatible para asegurar estanqueidad y correcta alineación."),
        ("criterio-sanitaria-flexibles-no-empotrados", "Conexión de aparato", "Tubo flexible", "¿Un tubo flexible de abasto puede quedar empotrado?", "No debe ocultarse como sustituto permanente de la tubería fija; debe quedar accesible, sin torsión y dentro de su uso previsto."),
        ("criterio-sanitaria-prueba-descarga-simultanea", "Recepción sanitaria", "Prueba funcional", "¿Basta con revisar que no haya fugas estáticas?", "No. También conviene probar descargas y consumos simultáneos para verificar evacuación, presión, ruidos anormales y conservación de sellos."),
        ("criterio-sanitaria-verificar-registros-accesibles", "Recepción sanitaria", "Accesibilidad de registros", "¿Qué debe revisarse antes de entregar la instalación?", "Que todos los registros, válvulas, bombas y tapas sean accesibles, identificables y operables sin demoler acabados."),
        ("criterio-sanitaria-plano-conforme-obra", "Recepción sanitaria", "Plano conforme a obra", "¿Es útil actualizar el plano después de instalar?", "Sí. Debe registrar cambios autorizados, cotas, válvulas, cajas y recorridos ocultos para mantenimiento futuro."),
        ("criterio-sanitaria-etiquetar-valvulas", "Red de agua", "Identificación", "¿Conviene identificar las válvulas?", "Sí. Etiqueta su función y sector atendido para aislar rápidamente una fuga o realizar mantenimiento."),
        ("criterio-sanitaria-proteger-aparatos-obra", "Aparatos instalados", "Protección", "¿Los aparatos pueden quedar expuestos mientras siguen los acabados?", "Deben protegerse contra golpes, pintura, mortero y uso prematuro, sin bloquear las inspecciones necesarias."),
        ("criterio-sanitaria-limpieza-final-red", "Recepción sanitaria", "Limpieza", "¿Qué limpieza se realiza al terminar?", "Retira residuos, limpia aireadores y trampas accesibles, enjuaga redes y verifica que cada aparato drene sin obstrucciones."),
    ]
    r += [criterio(*x) for x in criterios]
    return r


def reemplazar_patron(texto: str, patron: str, reemplazo: str) -> str:
    nuevo, n = re.subn(patron, reemplazo, texto, count=1)
    if n != 1:
        raise SystemExit(f"No se pudo actualizar el validador: {patron}")
    return nuevo


def main() -> None:
    candidatos = inventario()
    base = json.loads(NORMATIVA.read_text(encoding="utf-8"))
    banco = json.loads(PREGUNTAS.read_text(encoding="utf-8"))
    existentes = {p["id"] for p in base["parametros"]}
    nuevos = [p for p in candidatos if p["id"] not in existentes]
    if len(nuevos) < 60:
        raise SystemExit(f"El lote neto debe conservar al menos 60 reglas nuevas; quedaron {len(nuevos)}.")

    todas = [q for c in banco["categorias"] for q in c.get("preguntas", [])]
    max_q = max(int(q["id"][1:]) for q in todas if re.fullmatch(r"q\d+", q.get("id", "")))
    categorias = {c["nombre"]: c for c in banco["categorias"]}
    for i, item in enumerate(nuevos, start=1):
        qid = f"q{max_q+i}"
        nombre = item.pop("faq_categoria")
        pregunta = item.pop("pregunta")
        respuesta = item.pop("respuesta")
        item["faq_relacionadas"] = [qid]
        base["parametros"].append(item)
        cat = categorias.get(nombre)
        if cat is None:
            cat = {"nombre": nombre, "preguntas": []}
            banco["categorias"].append(cat)
            categorias[nombre] = cat
        cat["preguntas"].append({"id": qid, "pregunta": pregunta, "respuesta": respuesta})

    base["version"] = "2.4.0"
    base["fecha_revision"] = FECHA
    total_p = len(base["parametros"])
    total_q = sum(len(c.get("preguntas", [])) for c in banco["categorias"])
    validados = sum(p["estado_revision"] == "validado_con_numeral" for p in base["parametros"])
    criterios_total = sum(p["estado_revision"] == "criterio_tecnico_revisado" for p in base["parametros"])

    if len({p["id"] for p in base["parametros"]}) != total_p:
        raise SystemExit("Se produjeron identificadores duplicados.")
    faq_ids = [q["id"] for c in banco["categorias"] for q in c.get("preguntas", [])]
    if len(set(faq_ids)) != total_q:
        raise SystemExit("Se produjeron FAQ duplicadas.")

    NORMATIVA.write_text(json.dumps(base, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    PREGUNTAS.write_text(json.dumps(banco, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    check = CHECK.read_text(encoding="utf-8")
    check = reemplazar_patron(check, r"if len\(base\.parametros\) < \d+:", f"if len(base.parametros) < {total_p}:")
    check = reemplazar_patron(check, r"por lo menos \d+ parámetros revisados", f"por lo menos {total_p} parámetros revisados")
    check = reemplazar_patron(check, r"if validados < \d+:", f"if validados < {validados}:")
    check = reemplazar_patron(check, r"al menos \d+ numerales RNE validados", f"al menos {validados} numerales RNE validados")
    check = reemplazar_patron(check, r'if base\.version != "[^"]+":', 'if base.version != "2.4.0":')
    check = reemplazar_patron(check, r"La versión normativa esperada es [0-9.]+", "La versión normativa esperada es 2.4.0")
    check = reemplazar_patron(check, r"if criterios < \d+:", f"if criterios < {criterios_total}:")
    check = reemplazar_patron(check, r"al menos \d+ criterios técnicos revisados", f"al menos {criterios_total} criterios técnicos revisados")
    check = reemplazar_patron(check, r"if len\(todas\) < \d+:", f"if len(todas) < {total_q}:")
    check = re.sub(r"La base ampliada de [^\n]+ requiere por lo menos \d+ preguntas técnicas\.", f"La base ampliada de instalaciones sanitarias requiere por lo menos {total_q} preguntas técnicas.", check, count=1)
    prueba = '''    sanitaria = api.detalle_parametro_normativo("is010-deposito-rebose-brecha-aire")
    if sanitaria["valor"]["valor"] != 0.05:
        raise SystemExit("La brecha de aire del rebose debe conservar 0.05 m.")

    registro_sanitario = api.detalle_parametro_normativo("is010-registro-espacio-limpieza-minimo")
    if registro_sanitario["valor"]["valor"] != 0.10:
        raise SystemExit("El espacio libre del registro debe conservar 0.10 m.")

'''
    check = check.replace("    preguntas = json.loads(\n", prueba + "    preguntas = json.loads(\n", 1)
    CHECK.write_text(check, encoding="utf-8")

    DOC.write_text(f"""# Validación de instalaciones sanitarias en ejecución — 27 de julio de 2026

## Alcance

Se incorporaron **{len(nuevos)} parámetros** y **{len(nuevos)} preguntas** después de depurar los 41 parámetros IS.010 existentes en la versión 2.3.0.

## Contenido

- responsabilidades, coordinación y documentación del proyecto sanitario;
- cisternas, tanques, reboses, brechas de aire y protección de la calidad del agua;
- registros, cajas, trampas, sellos hidráulicos y ventilación sanitaria;
- pruebas antes del tapado, control por tramos y registro de resultados;
- corte, unión, soporte y protección de tuberías;
- pases, empotramientos, relleno y compactación;
- montaje de válvulas, bombas y aparatos sanitarios;
- limpieza, purga, desinfección, recepción y planos conforme a obra.

## Fuentes

- Norma Técnica IS.010 Instalaciones Sanitarias para Edificaciones y su modificación aprobada por RM N.° 107-2025-VIVIENDA.
- Publicación oficial de formación técnica SENCICO sobre instalaciones sanitarias en edificaciones.

## Resultado

- Versión normativa: `2.4.0`.
- Parámetros totales: `{total_p}`.
- Registros `validado_con_numeral`: `{validados}`.
- Criterios técnicos revisados: `{criterios_total}`.
- Preguntas técnicas: `{total_q}`.

## Criterios editoriales

- Se conservaron los parámetros existentes de dotaciones, presiones, velocidades, pendientes, almacenamiento y ventilación.
- Las cifras obligatorias se limitaron a cláusulas confirmadas de IS.010.
- Las prácticas de montaje y control se identifican como `criterio_tecnico_revisado` y no como mínimos universales.
- La información no reemplaza planos, especificaciones, fichas técnicas, pruebas ni supervisión profesional.
""", encoding="utf-8")
    print(f"Ampliación aplicada: {len(nuevos)} reglas; totales {total_p} parámetros y {total_q} preguntas.")

if __name__ == "__main__":
    main()
