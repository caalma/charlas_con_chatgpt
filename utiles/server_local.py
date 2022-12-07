#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from livereload import Server
import webbrowser
import yaml

with open('cfg.yml', 'r') as f:
    cfg = yaml.safe_load(f)

    r = cfg['ruta_publica']
    h = cfg['server']['host']
    p = cfg['server']['port']

    webbrowser.open(f'http://{h}:{p}')

    server = Server()
    server.watch(r)

    server.serve(root=r, host=h, port=p)
