from __future__ import annotations

from pathlib import Path
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
NORMATIVA = BACKEND / "normativa_tecnica.json"
PREGUNTAS = BACKEND / "preguntas_tecnicas.json"
CHECK = ROOT / "scripts" / "check_normativa.py"
DOC = ROOT / "docs" / "VALIDACION_SEGURIDAD_CONSTRUCCION_2026-07-27.md"
SENCICO = "https://www.gob.pe/institucion/sencico/informes-publicaciones/2880469-seguridad-y-salud-ocupacional"
MTPE = "https://www.gob.pe/institucion/mtpe/informes-publicaciones/6911666-seguridad-y-salud-en-el-trabajo-en-el-sector-construccion"

RAW = r'''
criterio-seguridad-responsable-designado|Gestión preventiva|Responsable de seguridad|Definir antes de iniciar quién dirige la prevención y quién lo reemplaza en su ausencia.|¿Quién debe encargarse de la seguridad diaria en una obra pequeña?
criterio-seguridad-induccion-ingreso|Gestión preventiva|Inducción de ingreso|No permitir el inicio de labores sin explicar riesgos, rutas, emergencias y reglas de la obra.|¿Un trabajador puede empezar sin recibir inducción de seguridad?
criterio-seguridad-charla-inicio-jornada|Gestión preventiva|Charla previa|Realizar una charla breve antes de tareas críticas o cuando cambien las condiciones.|¿Conviene hacer una charla de seguridad antes de empezar la jornada?
criterio-seguridad-ats-tarea-no-rutinaria|Gestión preventiva|ATS|Preparar y comunicar un análisis seguro antes de actividades no rutinarias o de alto riesgo.|¿Qué se debe hacer antes de una tarea peligrosa que no es habitual?
criterio-seguridad-cambio-condiciones-detener|Gestión preventiva|Cambio de condiciones|Detener y reevaluar si cambian el clima, acceso, equipo, personal o entorno.|¿Se debe continuar si cambian las condiciones previstas del trabajo?
criterio-seguridad-permiso-altura|Gestión preventiva|Permiso de altura|Autorizar altura después de verificar acceso, protección colectiva, anclajes, rescate y competencia.|¿Basta con ponerse un arnés para empezar un trabajo en altura?
criterio-seguridad-permiso-caliente|Gestión preventiva|Permiso de trabajo en caliente|Autorizar soldadura, corte o esmerilado después de controlar combustibles, ventilación, extinción y vigilancia.|¿Qué debe revisarse antes de soldar o cortar en obra?
criterio-seguridad-permiso-confinado|Gestión preventiva|Permiso de espacio confinado|No ingresar a cisternas, pozos o espacios confinados sin evaluación atmosférica, ventilación, vigía y rescate.|¿Puedo entrar solo a limpiar una cisterna vacía?
criterio-seguridad-coordinacion-frentes|Gestión preventiva|Frentes simultáneos|Coordinar cuadrillas para evitar exposición cruzada a caídas, energía, polvo o cargas suspendidas.|¿Cómo se evita que una cuadrilla ponga en riesgo a otra?
criterio-seguridad-subcontratista-reglas|Gestión preventiva|Subcontratistas|Exigir a subcontratistas y eventuales las mismas reglas, inducciones y controles.|¿Los subcontratistas deben cumplir el mismo plan de seguridad?
criterio-seguridad-visitante-acompanado|Gestión preventiva|Visitantes|Mantener a visitantes acompañados y fuera de zonas operativas salvo autorización y protección.|¿El propietario puede recorrer solo la obra mientras trabajan?
criterio-seguridad-reporte-casi-accidente|Gestión preventiva|Casi accidente|Registrar y analizar sucesos sin lesión para corregir la causa antes de un accidente.|¿También se reporta un incidente que no lesionó a nadie?
criterio-seguridad-inspeccion-tras-incidente|Gestión preventiva|Reinicio después de incidente|No reanudar hasta inspeccionar el área, equipo y procedimiento.|¿Se puede continuar inmediatamente después de un incidente?
criterio-seguridad-registro-inspecciones|Gestión preventiva|Registro de inspecciones|Conservar observaciones, responsables, fechas y evidencias de cierre.|¿Es necesario dejar constancia de las inspecciones de seguridad?
criterio-seguridad-correctiva-responsable-plazo|Gestión preventiva|Acción correctiva|Asignar responsable y plazo y comprobar que la condición fue corregida.|¿Basta con anotar un peligro sin comprobar que se corrigió?
criterio-seguridad-clima-revision-diaria|Gestión preventiva|Revisión climática|Revisar viento, lluvia, calor y tormenta antes de altura, izaje, excavación o electricidad exterior.|¿El clima debe revisarse antes de definir las tareas del día?
criterio-seguridad-rescate-antes-trabajo|Gestión preventiva|Plan de rescate|Definir medios, personal y comunicación antes de altura o espacio confinado.|¿Cuándo debe prepararse el plan de rescate?
criterio-seguridad-contactos-emergencia-visibles|Gestión preventiva|Contactos de emergencia|Mantener visibles teléfonos y ubicación de atención médica, bomberos, policía y responsables.|¿Dónde deben estar los números de emergencia?
criterio-seguridad-epp-seleccion-riesgo|Equipo de protección personal|Selección de EPP|Seleccionar el EPP según el peligro real y no entregar el mismo equipo para toda tarea.|¿El mismo equipo de protección sirve para todos los trabajos?
criterio-seguridad-epp-inspeccion-previa|Equipo de protección personal|Inspección previa|Revisar costuras, fisuras, deformaciones, limpieza y funcionamiento antes de usar.|¿Hay que revisar el EPP todos los días?
criterio-seguridad-casco-impacto-reemplazo|Equipo de protección personal|Casco después de impacto|Retirar un casco que recibió un impacto fuerte aunque no tenga grieta visible.|¿Puedo seguir usando un casco después de que le cayó un objeto?
criterio-seguridad-casco-no-modificar|Equipo de protección personal|Modificación de casco|No perforar, pintar con productos incompatibles ni alterar la suspensión.|¿Se puede perforar el casco para ventilarlo?
criterio-seguridad-casco-barboquejo|Equipo de protección personal|Barboquejo|Usarlo cuando viento, inclinación o altura puedan hacer caer el casco.|¿Cuándo se necesita barboquejo?
criterio-seguridad-pantalla-no-reemplaza-lentes|Equipo de protección personal|Protección ocular|La pantalla facial complementa, pero no reemplaza, los lentes contra partículas.|¿La careta facial reemplaza los lentes de seguridad?
criterio-seguridad-lente-rayado-reemplazo|Equipo de protección personal|Lentes dañados|Cambiar lentes que reduzcan visión por rayaduras, opacidad o deformación.|¿Se pueden usar lentes muy rayados?
criterio-seguridad-respirador-segun-contaminante|Equipo de protección personal|Selección de respirador|Elegir respirador y filtro según polvo, humo, vapor o contaminante.|¿Una mascarilla común sirve para polvo, pintura y soldadura?
criterio-seguridad-respirador-ajuste-facial|Equipo de protección personal|Ajuste de respirador|Comprobar el sello facial y evitar barba u objetos que impidan el ajuste.|¿La barba afecta el respirador?
criterio-seguridad-filtro-reemplazo|Equipo de protección personal|Cambio de filtros|Cambiar filtros por exposición, saturación, resistencia y plazo del fabricante.|¿Cuándo se cambia el filtro de un respirador?
criterio-seguridad-protector-auditivo-seleccion|Equipo de protección personal|Protección auditiva|Seleccionar y colocar tapones u orejeras según nivel y duración del ruido.|¿Cualquier tapón protege igual contra el ruido?
criterio-seguridad-guante-rotacion-prohibido|Equipo de protección personal|Guantes y partes rotativas|No usar guantes sueltos cerca de brocas, ejes o partes que puedan atraparlos.|¿Siempre es más seguro usar guantes con un taladro?
criterio-seguridad-guante-quimico-compatible|Equipo de protección personal|Guantes químicos|Verificar compatibilidad del material del guante con el producto usado.|¿Cualquier guante de goma sirve para solventes o ácidos?
criterio-seguridad-calzado-suela-estado|Equipo de protección personal|Calzado deteriorado|Retirar calzado con suela lisa, desprendida, perforada o contaminada.|¿Cuándo debe cambiarse un zapato de seguridad?
criterio-seguridad-alta-visibilidad-transito|Equipo de protección personal|Alta visibilidad|Usar prendas visibles cerca de vehículos, maquinaria, accesos o vía pública.|¿Cuándo es necesaria la ropa reflectiva?
criterio-seguridad-epp-personal-higiene|Equipo de protección personal|EPP compartido|Asignar personalmente equipos de contacto o desinfectarlos antes de compartir.|¿Se pueden compartir respiradores entre trabajadores?
criterio-seguridad-epp-seco-almacenado|Equipo de protección personal|Almacenamiento del EPP|Guardar limpio, seco y protegido del sol, químicos y deformación.|¿Cómo debe guardarse el EPP al terminar la jornada?
criterio-seguridad-epp-no-sustituye-control|Equipo de protección personal|Jerarquía de control|No usar el EPP para omitir barandas, ventilación, aislamiento o guardas.|¿El EPP reemplaza las protecciones colectivas?
criterio-seguridad-escalera-tipo-correcto|Escaleras provisionales|Selección de escalera|Elegir tipo y longitud adecuados; no improvisar con muebles, cilindros o materiales.|¿Puedo subirme a baldes o ladrillos si no tengo escalera?
criterio-seguridad-escalera-inspeccion|Escaleras provisionales|Inspección|Revisar largueros, peldaños, zapatas, seguros y soldaduras.|¿Qué partes de una escalera deben revisarse?
criterio-seguridad-escalera-base-firme|Escaleras provisionales|Base|Apoyar sobre superficie firme, nivelada y antideslizante; no calzar con piezas sueltas.|¿Se puede nivelar una escalera con ladrillos?
criterio-seguridad-escalera-sujecion|Escaleras provisionales|Sujeción|Asegurar la parte superior o inferior cuando exista riesgo de deslizamiento.|¿Una persona sosteniendo la escalera siempre es suficiente?
criterio-seguridad-escalera-tres-puntos|Escaleras provisionales|Tres puntos de contacto|Subir y bajar de frente manteniendo tres puntos de contacto.|¿Cómo se debe subir correctamente por una escalera?
criterio-seguridad-escalera-manos-libres|Escaleras provisionales|Transporte de materiales|Usar cinturón, cuerda o izaje; no subir con objetos que ocupen las manos.|¿Puedo subir una bolsa de cemento por una escalera?
criterio-seguridad-escalera-no-peldano-superior|Escaleras provisionales|Peldaños superiores|No pararse sobre la tapa ni peldaños prohibidos por el fabricante.|¿Se puede trabajar en el último peldaño de una escalera de tijera?
criterio-seguridad-escalera-tijera-seguros|Escaleras provisionales|Escalera de tijera|Abrir completamente y bloquear separadores antes de subir.|¿Qué pasa si no abro completamente la escalera de tijera?
criterio-seguridad-escalera-no-horizontal|Escaleras provisionales|Uso indebido|No usar una escalera como puente, pasarela, plataforma o encofrado.|¿Una escalera puede usarse acostada como puente?
criterio-seguridad-escalera-no-unir|Escaleras provisionales|Extensión improvisada|No unir dos escaleras ni prolongarlas con madera o alambre.|¿Puedo amarrar dos escaleras para alcanzar más altura?
criterio-seguridad-escalera-metal-electricidad|Escaleras provisionales|Escalera metálica|No usar cerca de conductores energizados o trabajos eléctricos.|¿Es seguro usar aluminio cerca de cables?
criterio-seguridad-escalera-un-usuario|Escaleras provisionales|Ocupación|Permitir un solo usuario salvo diseño expreso para más personas.|¿Pueden subir dos personas a la misma escalera?
criterio-seguridad-escalera-no-mover-ocupada|Escaleras provisionales|Movimiento|No mover ni ajustar mientras alguien permanece encima.|¿Se puede correr una escalera con una persona arriba?
criterio-seguridad-escalera-desembarco-libre|Escaleras provisionales|Desembarco|Mantener libre y protegido el punto de llegada.|¿El desembarco puede estar ocupado con materiales?
criterio-seguridad-escalera-control-transito|Escaleras provisionales|Zona inferior|Delimitar cuando se ubique en puertas, pasillos o circulación.|¿Qué hago si la escalera queda junto a una puerta?
criterio-seguridad-escalera-retirar-defectuosa|Escaleras provisionales|Equipo defectuoso|Marcar y retirar una escalera dañada para impedir su reutilización.|¿Qué se hace con una escalera con un peldaño roto?
criterio-seguridad-andamio-base-placa|Andamios y plataformas|Base del andamio|Apoyar montantes sobre placas y base resistente.|¿El tubo del andamio puede apoyarse directamente en tierra?
criterio-seguridad-andamio-no-ladrillos|Andamios y plataformas|Nivelación|No nivelar con ladrillos, bloques huecos o retazos inestables.|¿Se puede calzar un andamio con ladrillos?
criterio-seguridad-andamio-aplomo-nivel|Andamios y plataformas|Geometría|Comprobar aplomo, nivel, escuadra y arriostramiento durante montaje.|¿Qué debe revisarse al armar un andamio?
criterio-seguridad-andamio-componentes-compatibles|Andamios y plataformas|Componentes|No mezclar piezas incompatibles, deformadas, corroídas o improvisadas.|¿Puedo combinar piezas de distintos andamios?
criterio-seguridad-andamio-plataforma-completa|Andamios y plataformas|Plataforma|Cubrir la superficie prevista sin huecos peligrosos.|¿Se puede trabajar sobre una sola tabla en el andamio?
criterio-seguridad-andamio-tabla-fijada|Andamios y plataformas|Tablones|Fijar los tablones contra desplazamiento, vuelco o levantamiento.|¿Los tablones deben quedar sujetos?
criterio-seguridad-andamio-acceso-interno|Andamios y plataformas|Acceso|Usar acceso diseñado; no trepar por crucetas o barandas.|¿Puedo subir trepando por las crucetas?
criterio-seguridad-andamio-baranda-rodapie|Andamios y plataformas|Protección lateral|Instalar barandas y rodapié donde exista riesgo de caída de personas u objetos.|¿El rodapié del andamio es realmente necesario?
criterio-seguridad-andamio-carga-distribuida|Andamios y plataformas|Carga|Distribuir materiales y evitar concentraciones o impactos.|¿Puedo acumular ladrillos en un solo punto del andamio?
criterio-seguridad-andamio-capacidad-visible|Andamios y plataformas|Capacidad|Conocer y comunicar la carga admisible del sistema.|¿Cómo sé cuánto material soporta un andamio?
criterio-seguridad-andamio-ruedas-bloqueadas|Andamios y plataformas|Andamio móvil|Bloquear todas las ruedas antes de usar.|¿Basta con frenar una sola rueda?
criterio-seguridad-andamio-no-escalera-sobre-plataforma|Andamios y plataformas|Aumento de altura|No colocar escaleras, cajas o bancos sobre la plataforma.|¿Puedo poner una escalera encima del andamio?
criterio-seguridad-andamio-separacion-muro-control|Andamios y plataformas|Separación al frente|Controlar el vacío entre plataforma y fachada o instalar protección.|¿Qué pasa si queda un espacio grande entre andamio y muro?
criterio-seguridad-andamio-anclajes-no-retirar|Andamios y plataformas|Anclajes|No retirar amarres o arriostres para facilitar el trabajo sin rediseño.|¿Se puede quitar un amarre que estorba?
criterio-seguridad-andamio-modificacion-reinspeccion|Andamios y plataformas|Reinspección|Revisar después de modificar, trasladar, golpear o exponer a viento fuerte.|¿Cuándo debe reinspeccionarse un andamio?
criterio-seguridad-andamio-etiqueta-estado|Andamios y plataformas|Estado de uso|Identificar si está habilitado, restringido o fuera de servicio.|¿Cómo se comunica que un andamio aún no está listo?
criterio-seguridad-altura-cubrir-hueco-fijado|Trabajos en altura|Hueco en piso|Cubrir con elemento resistente, fijado y marcado para que no se desplace.|¿Basta con poner una tabla suelta sobre un hueco?
criterio-seguridad-altura-baranda-no-cinta|Trabajos en altura|Borde abierto|No sustituir una baranda resistente por cinta de señalización.|¿Una cinta roja reemplaza la baranda?
criterio-seguridad-altura-anclaje-verificado|Trabajos en altura|Punto de anclaje|Usar solo puntos identificados y verificados para el sistema.|¿Puedo enganchar el arnés a cualquier fierro?
criterio-seguridad-altura-linea-independiente|Trabajos en altura|Línea de vida|Mantenerla independiente de elementos temporales cuya falla pueda causar la caída.|¿La línea de vida puede sujetarse al mismo andamio?
criterio-seguridad-altura-calcular-espacio-caida|Trabajos en altura|Distancia libre|Verificar que cuerda, absorbedor, cuerpo y deformación no permitan golpear el nivel inferior.|¿Cómo sé si hay espacio suficiente para detener una caída?
criterio-seguridad-altura-efecto-pendulo|Trabajos en altura|Anclaje lateral|Reducir desplazamiento lateral para evitar golpe por péndulo.|¿Qué es el efecto péndulo en una caída?
criterio-seguridad-altura-conectores-compatibles|Trabajos en altura|Conectores|No conectar componentes de forma que puedan abrirse o cargarse lateralmente.|¿Cualquier mosquetón sirve con cualquier anclaje?
criterio-seguridad-altura-inspeccion-arnes|Trabajos en altura|Arnés|Revisar cintas, costuras, hebillas, etiquetas y contaminación antes de usar.|¿Qué se revisa en un arnés?
criterio-seguridad-altura-retirar-tras-caida|Trabajos en altura|Equipo que detuvo una caída|Retiro|Retirar y evaluar todo componente que haya detenido una caída.|¿Se puede reutilizar un arnés después de una caída?
criterio-seguridad-altura-herramienta-amarrada|Trabajos en altura|Herramientas|Asegurar herramientas cuando puedan caer sobre personas.|¿Cómo evito que una herramienta caiga desde un techo?
criterio-seguridad-altura-zona-exclusion|Trabajos en altura|Zona inferior|Delimitar y mantener libre el área expuesta a caída de objetos.|¿Puede trabajarse debajo de otra cuadrilla?
criterio-seguridad-altura-material-borde|Trabajos en altura|Materiales en borde|No almacenar piezas sueltas junto a bordes, huecos o plataformas.|¿Puedo dejar ladrillos junto al borde de la losa?
criterio-seguridad-herramienta-inspeccion-previa|Herramientas y equipos|Herramienta|Inspeccionar carcasa, cable, interruptor, guarda y accesorio antes de usar.|¿Qué debo revisar antes de usar una herramienta eléctrica?
criterio-seguridad-herramienta-defectuosa-retirar|Herramientas y equipos|Equipo defectuoso|Desconectar, identificar y retirar; no dejar disponible para otro trabajador.|¿Qué hago con una herramienta que da corriente o vibra raro?
criterio-seguridad-herramienta-correcta|Herramientas y equipos|Selección|Usar la herramienta y accesorio previstos; no improvisar palancas, llaves o extensiones.|¿Puedo usar cualquier herramienta para salir del paso?
criterio-seguridad-esmeril-guarda|Herramientas y equipos|Esmeril angular|Guarda|No operar sin guarda correctamente posicionada.|¿Se puede retirar la guarda del esmeril para cortar mejor?
criterio-seguridad-disco-rpm-compatible|Herramientas y equipos|Disco abrasivo|Compatibilidad|Verificar diámetro, material, fecha y velocidad admisible.|¿Cualquier disco sirve para cualquier esmeril?
criterio-seguridad-disco-inspeccion|Herramientas y equipos|Disco abrasivo|Estado|No usar discos fisurados, húmedos, golpeados o deformados.|¿Se puede usar un disco con una pequeña rajadura?
criterio-seguridad-cambiar-disco-desenergizado|Herramientas y equipos|Cambio de accesorio|Energía aislada|Desconectar o retirar batería antes de cambiar disco, broca o cuchilla.|¿Basta con soltar el gatillo para cambiar el disco?
criterio-seguridad-herramienta-dos-manos|Herramientas y equipos|Herramienta de dos empuñaduras|Control|Usar las empuñaduras previstas y mantener postura estable.|¿Puedo manejar el esmeril con una sola mano?
criterio-seguridad-cable-no-reparacion-cinta|Herramientas y equipos|Cable eléctrico|Reparación|No considerar cinta aislante como reparación permanente de cable dañado.|¿Puedo seguir usando un cable reparado solo con cinta?
criterio-seguridad-extension-desenrollada|Herramientas y equipos|Extensión enrollable|Calentamiento|Desenrollar cuando la carga y fabricante lo requieran para evitar sobrecalentamiento.|¿Una extensión puede trabajar enrollada?
criterio-seguridad-enchufe-no-tirar-cable|Herramientas y equipos|Desconexión|Manipulación|Desconectar sujetando el enchufe y no jalando el cable.|¿Es correcto desconectar tirando del cable?
criterio-seguridad-manos-secas-electricidad|Herramientas y equipos|Equipo eléctrico|Humedad|No manipular enchufes o herramientas con manos mojadas o sobre agua.|¿Puedo usar un taladro con las manos húmedas?
criterio-seguridad-bloqueo-mantenimiento|Herramientas y equipos|Mantenimiento|Bloqueo|Aislar energías y evitar arranque antes de limpiar, destrabar o reparar.|¿Cómo se evita que una máquina arranque durante el mantenimiento?
criterio-seguridad-taladro-pieza-sujeta|Herramientas y equipos|Taladro|Sujeción de pieza|Fijar la pieza; no sostener material pequeño con la mano.|¿Puedo sujetar con la mano una pieza mientras la perforo?
criterio-seguridad-sierra-empujador|Herramientas y equipos|Sierra de banco|Manos alejadas|Usar guía y empujador cuando corresponda.|¿Cómo mantengo las manos lejos del disco de una sierra?
criterio-seguridad-clavadora-no-apuntar|Herramientas y equipos|Clavadora|Dirección segura|No apuntar ni apoyar contra personas aunque parezca descargada.|¿Una clavadora descargada puede apuntarse a alguien?
criterio-seguridad-manguera-aire-retencion|Herramientas y equipos|Manguera neumática|Conexión|Asegurar acoples y controlar latigazo por desconexión.|¿Qué riesgo tiene una manguera de aire que se suelta?
criterio-seguridad-compresor-valvula|Herramientas y equipos|Compresor|Dispositivos de seguridad|Mantener válvula de alivio, manómetro y drenaje operativos.|¿Se puede anular la válvula de seguridad del compresor?
criterio-seguridad-bateria-carga-ventilada|Herramientas y equipos|Carga de baterías|Ubicación|Cargar en lugar ventilado, seco y lejos de combustibles.|¿Dónde deben cargarse las baterías de herramientas?
criterio-seguridad-caliente-retirar-combustibles|Trabajo en caliente|Área de trabajo|Combustibles|Retirar o proteger madera, solventes, cartón, polvo y otros combustibles.|¿Qué debe retirarse antes de soldar?
criterio-seguridad-caliente-vigia-fuego|Trabajo en caliente|Vigilancia de fuego|Control posterior|Asignar vigía durante el trabajo y el periodo posterior definido por el riesgo.|¿Quién vigila que no quede un incendio oculto después de soldar?
criterio-seguridad-caliente-extintor-cercano|Trabajo en caliente|Extinción|Disponibilidad|Mantener extintor apropiado, accesible y sin obstrucciones.|¿Debe haber un extintor junto al trabajo en caliente?
criterio-seguridad-caliente-pantalla-chispas|Trabajo en caliente|Pantallas|Protección de terceros|Instalar barreras frente a chispas, radiación y partículas.|¿Cómo se protege a quienes trabajan cerca de una soldadura?
criterio-seguridad-caliente-ventilacion-humos|Trabajo en caliente|Humos|Ventilación|Controlar humos con ventilación o extracción antes de depender solo del respirador.|¿Abrir una ventana siempre basta para los humos de soldadura?
criterio-seguridad-cilindro-vertical-asegurado|Trabajo en caliente|Cilindro comprimido|Posición|Mantener vertical, asegurado y con protección de válvula durante traslado y almacenamiento.|¿Un cilindro puede dejarse acostado en el piso?
criterio-seguridad-cilindro-no-rodar|Trabajo en caliente|Traslado de cilindro|Manipulación|Usar carro adecuado; no arrastrar, lanzar ni rodar horizontalmente.|¿Se puede mover un balón rodándolo?
criterio-seguridad-oxigeno-sin-grasa|Trabajo en caliente|Oxígeno|Contaminación|Mantener válvulas y conexiones libres de aceite o grasa.|¿Por qué no debe ponerse grasa en conexiones de oxígeno?
criterio-seguridad-mangueras-gas-inspeccion|Trabajo en caliente|Mangueras de gas|Inspección|Revisar cortes, quemaduras, conexiones y fugas antes de usar.|¿Qué se revisa en las mangueras de oxicorte?
criterio-seguridad-arrestallama|Trabajo en caliente|Equipo de oxicorte|Retorno de llama|Usar dispositivos compatibles contra retroceso y mantenerlos operativos.|¿Para qué sirve el arrestallamas?
criterio-seguridad-cerrar-cilindros-fin|Trabajo en caliente|Fin de trabajo|Cierre|Cerrar válvulas, liberar presión según procedimiento y guardar el equipo.|¿Qué debe hacerse con los cilindros al terminar?
criterio-seguridad-izaje-plan|Izaje y maquinaria|Maniobra de izaje|Planificación|Planificar peso, centro de gravedad, ruta, radio, equipo y comunicación.|¿Qué debe conocerse antes de levantar una carga?
criterio-seguridad-izaje-eslinga-inspeccion|Izaje y maquinaria|Eslinga|Inspección|Revisar cortes, hilos rotos, deformación, corrosión, etiqueta y accesorios.|¿Qué se revisa en una eslinga?
criterio-seguridad-izaje-capacidad-legible|Izaje y maquinaria|Aparejo|Capacidad|No usar accesorios sin identificación legible de capacidad.|¿Puedo usar una eslinga sin etiqueta?
criterio-seguridad-izaje-angulo-reduce-capacidad|Izaje y maquinaria|Eslingado|Ángulo|Considerar que el ángulo modifica la tensión y capacidad.|¿El ángulo de una eslinga cambia lo que puede levantar?
criterio-seguridad-izaje-aristas-protegidas|Izaje y maquinaria|Eslinga sobre arista|Protección|Proteger contra bordes que puedan cortar o dañar.|¿Cómo se protege una eslinga de una esquina filosa?
criterio-seguridad-izaje-no-nudos|Izaje y maquinaria|Eslinga|Uso indebido|No hacer nudos ni acortar con métodos improvisados.|¿Se puede hacer un nudo para acortar una eslinga?
criterio-seguridad-izaje-gancho-seguro|Izaje y maquinaria|Gancho|Seguro|Mantener pestillo y asiento de carga operativos; no cargar la punta.|¿La carga puede apoyarse en la punta del gancho?
criterio-seguridad-izaje-sin-personas-debajo|Izaje y maquinaria|Carga suspendida|Zona de exclusión|No permitir personas debajo ni dentro de la trayectoria.|¿Puedo pasar rápidamente debajo de una carga suspendida?
criterio-seguridad-izaje-cuerda-guia|Izaje y maquinaria|Carga|Control|Usar cuerda guía cuando corresponda sin envolverla al cuerpo.|¿Cómo se controla el giro de una carga?
criterio-seguridad-izaje-prueba-baja-altura|Izaje y maquinaria|Inicio de izaje|Prueba|Elevar ligeramente para comprobar equilibrio, freno y aparejo.|¿Conviene probar la carga antes de levantarla por completo?
criterio-seguridad-izaje-senalero-unico|Izaje y maquinaria|Comunicación|Señalero|Designar un señalero; cualquiera puede ordenar parada de emergencia.|¿Cuántas personas deben dar señales al operador?
criterio-seguridad-izaje-perder-vision-detener|Izaje y maquinaria|Comunicación|Pérdida de contacto|Detener si se pierde visión o comunicación con el señalero.|¿Qué hace el operador si deja de ver al señalero?
criterio-seguridad-maquinaria-alarma-retroceso|Izaje y maquinaria|Maquinaria móvil|Retroceso|Mantener alarma, luces, espejos o cámaras operativos y usar vigía si la visibilidad es limitada.|¿Qué se necesita para retroceder con maquinaria en obra?
criterio-seguridad-maquinaria-freno-calzas|Izaje y maquinaria|Equipo estacionado|Inmovilización|Aplicar freno, bajar implementos, retirar llave y usar calzas cuando corresponda.|¿Cómo debe dejarse una máquina estacionada?
criterio-seguridad-maquinaria-no-pasajeros|Izaje y maquinaria|Maquinaria|Pasajeros|No transportar personas fuera de asientos diseñados.|¿Un trabajador puede viajar en el cucharón?
criterio-seguridad-excavacion-servicios-localizar|Excavaciones y espacios confinados|Servicios enterrados|Localización|Revisar planos, detectar y marcar servicios antes de excavar.|¿Qué debe hacerse antes de abrir una zanja?
criterio-seguridad-excavacion-inspeccion-lluvia|Excavaciones y espacios confinados|Excavación|Reinspección|Revisar después de lluvia, vibración, desprendimiento o interrupción.|¿Cuándo debe reinspeccionarse una excavación?
criterio-seguridad-excavacion-no-entrar-sin-soporte|Excavaciones y espacios confinados|Zanja inestable|Ingreso|No ingresar si talud, entibado o sistema de protección no está implementado.|¿Puedo entrar unos minutos a una zanja sin entibado?
criterio-seguridad-excavacion-suelo-cambio-detener|Excavaciones y espacios confinados|Condición del suelo|Cambio|Detener si aparecen rellenos, grietas, agua, bloques o suelo distinto al previsto.|¿Qué hago si cambia el suelo durante la excavación?
criterio-seguridad-excavacion-equipo-borde|Excavaciones y espacios confinados|Vehículo junto a borde|Control|Mantener distancia, topes y evaluación de carga sobre el borde.|¿Puede una retroexcavadora trabajar pegada al borde?
criterio-seguridad-excavacion-no-bajo-cucharon|Excavaciones y espacios confinados|Equipo de excavación|Zona de peligro|No permanecer bajo cucharón ni dentro del radio de giro.|¿Puede una persona guiar desde debajo del cucharón?
criterio-seguridad-excavacion-agua-control|Excavaciones y espacios confinados|Agua en excavación|Control|Evacuar el agua con método que no desestabilice taludes ni colindantes.|¿Basta con bombear el agua de una zanja sin revisar el suelo?
criterio-seguridad-excavacion-no-trabajo-solo|Excavaciones y espacios confinados|Personal en zanja|Vigilancia|Evitar trabajo aislado donde un colapso o atmósfera peligrosa impida pedir ayuda.|¿Es seguro trabajar solo dentro de una excavación?
criterio-seguridad-confinado-medicion-atmosfera|Excavaciones y espacios confinados|Espacio confinado|Atmósfera|Medir oxígeno y contaminantes antes y durante el ingreso según el riesgo.|¿Una cisterna vacía siempre tiene aire seguro?
criterio-seguridad-confinado-vigia-permanente|Excavaciones y espacios confinados|Espacio confinado|Vigía|Mantener vigía exterior dedicado, con comunicación y sin abandonar el puesto.|¿El vigía puede realizar otra tarea mientras alguien está dentro?
criterio-seguridad-confinado-rescate-no-ingreso|Excavaciones y espacios confinados|Rescate|Método|Priorizar rescate sin ingreso y no permitir que una persona entre impulsivamente.|¿Debe un compañero entrar de inmediato si alguien se desmaya en una cisterna?
criterio-seguridad-confinado-ventilacion-no-oxigeno|Excavaciones y espacios confinados|Ventilación|Método|No usar oxígeno puro para ventilar un espacio confinado.|¿Se puede ventilar una cisterna con oxígeno?
criterio-seguridad-encofrado-inspeccion-prevaciado|Encofrados, concreto y acero|Encofrado|Inspección previa|Verificar apoyo, puntales, arriostres, uniones, limpieza y accesos antes del vaciado.|¿Qué se revisa en el encofrado antes de vaciar?
criterio-seguridad-encofrado-no-modificar-carga|Encofrados, concreto y acero|Encofrado cargado|Modificación|No cortar, mover o retirar puntales sin autorización y secuencia definida.|¿Se puede retirar un puntal que estorba durante el vaciado?
criterio-seguridad-desencofrado-zona-exclusion|Encofrados, concreto y acero|Desencofrado|Zona de peligro|Delimitar el área y controlar caída de paneles, clavos y piezas.|¿Puede circular gente debajo durante el desencofrado?
criterio-seguridad-acero-puntas-protegidas|Encofrados, concreto y acero|Acero sobresaliente|Protección|Proteger puntas expuestas contra empalamiento y señalizarlas.|¿Cómo se protegen las varillas que sobresalen?
criterio-seguridad-acero-no-caminar-inestable|Encofrados, concreto y acero|Armadura|Acceso|No caminar sobre acero sin pasarela o estabilidad verificada.|¿Puedo caminar directamente sobre la malla de acero?
criterio-seguridad-bomba-concreto-manguera|Encofrados, concreto y acero|Manguera de bombeo|Control|Asegurar conexiones y controlar movimientos o latigazo.|¿Qué riesgo tiene la manguera de una bomba de concreto?
criterio-seguridad-concreto-contacto-piel|Encofrados, concreto y acero|Concreto fresco|Quemadura química|Evitar contacto prolongado y lavar inmediatamente la piel contaminada.|¿El concreto fresco puede quemar la piel?
criterio-seguridad-vibrador-cable|Encofrados, concreto y acero|Vibrador|Cable y manguera|Proteger conexiones y evitar jalarlas para mover o retirar el equipo.|¿Se puede sacar el vibrador jalando el cable?
criterio-seguridad-panel-encofrado-izaje|Encofrados, concreto y acero|Panel de encofrado|Manipulación|Planificar el levantamiento y evitar sujetarlo en puntos improvisados.|¿Cómo debe levantarse un panel pesado de encofrado?
criterio-seguridad-apuntalamiento-mantener|Encofrados, concreto y acero|Apuntalamiento|Permanencia|Mantener soportes y reapuntalamiento durante el tiempo y secuencia definidos.|¿Se pueden retirar todos los puntales apenas endurece la superficie?
criterio-seguridad-ruta-peaton-vehiculo-separada|Tránsito y protección de terceros|Circulación|Separación|Separar rutas peatonales y vehiculares o instalar barreras y control.|¿Peatones y maquinaria pueden usar el mismo paso?
criterio-seguridad-vigia-retroceso|Tránsito y protección de terceros|Retroceso vehicular|Vigía|Usar vigía cuando existan puntos ciegos, personas o espacio reducido.|¿Cuándo se necesita un vigía para retroceder?
criterio-seguridad-velocidad-obra|Tránsito y protección de terceros|Vehículos|Velocidad|Definir y señalizar velocidad compatible con visibilidad y condiciones.|¿Debe existir límite de velocidad dentro de la obra?
criterio-seguridad-entrega-programada|Tránsito y protección de terceros|Entrega de materiales|Coordinación|Programar ingreso, descarga y salida para evitar congestión y exposición del público.|¿Cómo se organiza la llegada de un camión de materiales?
criterio-seguridad-publico-caida-objetos|Tránsito y protección de terceros|Zona colindante|Protección|Instalar cubiertas, mallas o exclusión cuando exista caída de objetos hacia terceros.|¿Cómo se protege al peatón frente a objetos que caen?
criterio-seguridad-noche-iluminacion|Tránsito y protección de terceros|Trabajo nocturno|Iluminación|Iluminar accesos, obstáculos, excavaciones y señalización sin deslumbrar.|¿Qué debe iluminarse si se trabaja de noche?
criterio-seguridad-polvo-control-fuente|Higiene ocupacional|Polvo|Control|Priorizar humectación, captación o aislamiento antes del respirador.|¿La mascarilla es el único control contra el polvo?
criterio-seguridad-silice-no-barrer-seco|Higiene ocupacional|Polvo de sílice|Limpieza|Evitar barrido en seco o aire comprimido que vuelva a dispersar polvo fino.|¿Se debe barrer en seco el polvo de corte de concreto?
criterio-seguridad-ruido-tiempo-exposicion|Higiene ocupacional|Ruido|Exposición|Reducir tiempo, distancia y fuentes y complementar con protección auditiva.|¿Basta con usar tapones frente a ruido intenso todo el día?
criterio-seguridad-vibracion-descansos|Higiene ocupacional|Herramienta vibratoria|Exposición|Controlar tiempo de uso, mantenimiento, agarre y pausas.|¿El uso prolongado de un rotomartillo puede afectar las manos?
criterio-seguridad-calor-hidratacion|Higiene ocupacional|Calor|Prevención|Asegurar agua, sombra, pausas y vigilancia de síntomas.|¿Qué controles necesita una cuadrilla expuesta al sol?
criterio-seguridad-calor-sintomas|Higiene ocupacional|Estrés térmico|Respuesta|Detener, enfriar y pedir ayuda ante confusión, desmayo o temperatura elevada.|¿Qué hago si un trabajador se desorienta por calor?
criterio-seguridad-viento-suspender|Higiene ocupacional|Viento fuerte|Suspensión|Suspender altura, paneles o izaje cuando el viento impida control seguro.|¿Cuándo debe detenerse un trabajo por viento?
criterio-seguridad-lluvia-superficie-revisar|Higiene ocupacional|Lluvia|Reinicio|Revisar superficies resbalosas, electricidad, taludes y accesos antes de reiniciar.|¿Qué se revisa después de una lluvia?
criterio-seguridad-tormenta-electrica|Higiene ocupacional|Tormenta eléctrica|Suspensión|Alejarse de altura, estructuras metálicas y áreas abiertas según el plan de emergencia.|¿Se puede trabajar en un techo durante una tormenta eléctrica?
criterio-seguridad-derrame-limpiar-aislar|Orden y emergencias|Derrame|Respuesta|Aislar, contener y limpiar con método compatible; no dejar superficie resbalosa.|¿Qué se hace ante un derrame de aceite?
criterio-seguridad-cables-ruta-protegida|Orden y emergencias|Cables y mangueras|Trazado|Pasarlos fuera de circulación o protegerlos contra tropiezo y aplastamiento.|¿Cómo deben cruzar los cables una zona de paso?
criterio-seguridad-clavos-recipiente|Orden y emergencias|Clavos y puntas|Acopio|Retirar o doblar puntas y disponerlas en recipiente seguro.|¿Dónde se colocan clavos y fierros cortantes retirados?
criterio-seguridad-quimico-etiqueta|Orden y emergencias|Producto químico|Identificación|Mantener envase original o rotulado; no usar botellas de bebida.|¿Puedo guardar solvente en una botella de gaseosa?
criterio-seguridad-hoja-seguridad-disponible|Orden y emergencias|Producto químico|Información|Mantener ficha de seguridad accesible y explicar primeros auxilios y derrames.|¿Para qué sirve la ficha de seguridad de un producto?
criterio-seguridad-alimentos-separados-quimicos|Orden y emergencias|Alimentos|Separación|No guardar ni consumir alimentos en áreas de químicos, polvo o residuos.|¿Se puede almorzar dentro del almacén de pinturas?
criterio-seguridad-extintor-no-bloqueado|Orden y emergencias|Extintor|Acceso|Mantener visible, señalizado y sin materiales delante.|¿Puede colocarse material delante de un extintor?
criterio-seguridad-botiquin-accesible|Orden y emergencias|Botiquín|Acceso|Mantener completo, identificado y accesible; no cerrado con llave inaccesible.|¿Dónde debe estar el botiquín?
criterio-seguridad-primer-auxilio-persona-capacitada|Orden y emergencias|Primeros auxilios|Competencia|Contar con persona capacitada y medios de comunicación durante la jornada.|¿Basta con tener botiquín sin nadie que sepa usarlo?
criterio-seguridad-simulacro-actualizar|Orden y emergencias|Emergencia|Simulacro|Practicar respuestas y corregir fallas de rutas, comunicación y reunión.|¿Para qué sirve realizar un simulacro en obra?
criterio-seguridad-ruta-cambio-actualizar|Orden y emergencias|Ruta de evacuación|Actualización|Modificar señalización y comunicar cada cambio por avance de obra.|¿Qué pasa si una ruta de evacuación queda bloqueada por la obra?
criterio-seguridad-escena-incidente-preservar|Orden y emergencias|Accidente|Preservación|Atender primero a las personas y conservar evidencias sin crear otro riesgo.|¿Debe limpiarse inmediatamente el lugar de un accidente?
'''


