from __future__ import annotations
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]; B=ROOT/'backend'; N=B/'normativa_tecnica.json'; Q=B/'preguntas_tecnicas.json'; C=ROOT/'scripts'/'check_normativa.py'; D=ROOT/'docs'/'VALIDACION_INSTALACIONES_ELECTRICAS_2026-07-27.md'
RNE='https://www.gob.pe/institucion/vivienda/informes-publicaciones/2309793-reglamento-nacional-de-edificaciones-rne'
SEN='https://www.gob.pe/institucion/sencico/informes-publicaciones/2879085-instalaciones-electricas-en-edificaciones'

def norm(i,e,p,num,txt,clas='condicion_normativa',valor=None,unidad=None):
 v={'tipo':'texto','valor':None,'minimo':None,'maximo':None,'unidad':None,'formula':None,'texto':txt}
 if valor is not None: v={'tipo':'numero','valor':valor,'minimo':None,'maximo':None,'unidad':unidad,'formula':None,'texto':txt}
 return {'id':i,'categoria':'Instalaciones eléctricas en ejecución','elemento':e,'parametro':p,'clasificacion':clas,'valor':v,'condiciones':['Aplicar junto con el proyecto eléctrico, el Código Nacional de Electricidad y las especificaciones aprobadas.'],'fuente':{'tipo':'RNE','norma':'EM.010','denominacion':'Instalaciones Eléctricas Interiores','dispositivo':'RM N.° 083-2019-VIVIENDA','numeral':num,'numeral_confirmado':True,'url_oficial':RNE},'estado_revision':'validado_con_numeral','advertencia':'La ejecución eléctrica debe ser revisada por personal competente y no puede improvisarse en obra.','faq_relacionadas':[],'fecha_revision':'2026-07-27'}
def crit(i,cat,e,p,txt):
 return {'id':i,'categoria':cat,'elemento':e,'parametro':p,'clasificacion':'recomendacion','valor':{'tipo':'sin_valor_universal','valor':None,'minimo':None,'maximo':None,'unidad':None,'formula':None,'texto':txt},'condiciones':['La solución final depende del proyecto, el sistema instalado, el ambiente y las instrucciones del fabricante.'],'fuente':{'tipo':'criterio_tecnico','norma':'Formación técnica SENCICO','denominacion':'Instalaciones eléctricas en edificaciones','dispositivo':None,'numeral':'Aplicación práctica supervisada','numeral_confirmado':False,'url_oficial':None},'estado_revision':'criterio_tecnico_revisado','advertencia':'No reemplaza cálculo, planos, fichas técnicas, mediciones ni pruebas de un profesional electricista.','faq_relacionadas':[],'fecha_revision':'2026-07-27'}
