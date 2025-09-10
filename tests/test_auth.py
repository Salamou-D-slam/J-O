import pytest
from werkzeug.security import generate_password_hash
from configtest import client
from app import create_app, db
from app.models import User

import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.extensions import db
from app.models import Offre, Epreuve
from configtest import client
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



def test_payment(client):
    with client.application.app_context():
        # Créer un utilisateur pour le test
        user = User(
            nom="test",
            prenom="user",
            email="test@test.com",
            password=generate_password_hash("test19000", method='pbkdf2:sha256', salt_length=8)
        )
        db.session.add(user)
        db.session.commit()

        # Connexion de l'utilisateur
        client.post("/login", data={
            "email": "test@test.com",
            "password": "test19000"
        })

        # Créer une épreuve de test
        epreuve = Epreuve(
            nom_epreuve="Test Epreuve",
            date_epreuve=datetime.date(2025, 9, 30)
        )
        db.session.add(epreuve)
        db.session.commit()

        # Créer une offre associée à l'épreuve
        offre = Offre(
            type_offre="test_solo",
            prix=25.0,
            nombre_personne=1,
            id_epreuve=epreuve.id,
            bi_restant=200,
            bi_vendu=0
        )
        db.session.add(offre)
        db.session.commit()

    # Simuler la route de paiement
    response = client.post("/paiement/test_solo", data={
        "pers1_nom": "test",
        "pers1_prenom": "user",
        "pers1_email": "test@gmail.com",
        "nom_card": "test user",
        "card_number": 1234123412341234,
        "expiration_card": 229,
        "CVV_card": 111
    }, follow_redirects=True)

    # Vérifier que le paiement a été accepté et la page charge correctement
    assert response.status_code == 200
    assert b"Informations personnelles" in response.data

    # assert response.status_code == 302
    # assert "/utilisateur" in response.headers["Location"]
