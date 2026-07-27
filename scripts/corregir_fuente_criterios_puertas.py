from pathlib import Path

ruta = Path(__file__).with_name("aplicar_ampliacion_puertas_ventanas.py")
texto = ruta.read_text(encoding="utf-8")
anterior = '"tipo": "manual_oficial",\n            "norma": "Formación técnica SENCICO",'
nuevo = '"tipo": "criterio_tecnico",\n            "norma": "Formación técnica SENCICO",'
if texto.count(anterior) != 1:
    raise SystemExit("No se encontró una única fuente de criterio para corregir.")
texto = texto.replace(anterior, nuevo, 1)
ruta.write_text(texto, encoding="utf-8")
print("Fuente de criterios corregida a criterio_tecnico.")
