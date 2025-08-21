from sqlalchemy import Integer, String, Float, CheckConstraint, DateTime, ForeignKey, event
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .extensions import db
import secrets
import string
import qrcode
import uuid
import os
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import JSONB






# Pour générer aléatoirement une clé de 22 caractere qui inclus les lettre, chiffre et caractère spéciaux préciser
def generate_random_clef_user(length=22):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return ''.join(secrets.choice(alphabet) for _ in range(length))



class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    nom: Mapped[str] = mapped_column(String(1000), nullable=False)
    prenom: Mapped[str] = mapped_column(String(1000), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default='utilisateur')
    clef_user: Mapped[str] = mapped_column(String(22), unique=True, nullable=False, default=None)

    tickets = relationship("Ticket", back_populates="user", cascade="all, delete-orphan")


# Pour vérifier la clef existe déja pour renforcer l'"unique"
@event.listens_for(User, 'before_insert')
def receive_before_insert(mapper, connection, target):
    while True:
        new_clef_user = generate_random_clef_user(22)
        existing = connection.execute(
            db.select(User).where(User.clef_user == new_clef_user)
        ).scalar()
        if not existing:
            break
    target.clef_user = new_clef_user


class Epreuve(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom_epreuve: Mapped[str] = mapped_column(String(250), nullable=False)
    date_epreuve: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    image_filename: Mapped[str] = mapped_column(String(250), nullable=True)  # chemin ou nom du fichier image

    # Jointure --> Une épreuve a plusieurs offres
    offres = relationship("Offre", back_populates="epreuve", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Epreuve {self.nom_epreuve}>'

class Offre(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type_offre: Mapped[str] = mapped_column(String(250), nullable=False)
    nombre_personne: Mapped[int] = mapped_column(Integer, nullable=False)
    prix: Mapped[float] = mapped_column(Float, nullable=True)
    id_epreuve: Mapped[int] = mapped_column(Integer, ForeignKey('epreuve.id'), nullable=False)

    bi_restant: Mapped[int] = mapped_column(Integer, nullable=False)
    bi_vendu: Mapped[int] = mapped_column(Integer, nullable=False, default= 0)

    # Jointure --> L’offre appartient à une épreuve
    epreuve = relationship("Epreuve", back_populates="offres")
    tickets = relationship("Ticket", back_populates="offre", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Offre {self.type_offre} pour epreuve {self.id_epreuve}>"



class Ticket(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    offre_id: Mapped[int] = mapped_column(Integer, ForeignKey('offre.id'), nullable=False)

    pers_data = mapped_column(JSONB, nullable=True)
    # pers1_nom: Mapped[str] = mapped_column(String(1000), nullable=False)
    # pers1_prenom: Mapped[str] = mapped_column(String(1000), nullable=False)
    # pers1_email: Mapped[str] = mapped_column(String(100), nullable=False)
    #
    # pers2_nom: Mapped[str] = mapped_column(String(1000), nullable=True)
    # pers2_prenom: Mapped[str] = mapped_column(String(1000), nullable=True)
    #
    # pers3_nom: Mapped[str] = mapped_column(String(1000), nullable=True)
    # pers3_prenom: Mapped[str] = mapped_column(String(1000), nullable=True)
    #
    # pers4_nom: Mapped[str] = mapped_column(String(1000), nullable=True)
    # pers4_prenom: Mapped[str] = mapped_column(String(1000), nullable=True)

    date_achat: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    qr_code: Mapped[str] = mapped_column(String(250), nullable=False)

    status: Mapped[str] = mapped_column(String(250), nullable=False, default='valide')
    used_at = db.Column(db.DateTime, nullable=True)

    # Cration de clef unique ticket
    clef_ticket: Mapped[str] = mapped_column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    # str(uuid.uuid4()): Crée une clé aléatoire, méthode différente de la précedente

    # Pour stocker les infos en Json utile pour stocker plusieur infos en une seule colonne
    # pers1: Mapped[dict] = mapped_column(JSONB, nullable=True)
    # pers2: Mapped[dict] = mapped_column(JSONB, nullable=True)
    # pers3: Mapped[dict] = mapped_column(JSONB, nullable=True)
    # pers4: Mapped[dict] = mapped_column(JSONB, nullable=True)

    # Pour Génèrer un QR code avec clef_user + clef_ticket
    # def generate_qr_code(self):
    #
    #     if not self.user or not self.clef_ticket:
    #         raise ValueError("Impossible de générer le QR code : utilisateur ou clef_ticket manquant.")
    #
    #     # Données à mettre dans le QR
    #     data_qr = f"{self.user.clef_user}:{self.clef_ticket}"
    #
    #     # Dossier de stockage
    #     output_dir = "static/qrcodes"
    #     os.makedirs(output_dir, exist_ok=True)
    #
    #     # Chemin complet du fichier
    #     file_path = os.path.join(output_dir, f"{self.ticket_key}.png")
    #
    #     # Création du QR code
    #     qr = qrcode.QRCode(
    #         version=1,
    #         error_correction=qrcode.constants.ERROR_CORRECT_L,
    #         box_size=10,
    #         border=4
    #     )
    #     qr.add_data(data_qr)
    #     qr.make(fit=True)
    #
    #     img = qr.make_image(fill_color="black", back_color="white")
    #     img.save(file_path)
    #
    #      # On enregistre le chemin dans la BDD
    #      self.qr_code_path = file_path

    user = relationship("User", back_populates="tickets")
    offre = relationship("Offre", back_populates="tickets")

# class Reservation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     personnes = db.relationship("Personne", back_populates="reservation")
#
# class Personne(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     prenom = db.Column(db.String(50))
#     nom = db.Column(db.String(50))
#     email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
#     reservation_id = db.Column(db.Integer, db.ForeignKey("reservation.id"))
#     reservation = db.relationship("Reservation", back_populates="personnes")
