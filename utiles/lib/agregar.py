from shutil import move
from datetime import datetime
from os import listdir
from os.path import getmtime

def agregar_charlas(cfg):
    rcc = cfg['ruta_charlas_crudas']
    rcn = cfg['ruta_charlas_nuevas']
    rar = cfg['arc_registro']

    formato = '%Y-%m-%d %H:%M:%S.%f -0300'

    archivos_disponibles = [a for a in listdir(rcn) if a.endswith('.html')]

    if not archivos_disponibles:
        print('No hay charlas nuevas que agregar.')

    for arc in archivos_disponibles:
        r_arc = f'{rcn}{arc}'
        fecha = datetime.fromtimestamp(getmtime(r_arc)).strftime(formato)

        with open(rar, 'a') as f:
            f.write(f"{arc}: '{fecha}'\n")

        r_arc_agregado = f'{rcc}{arc}'
        move(r_arc, r_arc_agregado)

        print(f'Agregado: {arc} .')
