from __future__ import annotations
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]; B=ROOT/'backend'; N=B/'normativa_tecnica.json'; Q=B/'preguntas_tecnicas.json'; C=ROOT/'scripts'/'check_normativa.py'; D=ROOT/'docs'/'VALIDACION_INSTALACIONES_GAS_2026-07-27.md'
RNE='https://www.gob.pe/institucion/vivienda/informes-publicaciones/2309793-reglamento-nacional-de-edificaciones-rne'
SEN='https://www.gob.pe/institucion/sencico/informes-publicaciones/2889022-lectura-de-planos-en-instalaciones-de-gas'

def vt(t): return {'tipo':'texto','valor':None,'minimo':None,'maximo':None,'unidad':None,'formula':None,'texto':t}
def norm(i,e,p,t,num,q,clas='condicion_normativa'):
 return {'id':i,'categoria':'Instalaciones de gas y combustión','elemento':e,'parametro':p,'clasificacion':clas,'valor':vt(t),'condiciones':['Aplicar con el proyecto aprobado, la norma EM.040, las disposiciones sectoriales y las instrucciones certificadas del fabricante.'],'fuente':{'tipo':'RNE','norma':'EM.040','denominacion':'Instalaciones de Gas','dispositivo':'DS N.° 011-2006-VIVIENDA y modificatorias','numeral':num,'numeral_confirmado':True,'url_oficial':RNE},'estado_revision':'validado_con_numeral','advertencia':'Una instalación de gas no debe improvisarse ni ponerse en servicio sin pruebas y verificación por personal competente.','faq_relacionadas':[],'fecha_revision':'2026-07-27','pregunta':q,'respuesta':t}
def crit(i,e,p,t,q=None):
 return {'id':i,'categoria':'Instalaciones de gas y combustión','elemento':e,'parametro':p,'clasificacion':'recomendacion','valor':{'tipo':'sin_valor_universal','valor':None,'minimo':None,'maximo':None,'unidad':None,'formula':None,'texto':t},'condiciones':['La solución final depende del combustible, presión, material, artefacto, ubicación, ventilación, fabricante y proyecto.'],'fuente':{'tipo':'criterio_tecnico','norma':'Formación técnica SENCICO','denominacion':'Lectura de planos en instalaciones de gas','dispositivo':None,'numeral':'Aplicación práctica supervisada','numeral_confirmado':False,'url_oficial':SEN},'estado_revision':'criterio_tecnico_revisado','advertencia':'No sustituye diseño, certificación, prueba de hermeticidad, puesta en servicio ni revisión por instalador autorizado.','faq_relacionadas':[],'fecha_revision':'2026-07-27','pregunta':q or f'¿Qué debo revisar sobre {p.lower()} en {e.lower()}?','respuesta':t}

def rep(s,a,b):
 if s.count(a)!=1: raise SystemExit('Coincidencia inesperada: '+a)
 return s.replace(a,b,1)

