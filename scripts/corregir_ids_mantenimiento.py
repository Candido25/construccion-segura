from pathlib import Path

ruta = Path(__file__).with_name("ampliar_mantenimiento_vida_util.py")
texto = ruta.read_text(encoding="utf-8")
anterior = '    for rid, elemento, nombre_parametro, pregunta, respuesta in inventario["practicas"]:\n        if rid in ids or not aceptar(pregunta):'
nuevo = '    for rid, elemento, nombre_parametro, pregunta, respuesta in inventario["practicas"]:\n        rid = re.sub(r"[^a-z0-9]+", "-", normalizar(rid)).strip("-")\n        if rid in ids or not aceptar(pregunta):'
if texto.count(anterior) != 1:
    raise SystemExit("No se encontró el bucle de prácticas de mantenimiento")
ruta.write_text(texto.replace(anterior, nuevo, 1), encoding="utf-8")
print("Identificadores de mantenimiento normalizados")
