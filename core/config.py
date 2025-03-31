import os
import re

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_principal import Principal
from flask_babel import Babel
from flask_migrate import Migrate
from flasgger import Swagger

from .constants import (
    SERVICES_DIR, 
    STORE_DIR, 
    ROOT_DIR, 
    TESTS_DIR
)

# database objects
db = SQLAlchemy()
migrate = Migrate()

# security objects
login_manager = LoginManager()
principal = Principal()

# internationalization objects
babel = Babel()

# api cdocumentation object
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
swagger = Swagger(config=swagger_config)


# default database
_MYSQL_USER = os.getenv('MYSQL_USER')
_MYSQL_PWD = os.getenv('MYSQL_PWD')
_DEFAULT_TEST_DB = "sqlite:///:memory:"
_DEFAULT_DEV_DB = f"sqlite:///{os.path.join(STORE_DIR, 'default.db')}"
_DEFAULT_PROD_DB = f"mysql://{_MYSQL_USER}:{_MYSQL_PWD}@localhost/default"

# services databases
_DEV_BINDS = {}
_PROD_BINDS = {}
_TEST_BINDS = {}
for name in os.listdir(SERVICES_DIR):
    api_dir = os.path.join(SERVICES_DIR, name)
    if name == 'auth':
        dbname = 'auth'
    else:
        dbnames = re.findall('([a-z][a-z0-9]*)_v[0-9_]+', name)
        if len(dbnames) != 1:
            continue
        dbname = dbnames[0]
    _DEV_BINDS[dbname] = f"sqlite:///{os.path.join(STORE_DIR, dbname + '.db')}"
    _PROD_BINDS[dbname] = f"mysql://{_MYSQL_USER}:{_MYSQL_PWD}@localhost/{dbname}"
    _TEST_BINDS[dbname] = f"sqlite:///{os.path.join(TESTS_DIR, 'data', dbname + '.db')}"


class Config:

    # Configurations Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  # À changer en prod
    SESSION_TYPE = 'filesystem'  # Pour stocker les sessions

    # configuration babel
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'fr'  # Langue par défaut
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    BABEL_TRANSLATION_DIRECTORIES = os.path.join(ROOT_DIR, 'translations')


class ProdConfig(Config):

    # configuration sqlalchemy
    SQLALCHEMY_DATABASE_URI = _DEFAULT_PROD_DB
    SQLALCHEMY_BINDS = _PROD_BINDS
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):

    # configuration sqlalchemy
    SQLALCHEMY_DATABASE_URI = _DEFAULT_DEV_DB
    SQLALCHEMY_BINDS = _DEV_BINDS
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):

    # configuration sqlalchemy
    SQLALCHEMY_DATABASE_URI = _DEFAULT_TEST_DB
    SQLALCHEMY_BINDS = _TEST_BINDS
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Désactiver CSRF pour les tests API
    TESTING = True
    WTF_CSRF_ENABLED = False 


config = {
    'dev':DevConfig,
    'test':TestConfig,
    'prod':ProdConfig
}