def normalizar(texto: str) -> str:
    base = unicodedata.normalize("NFD", str(texto or "").strip().lower())
    return "".join(c for c in base if unicodedata.category(c) != "Mn")


def criterio(datos: tuple[str, str, str, str, str]) -> dict:
    identificador, elemento, parametro, texto, pregunta = datos
    return {
        "id": identificador,
        "categoria": "Seguridad durante la construcción — control operativo",
        "elemento": elemento,
        "parametro": parametro,
        "clasificacion": "recomendacion",
        "valor": {"tipo": "sin_valor_universal", "valor": None, "minimo": None, "maximo": None, "unidad": None, "formula": None, "texto": texto},
        "condiciones": ["Aplicar junto con el Plan de Seguridad y Salud, la evaluación de riesgos, la Norma G.050, el procedimiento de trabajo y las instrucciones del fabricante."],
        "fuente": {"tipo": "criterio_tecnico", "norma": "Formación técnica SENCICO", "denominacion": "Seguridad y salud ocupacional", "dispositivo": None, "numeral": "Aplicación práctica supervisada", "numeral_confirmado": False, "url_oficial": SENCICO},
        "estado_revision": "criterio_tecnico_revisado",
        "advertencia": "La medida concreta debe ser definida por personal competente según la tarea, el equipo, el entorno y la evaluación de riesgos. No sustituye el Plan de Seguridad y Salud ni la Norma G.050.",
        "faq_relacionadas": [],
        "fecha_revision": "2026-07-27",
        "pregunta": pregunta,
        "respuesta": texto,
    }