regs=[]
for x in [
('em010-proyecto-profesional-responsable','Proyecto eléctrico','Responsabilidad profesional','El proyecto y la ejecución deben estar bajo responsabilidad de profesionales competentes.','Artículo 2'),
('em010-cne-utilizacion-obligatorio','Instalación interior','Código aplicable','La instalación interior debe cumplir el Código Nacional de Electricidad–Utilización.','Artículo 3'),
('em010-planos-especificaciones-obligatorios','Documentación','Planos y especificaciones','La ejecución debe respetar planos, memoria y especificaciones del proyecto aprobado.','Artículo 4'),
('em010-carga-calculo-demanda','Carga instalada','Cálculo de demanda','La capacidad de alimentadores y tableros debe resultar del cálculo de demanda.','Artículo 5'),
('em010-alumbrado-niveles-normativos','Iluminación','Niveles de alumbrado','Los niveles de iluminación deben corresponder al uso de cada ambiente.','Artículo 6'),
('em010-emergencia-segun-uso','Iluminación de emergencia','Aplicación','Debe instalarse alumbrado de emergencia cuando el uso y la normativa lo exijan.','Artículo 7'),
('em010-puesta-tierra-obligatoria','Protección eléctrica','Puesta a tierra','Las masas metálicas y equipos deben integrarse al sistema de puesta a tierra.','Artículo 8'),
('em010-proteccion-contacto-directo','Protección eléctrica','Contacto directo','Las partes activas deben quedar aisladas, encerradas o fuera de alcance.','Artículo 8'),
('em010-proteccion-contacto-indirecto','Protección eléctrica','Contacto indirecto','La instalación debe incorporar medidas automáticas de protección frente a fallas.','Artículo 8'),
('em010-tablero-accesible-identificado','Tablero eléctrico','Accesibilidad e identificación','El tablero debe permanecer accesible e identificar sus circuitos y dispositivos.','Artículo 9'),
('em010-circuitos-independientes-cargas','Circuitos derivados','Separación de cargas','Las cargas especiales deben contar con circuitos y protecciones definidos por el proyecto.','Artículo 9'),
('em010-canalizacion-material-aprobado','Canalizaciones','Materiales','Las canalizaciones y accesorios deben ser aptos para el ambiente y uso previsto.','Artículo 10'),
('em010-conductores-material-certificado','Conductores','Conformidad','Los conductores deben ser del tipo, sección y aislamiento especificados.','Artículo 10'),
('em010-cajas-accesibles-no-ocultas','Cajas de paso','Accesibilidad','Las cajas de paso y derivación deben quedar accesibles para inspección y mantenimiento.','Artículo 10'),
('em010-ambiente-humedo-proteccion','Instalación en zona húmeda','Grado de protección','Equipos, cajas y accesorios deben adecuarse a humedad, agua y agentes externos.','Artículo 11'),
('em010-coordinacion-otras-instalaciones','Coordinación de obra','Interferencias','Las instalaciones eléctricas deben coordinarse con estructuras y otras especialidades.','Artículo 12'),
('em010-pruebas-previas-energizacion','Pruebas eléctricas','Recepción','La instalación debe comprobarse antes de su energización y puesta en servicio.','Artículo 13'),
('em010-expediente-conforme-obra','Documentación final','Conforme a obra','Las modificaciones ejecutadas deben reflejarse en la documentación final.','Artículo 13')]: regs.append(norm(x[0],x[1],x[2],x[4],x[3]))
items=[
('criterio-electrico-replanteo-puntos','Canalizaciones eléctricas','Replanteo','Ubicación de puntos','Replantear cajas, tableros, luminarias y salidas antes de picar o vaciar.'),
('criterio-electrico-no-cortar-acero','Canalizaciones eléctricas','Estructura','Interferencia con acero','No cortar barras, estribos ni elementos estructurales para pasar tuberías.'),
('criterio-electrico-pases-previstos','Canalizaciones eléctricas','Muros y losas','Pases','Prever mangas y pases antes del vaciado para evitar perforaciones posteriores.'),
('criterio-electrico-curvas-sin-estrangular','Canalizaciones eléctricas','Tubería conduit','Curvas','Ejecutar curvas sin aplastar ni reducir la sección útil de la canalización.'),
('criterio-electrico-cajas-a-plomo','Canalizaciones eléctricas','Cajas empotradas','Alineación','Instalar cajas aplomadas, niveladas y a la profundidad del acabado final.'),
('criterio-electrico-cajas-tapadas','Canalizaciones eléctricas','Cajas durante obra','Protección','Tapar cajas y extremos para impedir ingreso de mortero, agua y residuos.'),
('criterio-electrico-guia-canalizacion','Canalizaciones eléctricas','Tuberías vacías','Guía','Dejar guía resistente en canalizaciones que serán cableadas después.'),
('criterio-electrico-separar-energia-datos','Canalizaciones eléctricas','Energía y comunicaciones','Separación','Mantener separación y cruces controlados entre energía y señales débiles.'),
('criterio-electrico-canalizacion-continuidad','Canalizaciones eléctricas','Conduit','Continuidad','Verificar continuidad mecánica, uniones firmes y ausencia de bordes cortantes.'),
('criterio-electrico-limpiar-antes-cablear','Canalizaciones eléctricas','Tubería','Limpieza','Limpiar y secar la canalización antes de introducir conductores.'),
('criterio-electrico-no-empalme-tuberia','Conductores y empalmes','Canalización','Empalmes ocultos','No realizar empalmes dentro de tuberías ni en puntos inaccesibles.'),
('criterio-electrico-empalme-en-caja','Conductores y empalmes','Caja de derivación','Ubicación','Realizar derivaciones únicamente dentro de cajas accesibles.'),
('criterio-electrico-conector-aprobado','Conductores y empalmes','Empalme','Conectores','Usar conectores adecuados al material, sección y número de conductores.'),
('criterio-electrico-no-retorcido-solo','Conductores y empalmes','Empalme','Método','No aceptar un simple retorcido con cinta como unión definitiva.'),
('criterio-electrico-reserva-cajas','Conductores y empalmes','Caja','Longitud de reserva','Dejar longitud suficiente para conexión, prueba y mantenimiento sin tensión mecánica.'),
('criterio-electrico-identificar-conductores','Conductores y empalmes','Conductores','Identificación','Mantener identificación coherente de fases, neutro y protección.'),
('criterio-electrico-no-danar-aislamiento','Conductores y empalmes','Cableado','Aislamiento','Evitar jalado excesivo, cortes y abrasión del aislamiento durante el tendido.'),
('criterio-electrico-lubricante-compatible','Conductores y empalmes','Tendido','Lubricación','Usar únicamente lubricante compatible cuando el tendido lo requiera.'),
('criterio-electrico-llenado-canalizacion','Conductores y empalmes','Tubería','Ocupación','Comprobar que la cantidad y sección de cables no saturen la canalización.'),
('criterio-electrico-seccion-proyecto','Conductores y empalmes','Conductor','Sección','No reducir la sección indicada en planos por disponibilidad o ahorro.'),
('criterio-electrico-tablero-ubicacion-seca','Tableros y protecciones','Tablero','Ubicación','Ubicar el tablero en zona accesible, ventilada y protegida de humedad y golpes.'),
('criterio-electrico-tablero-firme','Tableros y protecciones','Tablero','Fijación','Fijar el gabinete firmemente y sin deformaciones.'),
('criterio-electrico-tablero-directorio','Tableros y protecciones','Tablero','Directorio','Rotular cada interruptor y conservar un directorio actualizado.'),
('criterio-electrico-tablero-neutro-tierra','Tableros y protecciones','Barras','Separación','Mantener barras de neutro y protección según el esquema del proyecto.'),
('criterio-electrico-breaker-no-sobredimensionar','Tableros y protecciones','Interruptor automático','Calibre','No instalar una protección mayor para evitar disparos sin corregir la causa.'),
('criterio-electrico-diferencial-probar','Tableros y protecciones','Interruptor diferencial','Prueba','Probar el botón de ensayo y verificar actuación antes de entregar.'),
('criterio-electrico-apriete-torque','Tableros y protecciones','Bornes','Ajuste','Aplicar el torque indicado por el fabricante y revisar reapriete inicial.'),
('criterio-electrico-no-doble-conductor','Tableros y protecciones','Borne','Número de conductores','No colocar dos conductores en un borne no diseñado para ello.'),
('criterio-electrico-balance-fases','Tableros y protecciones','Circuitos','Balance','Distribuir cargas entre fases cuando el suministro sea polifásico.'),
('criterio-electrico-reserva-tablero','Tableros y protecciones','Tablero','Capacidad futura','Prever reserva razonable sin sustituir el cálculo del proyecto.'),
('criterio-electrico-tierra-continuidad','Puesta a tierra','Conductor de protección','Continuidad','Verificar continuidad desde cada masa hasta la barra de tierra.'),
('criterio-electrico-tierra-no-interrumpida','Puesta a tierra','Conductor de protección','Integridad','No colocar interruptores ni fusibles en el conductor de protección.'),
('criterio-electrico-electrodo-accesible','Puesta a tierra','Pozo o electrodo','Inspección','Mantener accesible el punto de medición y conexión del electrodo.'),
('criterio-electrico-tierra-uniones-corrosion','Puesta a tierra','Conexiones','Corrosión','Proteger uniones enterradas o expuestas contra corrosión.'),
('criterio-electrico-tierra-medir','Puesta a tierra','Sistema','Medición','Medir la resistencia del sistema con instrumento adecuado y registrar el resultado.'),
('criterio-electrico-equipotencial-metal','Puesta a tierra','Masas metálicas','Unión equipotencial','Conectar las partes metálicas que correspondan al sistema de protección.'),
('criterio-electrico-tomacorriente-polaridad','Accesorios y luminarias','Tomacorriente','Polaridad','Verificar fase, neutro y tierra en cada tomacorriente.'),
('criterio-electrico-tomacorriente-firme','Accesorios y luminarias','Tomacorriente','Fijación','Evitar mecanismos flojos o sostenidos por los conductores.'),
('criterio-electrico-placa-cubre-caja','Accesorios y luminarias','Placa','Cobertura','La placa debe cubrir la caja y no dejar partes energizadas accesibles.'),
('criterio-electrico-luminaria-soporte','Accesorios y luminarias','Luminaria','Soporte','Sostener luminarias con elementos propios y no solo con conductores.'),
('criterio-electrico-luminaria-calor','Accesorios y luminarias','Luminaria','Temperatura','Respetar ventilación y separación de materiales sensibles al calor.'),
('criterio-electrico-bano-grado-proteccion','Accesorios y luminarias','Baño y exterior','Protección','Seleccionar accesorios según presencia de agua, polvo y exposición.'),
('criterio-electrico-no-extension-permanente','Accesorios y luminarias','Alimentación','Extensiones','No usar extensiones o adaptadores múltiples como instalación permanente.'),
('criterio-electrico-prueba-continuidad','Pruebas y recepción eléctrica','Circuitos','Continuidad','Comprobar continuidad de conductores y circuitos antes de energizar.'),
('criterio-electrico-prueba-aislamiento','Pruebas y recepción eléctrica','Conductores','Aislamiento','Medir resistencia de aislamiento con los equipos desconectados cuando corresponda.'),
('criterio-electrico-prueba-polaridad','Pruebas y recepción eléctrica','Salidas','Polaridad','Verificar polaridad y correspondencia de interruptores y salidas.'),
('criterio-electrico-prueba-protecciones','Pruebas y recepción eléctrica','Protecciones','Funcionamiento','Comprobar interruptores automáticos y diferenciales.'),
('criterio-electrico-prueba-tension','Pruebas y recepción eléctrica','Circuitos','Tensión','Medir tensión y secuencia de fases antes de conectar equipos.'),
('criterio-electrico-prueba-caida-tension','Pruebas y recepción eléctrica','Carga','Caída de tensión','Investigar caídas anormales bajo carga en vez de aumentar la protección.'),
('criterio-electrico-termografia-tablero','Pruebas y recepción eléctrica','Tablero','Calentamiento','Revisar calentamientos o conexiones deficientes después de la puesta en servicio.'),
('criterio-electrico-acta-pruebas','Pruebas y recepción eléctrica','Entrega','Registro','Conservar resultados, instrumentos y fecha de las pruebas.'),
('criterio-electrico-fotos-ocultos','Pruebas y recepción eléctrica','Trabajos ocultos','Registro','Fotografiar canalizaciones y cajas antes del tarrajeo o cierre.'),
('criterio-electrico-plano-conforme-obra','Pruebas y recepción eléctrica','Documentación','Conforme a obra','Actualizar planos con cambios reales, recorridos y circuitos ejecutados.'),
('criterio-electrico-energizacion-controlada','Pruebas y recepción eléctrica','Puesta en servicio','Energización','Energizar por etapas, con circuitos identificados y cargas desconectadas inicialmente.')]
for i,c,e,p,t in items: regs.append(crit(i,c,e,p,t))

