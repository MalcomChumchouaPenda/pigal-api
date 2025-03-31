import os
import json
from functools import wraps
from datetime import datetime
from importlib import import_module

from flask import Flask, Blueprint, session
from flask import jsonify, redirect, url_for
from flask_paginate import Pagination
from flask_login import current_user, login_required
from flasgger import swag_from
import markdown as md

from .config import config, babel, swagger
from .config import db, migrate
from .config import login_manager, principal
from .constants import PAGES_DIR, SERVICES_DIR, ENCODINGS, CORE_DIR


def create_app(name, env_name='dev'):
    # Initialisation de Flask
    app = Flask(name,
                static_folder='core/static',
                template_folder='core/templates')
    app.config.from_object(config[env_name])
    # print(app.root_path)

    # initialisation de la securite
    login_manager.init_app(app)
    principal.init_app(app)

    # initialisation de la documentation des api
    app.config['SWAGGER'] = {
        'title': 'Pigal API',
        "description": "Pigal API documentation",
        "version": "1.0.0",
        'uiversion': 3,
        'openapi': '3.0.9'
    }
    swagger.init_app(app=app)

    # initialisation des langues
    babel.init_app(app, locale_selector=get_locale)

    # ajout des fonctions utilitaires et constantes
    app.jinja_env.globals.update(get_locale=get_locale)
    app.jinja_env.globals.update(default_deadline=default_deadline)
    app.jinja_env.globals.update(url_for_entry=url_for_entry)
    # app.jinja_env.globals.update(JINJA_CONSTANTS)

    # pages or services registration
    register_services(app)
    register_pages(app)
    
    # initialisation de la base de donnees
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        if env_name in ['dev', 'test']:
            db.drop_all()
            print('drop all table')
        db.create_all()
        print('create all table')
        if env_name in ['dev', 'prod']:
            init_data()
    return app


# PAGES REGISTRATION

def register_pages(app):
    if os.path.isdir(PAGES_DIR):
        print('Register pages')


# SERVICES REGISTRATION

def register_services(app):
    if os.path.isdir(SERVICES_DIR):
        for name in os.listdir(SERVICES_DIR):
                try:
                    modulename = f'services.{name}.routes'
                    module = import_module(modulename)
                    api = getattr(module, 'api')
                    prefix = '/auth' if name == 'auth' else f'/{name}-api'
                    app.register_blueprint(api, url_prefix=prefix)
                    print('Register service:', name)
                except (ModuleNotFoundError, AttributeError):
                    continue

def init_data():
    if os.path.isdir(SERVICES_DIR):
        for name in os.listdir(SERVICES_DIR):
            try:
                modulename = f'services.{name}.defaults'
                module = import_module(modulename)
                getattr(module, 'init_data')()
                print('Init data:', name)
            except (ModuleNotFoundError, AttributeError):
                continue


# BLUEPRINT FACTORY METHODS +  SECURITY METHODS

def create_ui(name, importname):
    return Ui(name, importname, 
              template_folder='templates', 
              static_folder='static')


class Ui(Blueprint):

    @classmethod
    def roles_accepted(cls, *roles):
        """Décorateur pour protéger les routes Flask qui renvoient des pages HTML."""
        def decorator(f):
            @wraps(f)
            @login_required
            def decorated_function(*args, **kwargs):
                if not current_user.is_authenticated:
                    msg = "Vous devez être connecté pour accéder à cette page."
                    return redirect(url_for("home.login", message=msg))  # Redirection vers la page de connexion
                if len([n for n in roles if current_user.has_role(n)]) == 0:
                    msg = "Vous n'avez pas la permission d'accéder à cette page."
                    return redirect(url_for("home.denied", message=msg))  # Redirection vers la page d'accueil
                return f(*args, **kwargs)
            return decorated_function
        return decorator


def create_api(name, importname):
    return Api(name, importname)


class Api(Blueprint):

    @classmethod
    def roles_accepted(cls, *roles):
        """Décorateur pour protéger les routes API avec des rôles spécifiques."""
        def decorator(f):
            @wraps(f)
            @login_required
            def decorated_function(*args, **kwargs):
                if not current_user.is_authenticated:
                    return jsonify({'message': 'Unauthorized'}), 401
                if len([n for n in roles if current_user.has_role(n)]) == 0:
                    return jsonify({'message': 'Forbidden'}), 403
                return f(*args, **kwargs)
            return decorated_function
        return decorator

    @classmethod
    def docs(cls, docname, methods=['GET']):
        """Décorateur pour protéger les routes API avec des rôles spécifiques."""
        docname = './docs/' + docname
        return swag_from(docname, methods=methods)
    

# FILES I/O METHODS

def get_path(filepath):
    if filepath.startswith('/pages/'):
        nexpath = os.path.normpath(filepath.replace('/pages/', ''))
        filepath = os.path.join(PAGES_DIR, nexpath)
    elif filepath.startswith('/services/'):
        nexpath = os.path.normpath(filepath.replace('/services/', ''))
        filepath = os.path.join(SERVICES_DIR, nexpath)
    elif filepath.startswith('/core/'):
        nexpath = os.path.normpath(filepath.replace('/core/', ''))
        filepath = os.path.join(CORE_DIR, nexpath)
    return filepath

def _use_encodings(filepath, encoding):
    text, valid = None, None
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            text = f.read()
        valid = True
    except UnicodeDecodeError:
        pass
    return text, valid

def _search_encodings(filepath):
    for encoding in ENCODINGS:
        text, valid = _use_encodings(filepath, encoding)
        if valid:
            break
    return text, valid


def read_text(filepath, encoding='utf-8', coerce=True):
    filepath = get_path(filepath)
    text, valid = _use_encodings(filepath, encoding)
    if not valid and coerce:
        text, valid = _search_encodings(filepath)
    if not valid:
        raise RuntimeError(f'Unable to read text in {filepath}')
    return text

def read_json(filepath, encoding='utf-8', coerce=True):
    text = read_text(filepath, encoding=encoding, coerce=coerce)
    data = json.loads(text)
    return data

def read_markdown(filepath, encoding='utf-8', coerce=True):
    text = read_text(filepath, encoding=encoding, coerce=coerce)
    return md.markdown(text)

def is_file(filename):
    filepath = get_path(filename)
    return os.path.isfile(filepath)



# OTHERS METHODS

def get_locale():
    lang = session.get('lang', 'fr')
    return lang

def default_deadline():
    now = datetime.now()
    return f'{now.year}/12/31'

def paginate_items(items, page, per_page=10):
    offset = (page - 1) * per_page
    page_items = items[offset: offset + per_page]
    page_total = len(page_items)
    total = len(items)
    info = f'{offset+1} à {offset + page_total} résultats sur {total}'
    pagination = Pagination(page=page, per_page=per_page, total=total, 
                            css_framework='bootstrap5', display_msg=info)
    return page_items, pagination

def url_for_entry(entry, default='#'):
    if 'point' in entry:
        kwargs = entry.get('kwargs', {})
        return url_for(entry['point'], **kwargs)
    return entry.get('url', default)


