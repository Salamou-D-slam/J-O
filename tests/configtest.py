import pytest
import sys
import os

# Ajouter le dossier racine au PYTHONPATH pour que Python trouve app/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import create_app, db

@pytest.fixture
def client():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "postgresql+psycopg2://jo_admin:joadmin2024@localhost:5432/jo_test",
        "WTF_CSRF_ENABLED": False,
    }
    app = create_app(test_config)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        try:
            yield client
        finally:
            with app.app_context():
                db.session.remove()
                db.drop_all()