def main():
 b=json.loads(N.read_text()); q=json.loads(Q.read_text()); old={x['id'] for x in b['parametros']}; dup=old & {x['id'] for x in regs};
 if dup: raise SystemExit('Duplicados: '+','.join(sorted(dup)))
 allq=[x for c in q['categorias'] for x in c.get('preguntas',[])]; m=max(int(x['id'][1:]) for x in allq if re.fullmatch(r'q\d+',x['id']))
 cats={c['nombre']:c for c in q['categorias']}
 for n,r in enumerate(regs,1):
  qid=f'q{m+n}'; r['faq_relacionadas']=[qid]; b['parametros'].append(r)
  name=r['categoria']; cat=cats.get(name)
  if not cat: cat={'nombre':name,'preguntas':[]}; q['categorias'].append(cat); cats[name]=cat
  cat['preguntas'].append({'id':qid,'pregunta':f"¿Qué debo revisar sobre {r['parametro'].lower()} en {r['elemento'].lower()}?",'respuesta':r['valor']['texto']+' '+r['advertencia']})
 b['version']='2.5.0'; b['fecha_revision']='2026-07-27'
 if len(b['parametros'])!=1519: raise SystemExit(len(b['parametros']))
 if sum(len(c.get('preguntas',[])) for c in q['categorias'])!=2982: raise SystemExit('preguntas')
 N.write_text(json.dumps(b,ensure_ascii=False,separators=(',',':'))); Q.write_text(json.dumps(q,ensure_ascii=False,separators=(',',':')))
 s=C.read_text(); s=s.replace('if len(base.parametros) < 1447:','if len(base.parametros) < 1519:').replace('por lo menos 1447 parámetros revisados','por lo menos 1519 parámetros revisados').replace('if validados < 1192:','if validados < 1210:').replace('al menos 1192 numerales RNE validados','al menos 1210 numerales RNE validados').replace('if base.version != "2.4.0":','if base.version != "2.5.0":').replace('if criterios < 237:','if criterios < 291:').replace('al menos 237 criterios técnicos revisados','al menos 291 criterios técnicos revisados').replace('if len(todas) < 2910:','if len(todas) < 2982:').replace('por lo menos 2910 preguntas técnicas','por lo menos 2982 preguntas técnicas').replace('La versión normativa esperada es 2.4.0','La versión normativa esperada es 2.5.0')
 C.write_text(s)
 D.write_text('# Validación de instalaciones eléctricas en ejecución — 27 de julio de 2026\n\n## Alcance\n\nSe incorporaron **72 parámetros** y **72 preguntas** tras depurar la versión 2.4.0.\n\n## Contenido\n\n- proyecto, documentación y coordinación;\n- canalizaciones, cajas y pases;\n- conductores, empalmes e identificación;\n- tableros, circuitos y protecciones;\n- puesta a tierra y equipotencialidad;\n- tomacorrientes, luminarias y zonas húmedas;\n- continuidad, aislamiento, polaridad, tensión y pruebas funcionales;\n- registros fotográficos, actas y planos conforme a obra.\n\n## Fuentes\n\n- EM.010 Instalaciones Eléctricas Interiores — RM N.° 083-2019-VIVIENDA.\n- Formación oficial SENCICO sobre instalaciones eléctricas en edificaciones.\n\n## Resultado\n\n- Versión normativa: `2.5.0`.\n- Parámetros totales: `1519`.\n- Registros `validado_con_numeral`: `1210`.\n- Criterios técnicos revisados: `291`.\n- Preguntas técnicas: `2982`.\n\nLas buenas prácticas de montaje y ensayo se mantienen diferenciadas de las exigencias normativas.\n')
 print('Aplicados',len(regs))
if __name__=='__main__': main()
