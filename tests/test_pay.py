import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.extensions import db
from app.models import Offre, Epreuve, User
from configtest import client
from werkzeug.security import generate_password_hash


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
    assert b"Informations personnelles" in response.data or b"accueil" in response.data
