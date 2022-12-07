from os.path import splitext
from datetime import datetime
from bs4 import BeautifulSoup
from os import listdir
from .general import humanizar, agregar_metadatos_basicos


def hacer(cfg):
    rpu = cfg['ruta_publica']
    rcp = cfg['ruta_charlas_publicas']

    ruta_raiz = rcp.replace('../docs/', './')

    formato = '%Y-%m-%d %H:%M:%S.%f -0300'

    fecha_de_actualizacion = datetime.now().strftime(formato)

    titulo = 'Compilación de charlas exploratorias con ChatGPT'
    html_cabecera = f'<header><div><h2>{titulo}</h2><p><small>ÚLTIMA ACUTUALIZACIÓN: {fecha_de_actualizacion}</small></p></div></header>'
    html_notas = '<section class="notas"><p>Algunos comentarios y notas sobre las capacidades y dificultades encontradas los dejo en <a href="./notas.html">esta página</a>.</p></section>'
    html_charlas = '<section><h3>Charlas realizadas</h3><div class="charlas"></div></section>'
    html_base = f'<html><head><link href="./style.css" rel="stylesheet"/><title>{titulo}</title></head><body>{html_cabecera}{html_notas}{html_charlas}</body></html>'

    dom = BeautifulSoup(html_base, 'html5lib')
    agregar_metadatos_basicos(dom)

    tag_body = dom.find('body')
    tag_body.attrs['class'] = 'indice'

    tag_charlas = dom.find(class_='charlas')

    for ar in sorted(listdir(rcp)):
        tag = dom.new_tag('a')
        tag.attrs['href'] = f'{ruta_raiz}{ar}'
        tag.string = humanizar(splitext(ar)[0])
        tag_charlas.append(tag)

    with open(f'{rpu}index.html', 'w') as fw:
        fw.write(str(dom))
        print('Índice actualizado.')
