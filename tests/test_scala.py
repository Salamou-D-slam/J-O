from locust import HttpUser, TaskSet, task, between
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash
import datetime
import os
from app.models import User, Epreuve, Offre
from dotenv import load_dotenv
load_dotenv()

# Config DB
DATABASE_TEST_URI = os.getenv('DATABASE_TEST_URI')

# Créer la session SQLAlchemy
engine = create_engine(DATABASE_TEST_URI)
Session = sessionmaker(bind=engine)
session = Session()

class UserBehavior(TaskSet):

    def on_start(self):
        # Vérifier si l'utilisateur existe
        if not session.query(User).filter_by(email="test@test.com").first():
            user = User(
                nom="test",
                prenom="user",
                email="test@test.com",
                password=generate_password_hash("testusertest", method='pbkdf2:sha256', salt_length=8)
            )
            session.add(user)
            session.commit()

        # Créer épreuve si elle n'existe pas
        if not session.query(Epreuve).filter_by(nom_epreuve="Test Epreuve").first():
            epreuve = Epreuve(
                nom_epreuve="Test Epreuve",
                date_epreuve=datetime.date(2025, 9, 30)
            )
            session.add(epreuve)
            session.commit()
        else:
            epreuve = session.query(Epreuve).filter_by(nom_epreuve="Test Epreuve").first()

        # Créer offre si elle n'existe pas
        if not session.query(Offre).filter_by(type_offre="test_solo").first():
            offre = Offre(
                type_offre="test_solo",
                prix=25.0,
                nombre_personne=1,
                id_epreuve=epreuve.id,
                bi_restant=2000,
                bi_vendu=0
            )
            session.add(offre)
            session.commit()

        # Connexion utilisateur
        self.client.post("/login", data={
            "email": "test@test.com",
            "password": "testusertest"
        })

    @task
    def paiement(self):
        self.client.post("/paiement/test_solo", data={
            "pers1_nom": "test",
            "pers1_prenom": "user",
            "pers1_email": "test@gmail.com",
            "nom_card": "test user",
            "card_number": 1234123412341234,
            "expiration_card": 229,
            "CVV_card": 111
        })


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)
    host = "http://127.0.0.1:5000"
