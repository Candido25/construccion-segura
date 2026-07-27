from pathlib import Path

ruta = Path(__file__).with_name("aplicar_ampliacion_puertas_ventanas.py")
texto = ruta.read_text(encoding="utf-8")
reemplazos = {
    "if len(registros) != 84:": "if len(registros) != 85:",
    "Se esperaban 84 registros": "Se esperaban 85 registros",
    "(1603, 3066, 1229, 356)": "(1604, 3067, 1230, 356)",
    "if len(base.parametros) < 1603:": "if len(base.parametros) < 1604:",
    "por lo menos 1603 parámetros revisados": "por lo menos 1604 parámetros revisados",
    "if validados < 1229:": "if validados < 1230:",
    "al menos 1229 numerales RNE validados": "al menos 1230 numerales RNE validados",
    "if len(todas) < 3066:": "if len(todas) < 3067:",
    "por lo menos 3066 preguntas técnicas": "por lo menos 3067 preguntas técnicas",
}
for anterior, nuevo in reemplazos.items():
    if texto.count(anterior) != 1:
        raise SystemExit(f"No se encontró una única coincidencia: {anterior}")
    texto = texto.replace(anterior, nuevo, 1)
ruta.write_text(texto, encoding="utf-8")
print("Conteos corregidos a 85 registros.")
