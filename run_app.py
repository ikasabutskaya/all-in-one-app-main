import os
import sys
import bottle

from beaker.middleware import SessionMiddleware
from bottle import route, run, static_file, template

from src import config, connector_db

# root directory of the app, needs for correct routing of static files (e.g. images)
dir_name = os.path.dirname(sys.argv[0])


@route('/')
@route('/index')
def page_main():
    client = get_all_clients()
    content = {
        'clients': client if client else [],
        'current_user': 'username',
        'app_version': '0.0.1'
    }
    return template('index', content)


def get_all_clients():
    my_sql_statement = 'select * from public.clients;'
    return connector_db.execute_statement(my_sql_statement)


@route('/img/<filename:re:.*\.png>')
@route('/img/<filename:re:.*\.jpg>')
def send_img(filename):
    return static_file(filename, root=dir_name + '/static/img')


@route('/js/<filename:re:.*\.js>')
def send_js(filename):
    return static_file(filename, root=dir_name + '/static/js')


@route('/favicon.ico')
def send_favicon():
    return static_file('favicon.ico', root=dir_name + '/static')


# Session settings
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': '../.session_data',
    'session.auto': True
}

run(server='paste', app=SessionMiddleware(bottle.app(), session_opts), host=config.HOST, reloader=False,
    port=config.PORT, debug=False)
