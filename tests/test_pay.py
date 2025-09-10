import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.extensions import db
from app.models import Offre, Epreuve
from configtest import client
from flask_login import current_user







def test_payment(client, ):
    with client.application.app_context():
        epreuve = Epreuve(nom_epreuve="Test Epreuve", date_epreuve= datetime.date(2025,9,30))
        db.session.add(epreuve)
        db.session.add(epreuve)
        db.session.commit()
        # Créer une offre de test
        offre = Offre(
            type_offre="test_solo",
            prix=25.0,
            nombre_personne=1,
            id_epreuve = epreuve.id,
            # date_epreuve = epreuve.date_epreuve
            bi_restant = 200
        )
        db.session.add(offre)
        db.session.commit()

    # Appel de la route paiement (URL doit matcher le type_offre)
    response = client.post("/paiement/test_solo", data={
        "pers1_nom": "test",
        "pers1_prenom": "user",
        "pers1_email": "test@gmail.com",
        "nom_card": "test user",
        "card_number": "1234123412341234",
        "expiration_card": "02/29",
        "CVV_card": "111"
    })

    # Vérifier que la page charge correctement
    assert response.status_code == 302
    assert "/utilisateur" in response.headers["Location"]


