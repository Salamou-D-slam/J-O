import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.extensions import db
from werkzeug.security import generate_password_hash
from configtest import client
from app.models import Offre, Epreuve, User, Ticket


def test_scan(client):
    with client.application.app_context():
        # Créer un utilisateur + offre + simulation paiement
        unique_email = f"test{+1}@test.com"  # Pour avoir un mail unique

        user = User(nom="test", prenom="user", email=unique_email)
        user.password = generate_password_hash("test19000", method='pbkdf2:sha256', salt_length=8)  # Hash direct
        db.session.add(user)
        db.session.commit()

        epreuve = Epreuve(
            nom_epreuve="Test Epreuve 2",
            date_epreuve=datetime.date(2025, 9, 30)
        )
        db.session.add(epreuve)
        db.session.commit()

        # Créer une offre associée à l'épreuve
        offre = Offre(
            type_offre="test2_solo",
            prix=25.0,
            nombre_personne=1,
            id_epreuve=epreuve.id,
            bi_restant=200,
            bi_vendu=0
        )
        db.session.add(offre)
        db.session.commit()

        # Simuler un paiement
        client.post("/login", data={
            "email": unique_email,
            "password": "test19000"
        }, follow_redirects=True)

        # Simuler la route de paiement
        response = client.post("/paiement/test2_solo", data={
            "pers1_nom": "test",
            "pers1_prenom": "user",
            "pers1_email": "test@gmail.com",
            "nom_card": "test user",
            "card_number": 1234123412341234,
            "expiration_card": 229,
            "CVV_card": 111
        }, follow_redirects=True)

    ticket = Ticket.query.first()
    assert ticket is not None, "Aucun ticket n'a été créé par la route paiement"
    ticket_id = ticket.id

    # Ticket valide
    response = client.get(f"/api/validate_ticket/{ticket_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("valid") is True

    # Ticket déjà utilisé
    response2 = client.get(f"/api/validate_ticket/{ticket_id}")
    assert response2.status_code == 400
    data2 = response2.get_json()
    assert data2.get("valid") is False

    # Ticket inexistant
    response3 = client.get(f"/api/validate_ticket/{ticket_id + 999}")
    assert response3.status_code == 404
    data3 = response3.get_json()
    assert data3.get("valid") is False