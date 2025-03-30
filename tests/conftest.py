import os
import sys

test_dir = os.path.dirname(__file__)
root_dir = os.path.dirname(test_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)


import pytest
from core.config import db
from core.utils import create_app
from services.config import register_services
from services.auth.queries import init_users


@pytest.fixture
def app():
    """Fixture qui crée une instance de l'application Flask pour les tests."""
    app = create_app('test', env_name='test')
    with app.app_context():
        init_users()

    register_services(app)
    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Client de test Flask pour envoyer des requêtes API."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Fixture pour le CLI runner de Flask."""
    return app.test_cli_runner()

