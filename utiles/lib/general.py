from os import listdir, remove
from os.path import exists, join
import yaml


def humanizar(text):
    text = text.replace('_', ' ')
    return text.capitalize()

def nuevo_tag(dom, name, attributes={}):
    tag = dom.new_tag(name)
    for k, v in attributes.items():
        tag.attrs[k] = v
    return tag

def agregar_metadatos_basicos(dom):
    tag = dom.find('head')
    tag.append(nuevo_tag(dom, 'meta',
                         {'charset': 'utf-8'}))
    tag.append(nuevo_tag(dom, 'meta',
                         {'name':'viewport',
                          'content':'width=device-width, initial-scale=1'
                         }))
    tag.append(nuevo_tag(dom, 'meta',
                         {'name':'format-detection',
                          'content':'telephone=no, email=no'
                         }))
    tag.append(nuevo_tag(dom, 'meta',
                         {'name':'mobile-web-app-capable',
                          'content':'yes'
                         }))

def hay_repeticion_de_nombres(cfg):
    rcc = cfg['ruta_charlas_crudas']
    rcn = cfg['ruta_charlas_nuevas']

    repetidos = []
    for arc in listdir(rcn):
        ar_previo = f'{rcc}{arc}'
        if exists(ar_previo):
            repetidos.append(arc)

    hay_repetidos = len(repetidos) > 0
    if hay_repetidos:
        print('Estos archivos tienen nombres repetidos:\n  ' + '\n  '.join(repetidos))
        print('Cambia los nombre manualmente.')
    return hay_repetidos

def vaciar_charlas_publicas(cfg):
    rcp = cfg['ruta_charlas_publicas']

    for arc in listdir(rcp):
        remove(join(rcp, arc))


def registros_temporales(cfg):
    with open(cfg['arc_registro'], 'r') as f:
        return yaml.safe_load(f)
