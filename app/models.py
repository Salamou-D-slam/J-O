from sqlalchemy import Integer, String, Float, CheckConstraint, DateTime, ForeignKey, event
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .extensions import db
import secrets
import string
import qrcode


# Pour générer aléatoirement une clé de 22 caractere qui inclus les lettre, chiffre et caractère spéciaux préciser
def generate_random_clef_user(length=22):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


# Pour creer le qr code
def generate_qr_code(data, file_path):
    # Création du QRCode
    qr = qrcode.QRCode(
        version=1,  # taille du QR
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # niveau de correction d'erreur
        box_size=10,  # taille des carré
        border=4,  # taille des carré des bordures blanched autour du QR code
    )
    qr.add_data(data)  # ajout des données à encoder
    qr.make(fit=True)  # génère la matrice du QR code

    # Génération de l'image PIL
    img = qr.make_image(fill_color="black", back_color="white")

    # Sauvegarde de l'image dans un fichier
    img.save(file_path)


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

    # Jointure --> L’offre appartient à une épreuve
    epreuve = relationship("Epreuve", back_populates="offres")
    tickets = relationship("Ticket", back_populates="offre", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Offre {self.type_offre} pour epreuve {self.id_epreuve}>"



class Ticket(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    offre_id: Mapped[int] = mapped_column(Integer, ForeignKey('offre.id'), nullable=False)
    date_achat: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    qr_code = mapped_column(String(250), nullable=False)
    status: Mapped[str] = mapped_column(String(250), nullable=False)
    clef_ticket: Mapped[str] = mapped_column(String(22), unique=True, nullable=False, default=None)


    # Pour vérifier la clef existe déja pour renforcer l'"unique"
    @event.listens_for(User, 'before_insert')
    def receive_before_insert(mapper, connection, target):
        while True:
            new_clef_ticket = generate_random_clef_user(22)
            existing = connection.execute(
                db.select(User).where(User.clef_user == new_clef_ticket)
            ).scalar()
            if not existing:
                break
        target.clef_ticket = new_clef_ticket


    user = relationship("User", back_populates="tickets")
    offre = relationship("Offre", back_populates="tickets")