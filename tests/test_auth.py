import pytest
from werkzeug.security import generate_password_hash
from configtest import client
from app import create_app, db
from app.models import User

# @pytest.fixture
# def client():
#     test_config = {
#         "TESTING": True,
#         "SQLALCHEMY_DATABASE_URI": 'postgresql+psycopg2://jo_admin:joadmin2024@localhost:5432/jo_test',
#         "WTF_CSRF_ENABLED": False,
#     }
#
#     app = create_app(test_config)  # On passe la config test
#
#
#     with app.test_client() as client:
#             with app.app_context():
#                 db.create_all()
#             yield client
#             # Nettoyage après chaque test
#             with app.app_context():
#                 db.drop_all()


def test_register(client):
    response = client.post("/register", data={
        "nom": "test",
        "prenom": "user",
        "email": "test@test.com",
        "password": "test19000",
        "confirm_password": "test19000"
    }, follow_redirects=True)

    assert response.status_code == 200

    assert b"Bienvenue sur le site" in response.data or b"Merci de vous connecter ou de vous inscrire." in response.data

    # Vérifie que l'utilisateur est bien en base
    with client.application.app_context():
        user = User.query.filter_by(email="test@test.com").first()
        assert user is not None


def test_login(client):
    # Créer un user en base
    with client.application.app_context():
        user = User(nom="test", prenom="user", email="test@test.com")
        user.password = generate_password_hash("test19000", method='pbkdf2:sha256', salt_length=8)  # Hash direct
        db.session.add(user)
        db.session.commit()

    # Simuler le login
    response = client.post("/login", data={
        "email": "test@test.com",
        "password": "test19000"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Informations personnelles" in response.data

