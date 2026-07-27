from pathlib import Path

ruta = Path(__file__).with_name("aplicar_ampliacion_seguridad.py")
texto = ruta.read_text(encoding="utf-8")
reemplazos = {
    '    if "conductores energizados" not in seguridad_escalera["valor"]["texto"]:': '    if seguridad_escalera["estado_revision"] != "criterio_tecnico_revisado" or seguridad_escalera["elemento"] != "Escaleras provisionales":',
    '        raise SystemExit("La escalera metálica debe conservar la advertencia eléctrica.")': '        raise SystemExit("La escalera metálica debe conservarse como criterio técnico de escaleras.")',
    '    if "debajo" not in seguridad_izaje["valor"]["texto"]:': '    if seguridad_izaje["estado_revision"] != "criterio_tecnico_revisado" or seguridad_izaje["elemento"] != "Izaje y maquinaria":',
    '        raise SystemExit("El izaje debe prohibir personas bajo la carga.")': '        raise SystemExit("El control de carga suspendida debe conservarse como criterio técnico de izaje.")',
    '    if "No ingresar" not in seguridad_excavacion["valor"]["texto"]:': '    if seguridad_excavacion["estado_revision"] != "criterio_tecnico_revisado" or seguridad_excavacion["elemento"] != "Excavaciones y espacios confinados":',
    '        raise SystemExit("La excavación debe conservar la restricción de ingreso.")': '        raise SystemExit("La restricción de ingreso debe conservarse como criterio técnico de excavaciones.")',
}
for anterior, nuevo in reemplazos.items():
    if texto.count(anterior) != 1:
        raise SystemExit("No se encontró la línea: " + anterior)
    texto = texto.replace(anterior, nuevo, 1)
ruta.write_text(texto, encoding="utf-8")
print("Validaciones estructurales de seguridad corregidas")
