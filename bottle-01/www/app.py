#!/usr/bin/env python3.12
from bottle import route, run, template, view, static_file, SimpleTemplate

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='/home/fria/projects/bottle/www/static')

@route('/')
@view('home')
def home():
    return None

if __name__ == '__main__':
    run(host='0.0.0.0', port=14344)
