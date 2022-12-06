#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from livereload import Server
import webbrowser

if __name__ == '__main__':
    ruta = '../docs/'
    host = 'localhost'
    port = 9998

    webbrowser.open(f'http://{host}:{port}')

    server = Server()
    server.watch(ruta)

    server.serve(root=ruta, host=host, port=port)