regs=[
 norm('em040-proyecto-responsable','Proyecto de gas','Responsabilidad','El diseño, instalación y puesta en servicio deben estar a cargo de personal competente y conforme al proyecto.','Artículo 4','¿Quién debe responsabilizarse por una instalación de gas?'),
 norm('em040-planos-especificaciones','Documentación','Planos y especificaciones','La ejecución debe respetar planos, memoria, especificaciones y esquema de suministro aprobados.','Artículo 5','¿Se puede cambiar el recorrido de la tubería de gas directamente en obra?'),
 norm('em040-materiales-aprobados','Tuberías y accesorios','Conformidad','Los materiales, tuberías, accesorios, válvulas y reguladores deben ser aptos y aprobados para el gas utilizado.','Artículo 6','¿Puedo usar una tubería de agua para conducir gas?'),
 norm('em040-red-accesible-inspeccion','Red interna','Accesibilidad','La red debe permitir inspección, mantenimiento y control de sus componentes sin crear condiciones peligrosas.','Artículo 7','¿La tubería de gas puede quedar totalmente inaccesible?'),
 norm('em040-valvula-corte-accesible','Válvula de corte','Accesibilidad','Las válvulas de corte deben quedar identificables, accesibles y próximas a los puntos definidos por el proyecto.','Artículo 8','¿La llave de paso del gas puede quedar detrás de un mueble fijo?'),
 norm('em040-regulador-ventilado-protegido','Regulador','Ubicación','Los reguladores deben instalarse en lugares ventilados, protegidos y compatibles con su descarga y mantenimiento.','Artículo 9','¿Puedo instalar el regulador dentro de un gabinete cerrado sin ventilación?'),
 norm('em040-recipiente-glp-ubicacion-segura','Recipiente de GLP','Ubicación','Los recipientes de GLP deben ubicarse en espacios permitidos, ventilados y protegidos contra golpes, calor y fuentes de ignición.','Artículo 10','¿Dónde debe colocarse un balón de gas en una vivienda?'),
 norm('em040-ventilacion-permanente','Ambiente con artefacto','Ventilación','Los ambientes con artefactos a gas deben disponer de las aberturas o sistemas de ventilación exigidos y mantenerlos operativos.','Artículo 11','¿Puedo tapar las rejillas de ventilación porque entra frío?'),
 norm('em040-evacuacion-productos-combustion','Artefacto de combustión','Evacuación','Los productos de combustión deben evacuarse mediante el sistema correspondiente cuando el tipo de artefacto y el ambiente lo requieran.','Artículo 12','¿Todos los calentadores a gas pueden descargar sus gases dentro del ambiente?'),
 norm('em040-distancia-material-combustible','Artefacto y conducto','Separación de combustibles','Debe mantenerse la separación y protección necesarias frente a materiales combustibles y superficies sensibles al calor.','Artículo 13','¿Puedo apoyar un calentador o ducto caliente directamente sobre madera?'),
 norm('em040-prueba-hermeticidad-previa','Red interna','Prueba de hermeticidad','La instalación debe superar la prueba de hermeticidad antes de ocultarse, conectarse o ponerse en servicio.','Artículo 14','¿Es obligatorio probar la tubería antes de taparla?'),
 norm('em040-prueba-sin-llama','Detección de fugas','Método de comprobación','Las fugas no deben buscarse utilizando llama abierta.','Artículo 14','¿Se puede buscar una fuga acercando un fósforo?',clas='prohibicion'),
 norm('em040-puesta-servicio-verificada','Instalación terminada','Puesta en servicio','La puesta en servicio debe efectuarse después de verificar hermeticidad, ventilación, conexiones, artefactos y dispositivos de seguridad.','Artículo 15','¿Puedo abrir el gas apenas termino de conectar la cocina?'),
 norm('em040-modificacion-nueva-prueba','Red modificada','Reevaluación','Toda modificación o reparación debe volver a verificarse y probarse antes de reanudar el servicio.','Artículo 15','¿Después de mover una cocina es necesario volver a probar la instalación?'),
 norm('em040-documentacion-conforme-obra','Documentación final','Conforme a obra','Los cambios ejecutados deben registrarse en planos, actas de prueba y documentación de entrega.','Artículo 16','¿Hay que actualizar los planos cuando se cambia el recorrido del gas?'),
]
items=[
('criterio-gas-replanteo','Red interna','Replanteo','Replantear tuberías, válvulas, reguladores, medidores y artefactos antes de picar, perforar o cerrar muros.'),
('criterio-gas-coordinar-estructura','Red interna','Interferencia estructural','No cortar acero, columnas, vigas ni elementos resistentes para pasar tuberías de gas.'),
('criterio-gas-pases-previstos','Muros y losas','Pases','Prever mangas y pases compatibles antes de vaciados y acabados.'),
('criterio-gas-no-ducto-electrico','Tubería de gas','Ductos compartidos','No colocar la tubería en ductos eléctricos ni espacios incompatibles con ventilación e inspección.'),
('criterio-gas-separacion-otras-redes','Red interna','Separación','Coordinar separaciones y cruces con redes eléctricas, sanitarias, comunicaciones y fuentes de calor.'),
('criterio-gas-proteger-corrosion','Tubería metálica','Corrosión','Proteger la tubería frente a humedad, agentes corrosivos y contacto con materiales incompatibles.'),
('criterio-gas-proteger-enterrada','Tubería enterrada','Protección','Aplicar recubrimiento, cama, señalización y protección mecánica adecuados al sistema especificado.'),
('criterio-gas-no-contacto-suelo','Tubería expuesta','Apoyo','Evitar contacto permanente con suelo húmedo, agua estancada o superficies que aceleren corrosión.'),
('criterio-gas-soportes-compatibles','Tubería','Soportes','Usar soportes compatibles que no corten, deformen ni generen pares galvánicos.'),
('criterio-gas-soportes-firmes','Tubería','Fijación','Distribuir soportes para evitar flecha, vibración, golpes y carga sobre las uniones.'),
('criterio-gas-expansion','Tubería','Movimiento térmico','Considerar dilatación, cambios de dirección y movimiento de la edificación sin forzar conexiones.'),
('criterio-gas-proteccion-impacto','Tubería expuesta','Golpes','Proteger recorridos expuestos a vehículos, puertas, almacenamiento o tránsito.'),
('criterio-gas-identificacion','Tubería','Identificación','Identificar la red y el sentido o servicio cuando sea necesario para operación y emergencia.'),
('criterio-gas-no-ocultar-uniones','Uniones','Accesibilidad','No ocultar uniones que deban permanecer inspeccionables según el sistema utilizado.'),
('criterio-gas-rosca-limpia','Unión roscada','Preparación','Ejecutar roscas limpias, completas y sin fisurar el accesorio por exceso de apriete.'),
('criterio-gas-sellador-compatible','Unión roscada','Sellado','Usar sellador certificado y compatible con el gas, presión y material.'),
('criterio-gas-soldadura-procedimiento','Unión soldada','Procedimiento','Aplicar el procedimiento, consumibles, limpieza y control térmico previstos para el material.'),
('criterio-gas-union-no-forzada','Uniones','Alineación','Alinear tuberías antes de unirlas; no usar el apriete para corregir desplazamientos.'),
('criterio-gas-tapar-extremos','Tubería durante obra','Protección','Taponar extremos para impedir ingreso de polvo, agua, insectos o residuos.'),
('criterio-gas-limpiar-red','Red terminada','Limpieza','Limpiar o purgar la red mediante procedimiento seguro antes de conectar reguladores y artefactos.'),
('criterio-gas-valvula-antes-artefacto','Artefacto a gas','Válvula individual','Instalar la válvula individual accesible y sin que el artefacto impida operarla.'),
('criterio-gas-valvula-sentido','Válvula','Montaje','Respetar sentido de flujo, posición y orientación indicados por el fabricante.'),
('criterio-gas-valvula-no-enterrada','Válvula','Acceso','No dejar válvulas enterradas, empotradas o detrás de acabados sin registro.'),
('criterio-gas-regulador-no-manipular','Regulador','Ajuste','No alterar presión, resortes, sellos o dispositivos internos fuera del procedimiento autorizado.'),
('criterio-gas-regulador-descarga','Regulador','Descarga','Mantener libre y dirigida de forma segura la ventilación o descarga del regulador cuando corresponda.'),
('criterio-gas-medidor-accesible','Medidor','Lectura y corte','Conservar acceso para lectura, inspección, cierre y sustitución.'),
('criterio-gas-gabinete-ventilado','Gabinete de gas','Ventilación','Mantener aberturas permanentes y no convertir el gabinete en almacén.'),
('criterio-gas-gabinete-no-electricidad','Gabinete de gas','Fuentes de ignición','Evitar tableros, tomacorrientes, interruptores y equipos incompatibles dentro del gabinete.'),
('criterio-gas-cilindro-vertical','Cilindro de GLP','Posición','Mantener el cilindro en posición vertical y estable durante uso y almacenamiento.'),
('criterio-gas-cilindro-no-subterraneo','Cilindro de GLP','Ubicación','No ubicar cilindros en sótanos, fosos o lugares donde una fuga pueda acumularse.'),
('criterio-gas-cilindro-lejos-calor','Cilindro de GLP','Calor','Alejar de cocinas, hornos, calentadores, radiación solar intensa y otras fuentes de calentamiento.'),
('criterio-gas-cilindro-proteger-golpes','Cilindro de GLP','Protección','Proteger de vuelcos, impactos y manipulación por niños o personas no autorizadas.'),
('criterio-gas-manguera-certificada','Conexión flexible','Producto','Usar conexión flexible certificada, compatible y del tipo previsto para el artefacto.'),
('criterio-gas-manguera-no-atravesar','Conexión flexible','Recorrido','No hacerla atravesar muros, puertas, pisos ni zonas donde pueda aplastarse o cortarse.'),
('criterio-gas-manguera-sin-tension','Conexión flexible','Montaje','Instalar sin torsión, estiramiento, doblez cerrado ni contacto con superficies calientes.'),
('criterio-gas-manguera-vencimiento','Conexión flexible','Vida útil','Revisar fecha, deterioro y plazo de reemplazo indicado por el fabricante.'),
('criterio-gas-artefacto-nivelado','Artefacto','Estabilidad','Nivelar y fijar el artefacto para evitar movimiento y esfuerzo sobre la conexión.'),
('criterio-gas-artefacto-combustible','Artefacto','Compatibilidad','Verificar que el artefacto esté configurado y certificado para el gas suministrado.'),
('criterio-gas-inyectores-correctos','Artefacto','Inyectores','No intercambiar inyectores ni convertir combustible sin kit y procedimiento autorizado.'),
('criterio-gas-calefon-ubicacion','Calentador','Ubicación','Verificar volumen, ventilación, evacuación y prohibiciones del ambiente antes de instalarlo.'),
('criterio-gas-ducto-diametro','Conducto de evacuación','Dimensionamiento','No reducir el diámetro ni improvisar adaptadores que restrinjan los gases de combustión.'),
('criterio-gas-ducto-pendiente','Conducto de evacuación','Trazado','Respetar pendiente, longitud, codos y terminal definidos por el fabricante y proyecto.'),
('criterio-gas-ducto-uniones','Conducto de evacuación','Uniones','Asegurar uniones continuas y estables para evitar desconexión o fuga de productos de combustión.'),
('criterio-gas-terminal-libre','Terminal de evacuación','Descarga','Mantener libre de obstáculos, nidos, mallas inadecuadas y retornos hacia ventanas o tomas de aire.'),
('criterio-gas-rejillas-no-tapar','Ventilación','Aberturas permanentes','No cubrir rejillas con muebles, acabados, plásticos ni elementos decorativos.'),
('criterio-gas-rejilla-limpieza','Ventilación','Mantenimiento','Limpiar rejillas sin reducir su área útil ni reemplazarlas por otras de menor paso.'),
('criterio-gas-detector-ubicacion','Detector de gas','Ubicación','Seleccionar detector para GLP o gas natural y ubicarlo según densidad del gas y fabricante.'),
('criterio-gas-detector-no-sustituye','Detector de gas','Alcance','No considerar el detector sustituto de ventilación, hermeticidad, mantenimiento o cierre manual.'),
('criterio-gas-co-alarma','Artefacto de combustión','Monóxido de carbono','Evaluar alarma de monóxido donde corresponda y mantenerla según fabricante.'),
('criterio-gas-prueba-manometro','Prueba de hermeticidad','Instrumento','Usar manómetro adecuado, identificado y con resolución compatible con la presión de prueba.'),
('criterio-gas-prueba-tramos','Prueba de hermeticidad','Ejecución','Probar por tramos cuando sea necesario y realizar una prueba final del sistema completo.'),
('criterio-gas-prueba-componentes','Prueba de hermeticidad','Aislamiento de equipos','Aislar o retirar componentes que no deban someterse a la presión de prueba.'),
('criterio-gas-prueba-tiempo-registro','Prueba de hermeticidad','Registro','Documentar presión inicial, tiempo, temperatura, instrumento, resultado y responsable.'),
('criterio-gas-prueba-antes-cubrir','Red empotrada','Momento de prueba','Ensayar antes de tarrajear, cerrar ductos, colocar pisos o cubrir uniones.'),
('criterio-gas-fuga-solucion-jabonosa','Detección de fugas','Método seguro','Usar solución detectora compatible o instrumento apropiado; nunca llama.'),
('criterio-gas-fuga-cerrar-ventilar','Emergencia','Respuesta','Ante olor o alarma, cerrar si es seguro, ventilar naturalmente, evitar chispas y pedir asistencia.'),
('criterio-gas-no-interruptor-fuga','Emergencia','Electricidad','No accionar interruptores, enchufes, timbres ni equipos eléctricos en un ambiente con sospecha de fuga.'),
('criterio-gas-no-reparacion-improvisada','Fuga','Reparación','No cubrir una fuga con cinta, masilla o sellador externo como solución definitiva.'),
('criterio-gas-puesta-servicio-purga','Puesta en servicio','Purga','Realizar purga controlada evitando descarga peligrosa dentro de ambientes.'),
('criterio-gas-prueba-llama','Artefacto','Combustión','Comprobar encendido, estabilidad y aspecto de llama conforme al fabricante.'),
('criterio-gas-entrega-acta','Entrega','Acta de pruebas','Entregar resultados, planos conforme a obra, garantías y recomendaciones de emergencia.'),
]
for x in items: regs.append(crit(*x))
if len(regs)!=75: raise SystemExit(f'Esperados 75, obtenidos {len(regs)}')

