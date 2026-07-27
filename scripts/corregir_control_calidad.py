from pathlib import Path

ruta = Path(__file__).with_name("ampliar_control_calidad_cierre.py")
texto = ruta.read_text(encoding="utf-8")
anterior = '    if calidad_asbuilt["elemento"] != "Planos conforme a obra":'
nuevo = '    if calidad_asbuilt["parametro"] != "Planos conforme a obra":'
if texto.count(anterior) != 1:
    raise SystemExit("No se encontró la comprobación de planos conforme a obra")
ruta.write_text(texto.replace(anterior, nuevo, 1), encoding="utf-8")
print("Comprobación de planos conforme a obra corregida")
