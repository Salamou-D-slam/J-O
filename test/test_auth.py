import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    # Config spéciale test
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False
    })

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        # Nettoyage après chaque test
        with app.app_context():
            db.drop_all()
