import csv
import json
import os

ruta_csv = 'backend/datos.csv'
ruta_json = 'backend/preguntas_tecnicas.json'

def convertir_csv_a_json():
    categorias_dict = {}
    contador_id = 1

    try:
        with open(ruta_csv, mode='r', encoding='utf-8-sig') as archivo_csv:
            # Aquí le decimos a Python que use el punto y coma como separador
            lector = csv.DictReader(archivo_csv, delimiter=';')
            
            for fila in lector:
                # Aquí le indicamos que busque la columna exactamente con su tilde
                cat = fila['Categoría'].strip()
                preg = fila['Pregunta'].strip()
                resp = fila['Respuesta'].strip()
                
                if cat not in categorias_dict:
                    categorias_dict[cat] = []
                    
                categorias_dict[cat].append({
                    "id": f"q{contador_id}",
                    "pregunta": preg,
                    "respuesta": resp
                })
                contador_id += 1
                
        formato_final = {"categorias": []}
        for nombre_cat, lista_preguntas in categorias_dict.items():
            formato_final["categorias"].append({
                "nombre": nombre_cat,
                "preguntas": lista_preguntas
            })
            
        with open(ruta_json, mode='w', encoding='utf-8') as archivo_json:
            json.dump(formato_final, archivo_json, indent=2, ensure_ascii=False)
            
        print(f"¡Éxito total! Se procesaron {contador_id - 1} preguntas.")
        print("El archivo 'preguntas_tecnicas.json' ha sido actualizado y estructurado correctamente.")
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_csv}. Asegúrate de que esté en la carpeta 'backend'.")
    except KeyError as e:
        print(f"Error estructural: No se encontró la columna {e}. Verifica los encabezados en tu Excel/CSV.")

if __name__ == "__main__":
    convertir_csv_a_json()