#!/usr/bin/env python
import os
import sqlite3
from bottle import Bottle, run, route, view, static_file, abort, template, SimpleTemplate

app = Bottle()

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='/root/projects/bottle-dev/bottle/www/static')

@app.route('/')
@view('home')
def home():
    return None

# Root directory you want to expose for listing
BASE_DIR = os.path.abspath('./static/uploads')

@app.route('/uploads/')
@app.route('/uploads/<subpath:path>')
def list_directory(subpath=''):
    target_path = os.path.normpath(os.path.join(BASE_DIR, subpath))

    # Security check: prevent directory traversal attacks
    if not target_path.startswith(BASE_DIR):
        return abort(403, "Access denied.")

    if os.path.isdir(target_path):
        try:
            items = os.listdir(target_path)
        except PermissionError:
            return abort(403, "Permission denied.")

        # Build simple HTML listing
        html = [f"<h2>Directory listing for /{subpath}</h2><ul>"]
        if subpath:
            parent_path = os.path.dirname(subpath)
            html.append(f'<li><a href="/uploads/{parent_path}">[Up one level]</a></li>')

        for item in sorted(items):
            item_path = os.path.join(subpath, item)
            html.append(f'<li><a href="/uploads/{item_path}">{item}</a></li>')
        html.append("</ul>")
        return "".join(html)

    elif os.path.isfile(target_path):
        directory = os.path.dirname(target_path)
        filename = os.path.basename(target_path)
        return static_file(filename, root=directory)
    else:
        return abort(404, "File not found.")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=14344, debug=True)
