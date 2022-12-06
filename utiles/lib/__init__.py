from time import ctime
from datetime import datetime
from shutil import move
from bs4 import BeautifulSoup
from os import listdir, remove
from os.path import basename, splitext, getmtime, exists, join
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


def publicar(arc, cfg):

    with open(cfg['arc_registro'], 'r') as f:
        dat_registro = yaml.safe_load(f)

    with  open(arc, 'r') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html5lib')

        # eliminacion de tags innecesarios
        tags_a_eliminar = [
            'svg', 'script', 'link', 'style', 'form', 'button', 'img', 'next-route-announcer',
            'meta', 'noscript', 'deepl-inline-translate', 'deepl-inline-popup',
            'deepl-inline-trigger'
            ]
        clases_a_eliminar = [

            'Thread__PositionForm-sc-15plnpr-3',
            'hidden md:fixed md:inset-y-0 md:flex md:w-52 md:flex-col bg-gray-900',
            'Pagination__PaginationState-sc-q79nhy-2',
            'ConversationItem__Role-sc-18srrdc-2',
            'ConversationItem__ActionButtons-sc-18srrdc-4',
            'ThreadLayout__BottomSpacer-sc-wfs93o-1',
            'flex-grow flex-shrink-0'
            ]

        for sel in tags_a_eliminar:
            for it in soup.select(sel):
                it.extract()

        for sel in clases_a_eliminar:
            for it in soup.find_all(class_=sel):
                it.extract()

        # limpieza de atributos
        if 'ConversationItem__ConversationItemWrapper' in html:
            soup = limpiar_tags_modelo_1(soup)
        else:
            soup = limpiar_tags_modelo_2(soup)

        # tags a modificar
        tag_head = soup.find('head')
        tag_body = soup.find('body')
        tag_title = soup.find('title')

        # actualizacion de titulo
        titulo = 'ChatGPT : ' +  humanizar(basename(splitext(arc)[0]))
        tag_title.string = titulo

        # insertar estilo
        tag_head.append(nuevo_tag(soup, 'link',
                                  {'href': '../style.css',
                                  'rel': 'stylesheet'}))

        # insert metadatos
        agregar_metadatos_basicos(soup)

        # insertar cabecera
        tag_cab = soup.new_tag('header')
        tag_menu = soup.new_tag('a')
        tag_menu.attrs['class'] = 'menu'
        tag_menu.attrs['href'] = '../'
        tag_menu.append(BeautifulSoup('<span>&#x1F3E0;</span>', 'html.parser'))
        tag_cab.append(tag_menu)
        tag_cab.append(BeautifulSoup(f'<h2>{titulo}</h2>', 'html.parser'))

        nom_arc = basename(arc)
        if nom_arc in dat_registro:
            fecha_de_charla = dat_registro[nom_arc]
            tag_cab.find('h2').append(BeautifulSoup(f'<span>Realizada el {fecha_de_charla} </span>', 'html.parser'))

        tag_body.insert(0, tag_cab)

        # grabar resultado
        arc_nuevo = basename(arc)
        rcp = cfg['ruta_charlas_publicas']
        with open(f'{rcp}{arc_nuevo}', 'w') as fw:
            fw.write(str(soup))

        print(f'Publicado: {arc}')

def limpiar_tags_modelo_1(soup):
    indice_de_mensaje = 0
    for tag in soup.find_all(['div', 'main', 'html']):
        tclass = tag.get('class')
        if tclass :
            if 'ConversationItem__ConversationItemWrapper-sc-18srrdc-0' in tag['class']:
                indice_de_mensaje += 1
                emisor = 'gpt' if 'bg-gray-50' in tag['class'] else 'otro'
                tag['class'] = f'mensaje {emisor}'
                tag_ancla = soup.new_tag('a')
                tag_ancla.attrs['href'] = f'#m{indice_de_mensaje}'
                tag_ancla.attrs['class'] = 'ref-mensaje'
                tag.insert(0, tag_ancla)
                tag.attrs['id'] = f'm{indice_de_mensaje}'
            else:
                del tag['class']
                del tag['id']
        else:
            del tag['id']

        del tag['style']

    for tag in soup.find_all('div'):
        tclass = tag.get('class')
        if not tclass:
            tag.unwrap()

    return soup

def limpiar_tags_modelo_2(soup):
    indice_de_mensaje = 0
    for tag in soup.find_all(['div', 'main', 'html']):
        tclass = tag.get('class')
        if tclass :
            if 'border-black/10' in tag['class']:
                indice_de_mensaje += 1
                emisor = 'gpt' if 'bg-gray-50' in tag['class'] else 'otro'
                tag['class'] = f'mensaje {emisor}'
                tag_ancla = soup.new_tag('a')
                tag_ancla.attrs['href'] = f'#m{indice_de_mensaje}'
                tag_ancla.attrs['class'] = 'ref-mensaje'
                tag.insert(0, tag_ancla)
                tag.attrs['id'] = f'm{indice_de_mensaje}'
            else:
                del tag['class']
                del tag['id']
        else:
            del tag['id']

        del tag['style']

    #for tag in soup.find_all('div'):
    #    tclass = tag.get('class')
    #    if not tclass:
    #        tag.unwrap()

       #  border-b  dark:border-gray-900/50 text-gray-800 dark:text-gray-100
    return soup


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


def agregar_charlas(cfg):
    rcc = cfg['ruta_charlas_crudas']
    rcn = cfg['ruta_charlas_nuevas']
    rar = cfg['arc_registro']

    formato = '%Y-%m-%d %H:%M:%S.%f -0300'

    for arc in listdir(rcn):
        if arc.endswith('.html'):
            r_arc = f'{rcn}{arc}'
            fecha = datetime.fromtimestamp(getmtime(r_arc)).strftime(formato)

            with open(rar, 'a') as f:
                f.write(f"{arc}: '{fecha}'\n")

            r_arc_agregado = f'{rcc}{arc}'
            move(r_arc, r_arc_agregado)

            print(f'Agregado: {arc}')

def hacer_indice(cfg):
    rpu = cfg['ruta_publica']
    rcp = cfg['ruta_charlas_publicas']

    ruta_raiz = rcp.replace('../docs/', '/')

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


def hacer_notas(cfg):
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

def vaciar_charlas_publicas(cfg):
    rcp = cfg['ruta_charlas_publicas']

    for arc in listdir(rcp):
        remove(join(rcp, arc))
