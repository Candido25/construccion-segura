from pathlib import Path

ruta = Path(__file__).with_name("aplicar_ampliacion_seguridad.py")
texto = ruta.read_text(encoding="utf-8")
linea_condicion = '    if "guarda" not in seguridad_esmeril["valor"]["texto"]:'
linea_error = '        raise SystemExit("El esmeril debe conservar la exigencia de guarda.")'
nueva_condicion = '    if seguridad_esmeril["estado_revision"] != "criterio_tecnico_revisado" or seguridad_esmeril["elemento"] != "Herramientas y equipos":'
nuevo_error = '        raise SystemExit("La guarda del esmeril debe conservarse como criterio técnico de herramientas.")'
if texto.count(linea_condicion) != 1 or texto.count(linea_error) != 1:
    raise SystemExit("No se encontraron las líneas de validación del esmeril")
texto = texto.replace(linea_condicion, nueva_condicion, 1).replace(linea_error, nuevo_error, 1)
ruta.write_text(texto, encoding="utf-8")
print("Validación del esmeril corregida")