def reemplazar_unico(texto: str, anterior: str, nuevo: str) -> str:
    if texto.count(anterior) != 1:
        raise SystemExit(f"Coincidencia inesperada para: {anterior}")
    return texto.replace(anterior, nuevo, 1)


def main() -> None:
    filas = [tuple(parte.strip() for parte in linea.split("|", 4)) for linea in RAW.splitlines() if linea.strip()]
    if any(len(fila) != 5 for fila in filas):
        raise SystemExit("Hay una fila de seguridad incompleta")
    registros = [criterio(fila) for fila in filas]
    if len({r["id"] for r in registros}) != len(registros):
        raise SystemExit("Hay identificadores repetidos en el lote")

    base = json.loads(NORMATIVA.read_text(encoding="utf-8"))
    preguntas = json.loads(PREGUNTAS.read_text(encoding="utf-8"))
    if base["version"] != "2.8.0" or len(base["parametros"]) != 1802:
        raise SystemExit("Base normativa inesperada")

    ids_existentes = {p["id"] for p in base["parametros"]}
    repetidos = ids_existentes.intersection(r["id"] for r in registros)
    if repetidos:
        raise SystemExit("ID ya existente: " + ", ".join(sorted(repetidos)))

    todas_actuales = [p for categoria in preguntas.get("categorias", []) for p in categoria.get("preguntas", []) if isinstance(p, dict)]
    preguntas_existentes = {normalizar(p.get("pregunta", "")) for p in todas_actuales}
    duplicadas = [r["pregunta"] for r in registros if normalizar(r["pregunta"]) in preguntas_existentes]
    if duplicadas:
        raise SystemExit("Pregunta ya existente: " + duplicadas[0])

    maximo = max(int(p["id"][1:]) for p in todas_actuales if re.fullmatch(r"q\d+", p.get("id", "")))
    categoria = next((c for c in preguntas["categorias"] if c.get("nombre") == "Seguridad durante la construcción — control operativo"), None)
    if categoria is None:
        categoria = {"nombre": "Seguridad durante la construcción — control operativo", "preguntas": []}
        preguntas["categorias"].append(categoria)

    for indice, registro in enumerate(registros, 1):
        qid = f"q{maximo + indice}"
        parametro = {k: v for k, v in registro.items() if k not in {"pregunta", "respuesta"}}
        parametro["faq_relacionadas"] = [qid]
        base["parametros"].append(parametro)
        categoria["preguntas"].append({"id": qid, "pregunta": registro["pregunta"], "respuesta": registro["respuesta"]})

    k = len(registros)
    base["version"] = "2.9.0"
    base["fecha_revision"] = "2026-07-27"
    esperados = (1802 + k, 3265 + k, 1245, 539 + k)
    totales = (
        len(base["parametros"]),
        sum(len(c.get("preguntas", [])) for c in preguntas["categorias"]),
        sum(p.get("estado_revision") == "validado_con_numeral" for p in base["parametros"]),
        sum(p.get("estado_revision") == "criterio_tecnico_revisado" for p in base["parametros"]),
    )
    if totales != esperados:
        raise SystemExit(f"Totales inesperados: {totales}, esperados: {esperados}")

    NORMATIVA.write_text(json.dumps(base, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    PREGUNTAS.write_text(json.dumps(preguntas, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    check = CHECK.read_text(encoding="utf-8")
    check = reemplazar_unico(check, "if len(base.parametros) < 1802:", f"if len(base.parametros) < {1802 + k}:")
    check = reemplazar_unico(check, "por lo menos 1802 parámetros revisados", f"por lo menos {1802 + k} parámetros revisados")
    check = reemplazar_unico(check, 'if base.version != "2.8.0":', 'if base.version != "2.9.0":')
    check = reemplazar_unico(check, "La versión normativa esperada es 2.8.0", "La versión normativa esperada es 2.9.0")
    check = reemplazar_unico(check, "if criterios < 539:", f"if criterios < {539 + k}:")
    check = reemplazar_unico(check, "al menos 539 criterios técnicos revisados", f"al menos {539 + k} criterios técnicos revisados")
    check = reemplazar_unico(check, "if len(todas) < 3265:", f"if len(todas) < {3265 + k}:")
    check = reemplazar_unico(check, "por lo menos 3265 preguntas técnicas", f"por lo menos {3265 + k} preguntas técnicas")
    extra = '''\n    seguridad_ats = api.detalle_parametro_normativo("criterio-seguridad-ats-tarea-no-rutinaria")\n    if seguridad_ats["estado_revision"] != "criterio_tecnico_revisado":\n        raise SystemExit("El ATS debe conservarse como criterio técnico revisado.")\n\n    seguridad_escalera = api.detalle_parametro_normativo("criterio-seguridad-escalera-metal-electricidad")\n    if "conductores energizados" not in seguridad_escalera["valor"]["texto"]:\n        raise SystemExit("La escalera metálica debe conservar la advertencia eléctrica.")\n\n    seguridad_andamio = api.detalle_parametro_normativo("criterio-seguridad-andamio-no-ladrillos")\n    if seguridad_andamio["fuente"]["tipo"] != "criterio_tecnico":\n        raise SystemExit("La base del andamio debe conservar fuente técnica.")\n\n    seguridad_esmeril = api.detalle_parametro_normativo("criterio-seguridad-esmeril-guarda")\n    if "guarda" not in seguridad_esmeril["valor"]["texto"]:\n        raise SystemExit("El esmeril debe conservar la exigencia de guarda.")\n\n    seguridad_izaje = api.detalle_parametro_normativo("criterio-seguridad-izaje-sin-personas-debajo")\n    if "debajo" not in seguridad_izaje["valor"]["texto"]:\n        raise SystemExit("El izaje debe prohibir personas bajo la carga.")\n\n    seguridad_excavacion = api.detalle_parametro_normativo("criterio-seguridad-excavacion-no-entrar-sin-soporte")\n    if "No ingresar" not in seguridad_excavacion["valor"]["texto"]:\n        raise SystemExit("La excavación debe conservar la restricción de ingreso.")\n\n'''
    check = reemplazar_unico(check, "    preguntas = json.loads(\n", extra + "    preguntas = json.loads(\n")
    CHECK.write_text(check, encoding="utf-8")

    DOC.write_text(f'''# Validación de seguridad durante la construcción — 27 de julio de 2026\n\n## Alcance\n\nSe incorporaron **{k} parámetros** y **{k} preguntas** después de depurar **839 registros relacionados**, entre ellos **206 parámetros G.050** ya existentes.\n\n## Contenido\n\n- planificación diaria, inducción, ATS, permisos y coordinación de frentes;\n- selección, inspección, almacenamiento y limitaciones del EPP;\n- escaleras, andamios, huecos, bordes, anclajes y rescate;\n- herramientas eléctricas, discos, guardas, cables y bloqueo de energía;\n- soldadura, oxicorte, cilindros, humos y vigilancia de fuego;\n- izaje, eslingas, ganchos, señalero, carga suspendida y maquinaria móvil;\n- excavaciones, servicios enterrados, atmósferas y espacios confinados;\n- encofrados, acero, concreto, bombeo, desencofrado y apuntalamiento;\n- tránsito interno, protección del público, polvo, ruido, calor, lluvia y tormenta;\n- orden, derrames, químicos, primeros auxilios, simulacros y evacuación.\n\n## Resultado\n\n- Versión normativa: `2.9.0`.\n- Parámetros totales: `{1802 + k}`.\n- Registros `validado_con_numeral`: `1245`.\n- Criterios técnicos revisados: `{539 + k}`.\n- Preguntas técnicas: `{3265 + k}`.\n\n## Criterios editoriales\n\n- Se conservaron sin duplicar los mínimos y prohibiciones ya registrados de la G.050.\n- La G.050 vigente sigue identificada en el RNE como la aprobada por DS N.° 010-2009; los comités de actualización no se trataron como norma aprobada.\n- El nuevo lote se concentra en decisiones operativas, inspección previa, compatibilidad de equipos y respuesta ante cambios.\n- No se fijaron capacidades, distancias, frecuencias o límites universales cuando dependen del equipo, fabricante, cálculo o evaluación de riesgos.\n- Las reglas nuevas se identifican como `criterio_tecnico_revisado` y no sustituyen el PSST, la G.050, el responsable de obra ni los procedimientos específicos.\n\n## Fuentes oficiales complementarias\n\n- SENCICO: Seguridad y salud ocupacional.\n- MTPE: Seguridad y salud en el trabajo en el sector construcción ({MTPE}).\n''', encoding="utf-8")
    print(f"Aplicados {k} parámetros y preguntas; versión 2.9.0")


if __name__ == "__main__":
    main()
