import yaml
from bs4 import BeautifulSoup
from os.path import basename
from .general import agregar_metadatos_basicos


def hacer(cfg):
    rpu = cfg['ruta_publica']
    rar = cfg['arc_notas']
    rcp = cfg['ruta_charlas_publicas']

    ruta_raiz = rcp.replace('/docs/', '/')

    titulo = 'Notas sobre las charlas con ChatGPT'
    html_cabecera = f'<header><a class="menu" href="./"><span>&#x1F3E0;</span></a><h2>{titulo}</h2></header>'
    html_base = f'<html><head><link href="./style.css" rel="stylesheet"/><title>{titulo}</title></head><body>{html_cabecera}</body></html>'

    dom = BeautifulSoup(html_base, 'html5lib')
    agregar_metadatos_basicos(dom)

    tag_body = dom.find('body')
    tag_body.attrs['class'] = 'notas'

    with open(rar, 'r') as f:
        notas = yaml.safe_load(f)

        for nota in notas:
            tex = nota['tex']
            enlaces = ''
            for url in nota['ref']:
                nom = basename(url)
                enlaces += f'<li><a href=".{url}">{nom}</a></li>'
            tex_html = f'<section class="nota"><div>{tex}</div><ul>{enlaces}</ul></section>'
            tag_body.append(BeautifulSoup(tex_html, 'html.parser'))

    with open(f'{rpu}notas.html', 'w') as fw:
        fw.write(str(dom))
        print('Notas actualizadas.')
