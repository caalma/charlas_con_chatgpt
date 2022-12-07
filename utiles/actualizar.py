#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from sys import argv
from os import listdir
from os.path import exists
import yaml
from lib import (
    hay_repeticion_de_nombres,
    hacer_notas, hacer_indice,
    publicar_charlas, agregar_charlas,
    vaciar_charlas_publicas)

ayuda = """
Las acciones diposnibles son:
ayuda              muestra este contenido
indice             reconstruye el índice general
notas              reconstruye la página de notas
publicar           limpia las charlas crudas y las pone públicas
publicar_nuevos    solo aplica limpieza a archivos no publicados
agregar            agrega las charlas nuevas y actualiza el registro
vaciar_charlas     elimina todas las charlas públicas
todo               activa: agregar, publicar_nuevos, indice, notas

Si no se indican acciones se asume 'todo'.
Pueden indicarse más de una.
"""

if __name__ == '__main__':
    # definir acciones
    acciones = ['ayuda'] if len(argv) == 1 else argv[1:]
    if 'todo' in acciones:
        acciones = ['agregar', 'publicar_nuevos', 'notas', 'indice']

    if 'publicar_nuevos' in acciones:
        acciones.append('publicar')

    # mostrar ayuda
    if 'ayuda' in acciones:
        print(ayuda)
        quit()

    # carga configuracion y registro
    with open('cfg.yml', 'r') as f:
        cfg = yaml.safe_load(f)

    # agregar nuevas
    if 'agregar' in acciones:
        if not hay_repeticion_de_nombres(cfg):
            agregar_charlas(cfg)

    # recrear limpieza
    if 'publicar' in acciones:
        rcc = cfg['ruta_charlas_crudas']
        rch = cfg['ruta_charlas_publicas']

        for arc in listdir(rcc):
            arc_crudo = f'{rcc}{arc}'
            arc_publico = f'{rch}{arc}'
            try:
                if 'publicar_nuevos' in acciones:
                    if not exists(arc_publico):
                        publicar_charlas(arc_crudo, cfg)
                else:
                    publicar_charlas(arc_crudo, cfg)

            except Exception as error:
                print(f'Fallo la publicación de: {arc} .\n{error}')

    # vaciar charlas
    if 'vaciar_charlas' in acciones:
        vaciar_charlas_publicas(cfg)

    # reconstruir notas
    if 'notas' in acciones:
        hacer_notas(cfg)

    # reconstruir indice
    if 'indice' in acciones:
        hacer_indice(cfg)
