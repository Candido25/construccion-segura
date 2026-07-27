from pathlib import Path

ruta = Path(__file__).with_name("aplicar_ampliacion_seguridad.py")
texto = ruta.read_text(encoding="utf-8")
anterior = '''    seguridad_esmeril = api.detalle_parametro_normativo("criterio-seguridad-esmeril-guarda")
    if "guarda" not in seguridad_esmeril["valor"]["texto"]:
        raise SystemExit("El esmeril debe conservar la exigencia de guarda.")
'''
nuevo = '''    seguridad_esmeril = api.detalle_parametro_normativo("criterio-seguridad-esmeril-guarda")
    if seguridad_esmeril["estado_revision"] != "criterio_tecnico_revisado" or seguridad_esmeril["elemento"] != "Herramientas y equipos":
        raise SystemExit("La guarda del esmeril debe conservarse como criterio técnico de herramientas.")
'''
if texto.count(anterior) != 1:
    raise SystemExit("No se encontró el bloque de validación del esmeril")
ruta.write_text(texto.replace(anterior, nuevo, 1), encoding="utf-8")
print("Validación del esmeril corregida")
