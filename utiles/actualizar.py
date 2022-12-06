#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from sys import argv
from os import listdir, remove
from os.path import basename, splitext, getmtime, exists, join
from time import ctime
from datetime import datetime
from shutil import move
from bs4 import BeautifulSoup
import webbrowser
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


def publicar(arc, destino):
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
            'ThreadLayout__BottomSpacer-sc-wfs93o-1'
            ]

        for sel in tags_a_eliminar:
            for it in soup.select(sel):
                it.extract()

        for sel in clases_a_eliminar:
            for it in soup.find_all(class_=sel):
                it.extract()

        # limpieza de atributos
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
        ar_res = f'{destino}{arc_nuevo}'
        with open(ar_res, 'w') as fw:
            fw.write(str(soup))

def hay_repeticion_de_nombres():
    global ruta_charlas_crudas
    global ruta_charlas_nuevas

    repetidos = []
    for arc in listdir(ruta_charlas_nuevas):
        ar_previo = f'{ruta_charlas_crudas}{arc}'
        if exists(ar_previo):
            repetidos.append(arc)

    hay_repetidos = len(repetidos) > 0
    if hay_repetidos:
        print('Estos archivos tienen nombres repetidos:\n  ' + '\n  '.join(repetidos))
        print('Cambia los nombre manualmente.')
    return hay_repetidos


def agregar_charlas():
    global ruta_charlas_crudas
    global ruta_charlas_nuevas
    global arc_registro

    formato = '%Y-%m-%d %H:%M:%S.%f -0300'

    for arc in listdir(ruta_charlas_nuevas):
        ruta_ar = f'{ruta_charlas_nuevas}{arc}'
        fecha = datetime.fromtimestamp(getmtime(ruta_ar)).strftime(formato)

        with open(arc_registro, 'a') as f:
            f.write(f"{arc}: '{fecha}'\n")

        ruta_ar_agregado = f'{ruta_charlas_crudas}{arc}'
        move(ruta_ar, ruta_ar_agregado)

        print(f'Agregado: {arc}')


def hacer_indice():
    global ruta_publica
    global ruta_charlas

    ruta_raiz = ruta_charlas.replace('/docs/', '/')

    titulo = 'Compilación de charlas exploratorias con ChatGPT'
    html_cabecera = f'<header><h2>{titulo}</h2></header>'
    html_notas = '<section class="notas"><p>Algunos comentarios y notas sobre las capacidades y dificultades encontradas los dejo en <a href="./notas.html">esta página</a>.</p></section>'
    html_charlas = '<section><h3>Charlas realizadas</h3><div class="charlas"></div></section>'
    html_base = f'<html><head><link href="./style.css" rel="stylesheet"/><title>{titulo}</title></head><body>{html_cabecera}{html_notas}{html_charlas}</body></html>'

    dom = BeautifulSoup(html_base, 'html5lib')
    agregar_metadatos_basicos(dom)

    tag_body = dom.find('body')
    tag_body.attrs['class'] = 'indice'

    tag_charlas = dom.find(class_='charlas')

    for ar in sorted(listdir(ruta_charlas)):
        tag = dom.new_tag('a')
        tag.attrs['href'] = f'{ruta_raiz}{ar}'
        tag.string = humanizar(splitext(ar)[0])
        tag_charlas.append(tag)

    with open(f'{ruta_publica}index.html', 'w') as fw:
        fw.write(str(dom))
        print('Índice actualizado.')


def hacer_notas():
    global ruta_publica
    global arc_notas

    ruta_raiz = ruta_charlas.replace('/docs/', '/')

    titulo = 'Notas sobre las charlas con ChatGPT'
    html_cabecera = f'<header><a class="menu" href="./"><span>&#x1F3E0;</span></a><h2>{titulo}</h2></header>'
    html_base = f'<html><head><link href="./style.css" rel="stylesheet"/><title>{titulo}</title></head><body>{html_cabecera}</body></html>'



    dom = BeautifulSoup(html_base, 'html5lib')
    agregar_metadatos_basicos(dom)

    tag_body = dom.find('body')
    tag_body.attrs['class'] = 'notas'

    with open(arc_notas, 'r') as f:
        notas = yaml.safe_load(f)

        for nota in notas:
            tex = nota['tex']
            enlaces = ''
            for url in nota['ref']:
                nom = basename(url)
                enlaces += f'<li><a href=".{url}">{nom}</a></li>'
            tex_html = f'<section class="nota"><div>{tex}</div><ul>{enlaces}</ul></section>'
            tag_body.append(BeautifulSoup(tex_html, 'html.parser'))

    with open(f'{ruta_publica}notas.html', 'w') as fw:
        fw.write(str(dom))
        print('Notas actualizadas.')

def vaciar_charlas_publicas():
    global ruta_charlas

    for arc in listdir(ruta_charlas):
        remove(join(ruta_charlas, arc))


ayuda = """
Las acciones diposnibles son:
ayuda              muestra este contenido
indice             reconstruye el índice general
notas              reconstruye la página de notas
publicar           limpia las charlas crudas y las pone públicas
publicar_nuevos    solo aplica limpieza a archivos no publicados
agregar            agrega las charlas nuevas y actualiza el registro
vaciar_charlas     elimina todas las charlas públicas
todo               activa: agregar, publicar, indice, notas

Si no se indican acciones se asume 'todo'.
Pueden indicarse más de una.
"""

if __name__ == '__main__':
    ruta_charlas_crudas = './charlas_crudas/'
    ruta_charlas_nuevas = './charlas_nuevas/'
    ruta_publica = './docs/'
    ruta_charlas = f'{ruta_publica}charlas/'
    arc_registro = './registro_temporal.yml'
    arc_notas = './notas.yml'

    with open(arc_registro, 'r') as f:
        dat_registro = yaml.safe_load(f)

    # definir acciones
    acciones = ['todo'] if len(argv) == 1 else argv[1:]
    if 'todo' in acciones:
        acciones = ['agregar', 'publicar', 'notas', 'indice']

    # mostrar ayuda
    if 'ayuda' in acciones:
        print(ayuda)
        quit()

    # agregar nuevas
    if 'agregar' in acciones:
        if not hay_repeticion_de_nombres():
            agregar_charlas()

    # recrear limpieza
    if 'publicar' in acciones:
        for arc in listdir(ruta_charlas_crudas):
            try:
                publicar(f'{ruta_charlas_crudas}{arc}', ruta_charlas)
                print(f'Publicado: {arc}')
            except Exception as error:
                print(f'Fallo la publicación de: {arc}.\n{error}')

    # recrear limpieza solo archivos nuevos
    if 'publicar_nuevos' in acciones:
        for arc in listdir(ruta_charlas_crudas):
            arc_a_agregar = f'{ruta_charlas}{arc}'

            if not exists(arc_a_agregar):
                try:
                    publicar(f'{ruta_charlas_crudas}{arc}', ruta_charlas)
                    print(f'Publicado: {arc}')
                except Exception as error:
                    print(f'Fallo la publicación de: {arc}.\n{error}')


    # vaciar charlas
    if 'vaciar_charlas' in acciones:
        vaciar_charlas_publicas()

    # reconstruir notas
    if 'notas' in acciones:
        hacer_notas()

    # reconstruir indice
    if 'indice' in acciones:
        hacer_indice()
