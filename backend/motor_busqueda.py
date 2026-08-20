#!/usr/bin/env python3
import json
import os
import sys
import argparse


def load_data():
    here = os.path.dirname(__file__)
    path = os.path.join(here, 'preguntas_tecnicas.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def search(data, keyword):
    kw = keyword.lower()
    results = []
    for cat in data.get('categorias', []):
        cat_name = cat.get('nombre', '')
        for p in cat.get('preguntas', []):
            pid = p.get('id', '')
            q = p.get('pregunta', '')
            a = p.get('respuesta', '')
            combined = ' '.join([q, a, cat_name]).lower()
            if kw in combined:
                results.append({'categoria': cat_name, 'id': pid, 'pregunta': q, 'respuesta': a})
    return results


def main():
    parser = argparse.ArgumentParser(description='Motor de búsqueda para preguntas técnicas')
    parser.add_argument('keyword', nargs='?', help='Palabra clave a buscar')
    args = parser.parse_args()

    data = load_data()

    if args.keyword:
        keyword = args.keyword
    else:
        try:
            keyword = input('Ingrese palabra clave: ').strip()
        except EOFError:
            sys.exit(0)

    if not keyword:
        print('No se ingresó ninguna palabra clave.')
        sys.exit(0)

    results = search(data, keyword)

    if not results:
        print(f'No se encontraron resultados para: "{keyword}"')
        sys.exit(0)

    print(f'{len(results)} resultado(s) encontrado(s) para "{keyword}":')
    for i, r in enumerate(results, 1):
        print('---')
        print(f'{i}. Categoría: {r["categoria"]}')
        print(f'ID: {r["id"]}')
        print(f'P: {r["pregunta"]}')
        print(f'R: {r["respuesta"]}')


if __name__ == '__main__':
    main()
