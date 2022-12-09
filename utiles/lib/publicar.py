import yaml
from bs4 import BeautifulSoup
from .general import humanizar, agregar_metadatos_basicos, nuevo_tag
from os.path import basename, splitext


tags_a_eliminar = [
    #'img',
    'svg', 'script', 'link', 'style', 'form', 'button', 'next-route-announcer',
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
    'flex-grow flex-shrink-0',
    'text-xs text-black/50 dark:text-white/50 pt-2 pb-3 px-3 md:pt-3 md:pb-6 md:px-4 text-center'
    ]


def publicar_charlas(arc, cfg):
    with open(cfg['arc_registro'], 'r') as f:
        dat_registro = yaml.safe_load(f)

    with  open(arc, 'r') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html5lib')

        # eliminacion de tags innecesarios
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

    return soup