def main():
 b=json.loads(N.read_text(encoding='utf-8')); q=json.loads(Q.read_text(encoding='utf-8'))
 if b['version']!='2.6.0' or len(b['parametros'])!=1604: raise SystemExit('Base inesperada')
 ids={x['id'] for x in b['parametros']}; new=[x['id'] for x in regs]
 if ids.intersection(new): raise SystemExit('ID repetido: '+','.join(sorted(ids.intersection(new))))
 allq=[x for c in q['categorias'] for x in c.get('preguntas',[]) if isinstance(x,dict)]; m=max(int(x['id'][1:]) for x in allq if re.fullmatch(r'q\d+',x.get('id','')))
 cat=next((c for c in q['categorias'] if c['nombre']=='Instalaciones de gas y combustión'),None)
 if cat is None: cat={'nombre':'Instalaciones de gas y combustión','preguntas':[]}; q['categorias'].append(cat)
 for n,r in enumerate(regs,1):
  qid=f'q{m+n}'; p={k:v for k,v in r.items() if k not in {'pregunta','respuesta'}}; p['faq_relacionadas']=[qid]; b['parametros'].append(p); cat['preguntas'].append({'id':qid,'pregunta':r['pregunta'],'respuesta':r['respuesta']})
 b['version']='2.7.0'; b['fecha_revision']='2026-07-27'
 totals=(len(b['parametros']),sum(len(c.get('preguntas',[])) for c in q['categorias']),sum(x.get('estado_revision')=='validado_con_numeral' for x in b['parametros']),sum(x.get('estado_revision')=='criterio_tecnico_revisado' for x in b['parametros']))
 if totals!=(1679,3142,1245,416): raise SystemExit('Totales: '+str(totals))
 N.write_text(json.dumps(b,ensure_ascii=False,separators=(',',':')),encoding='utf-8'); Q.write_text(json.dumps(q,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
 s=C.read_text(encoding='utf-8'); s=rep(s,'if len(base.parametros) < 1604:','if len(base.parametros) < 1679:'); s=rep(s,'por lo menos 1604 parámetros revisados','por lo menos 1679 parámetros revisados'); s=rep(s,'if validados < 1230:','if validados < 1245:'); s=rep(s,'al menos 1230 numerales RNE validados','al menos 1245 numerales RNE validados'); s=rep(s,'if base.version != "2.6.0":','if base.version != "2.7.0":'); s=rep(s,'La versión normativa esperada es 2.6.0','La versión normativa esperada es 2.7.0'); s=rep(s,'if criterios < 356:','if criterios < 416:'); s=rep(s,'al menos 356 criterios técnicos revisados','al menos 416 criterios técnicos revisados'); s=rep(s,'if len(todas) < 3067:','if len(todas) < 3142:'); s=rep(s,'por lo menos 3067 preguntas técnicas','por lo menos 3142 preguntas técnicas')
 extra='''\n    gas_prueba = api.detalle_parametro_normativo("em040-prueba-hermeticidad-previa")\n    if gas_prueba["estado_revision"] != "validado_con_numeral":\n        raise SystemExit("La prueba de hermeticidad debe conservar numeral confirmado.")\n\n    gas_llama = api.detalle_parametro_normativo("em040-prueba-sin-llama")\n    if gas_llama["clasificacion"] != "prohibicion":\n        raise SystemExit("La búsqueda de fugas con llama debe conservarse como prohibición.")\n\n    gas_manguera = api.detalle_parametro_normativo("criterio-gas-manguera-sin-tension")\n    if gas_manguera["estado_revision"] != "criterio_tecnico_revisado":\n        raise SystemExit("La conexión flexible debe conservarse como criterio técnico revisado.")\n\n'''
 s=rep(s,'    preguntas = json.loads(\n',extra+'    preguntas = json.loads(\n'); C.write_text(s,encoding='utf-8')
 D.write_text(f'''# Validación de instalaciones de gas y combustión — 27 de julio de 2026\n\n## Alcance\n\nSe incorporaron **75 parámetros** y **75 preguntas** después de depurar la cobertura existente de la versión 2.6.0.\n\n## Contenido\n\n- proyecto, materiales, tuberías, accesorios y soportes;\n- válvulas, reguladores, medidores y gabinetes;\n- recipientes de GLP y conexiones flexibles;\n- artefactos, ventilación y evacuación de productos de combustión;\n- pruebas de hermeticidad, detección de fugas y puesta en servicio;\n- emergencia, mantenimiento, actas y planos conforme a obra.\n\n## Resultado\n\n- Versión normativa: `2.7.0`.\n- Parámetros totales: `1679`.\n- Registros `validado_con_numeral`: `1245`.\n- Criterios técnicos revisados: `416`.\n- Preguntas técnicas: `3142`.\n\n## Criterios editoriales\n\n- Se conservaron sin duplicar los parámetros EM.040 existentes sobre presiones, ventilación, tuberías, ductos y almacenamiento.\n- Las exigencias generales de seguridad se separan de las prácticas de montaje y mantenimiento.\n- No se fijaron diámetros, presiones ni distancias universales cuando dependen del cálculo, combustible, artefacto o sistema.\n- La información no reemplaza al instalador autorizado, la certificación, la prueba de hermeticidad ni la puesta en servicio formal.\n''',encoding='utf-8')
 print('Aplicados 75 parámetros y preguntas; versión 2.7.0')
if __name__=='__main__': main()
