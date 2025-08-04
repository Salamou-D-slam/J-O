from sqlalchemy import Integer, String, Float, CheckConstraint, DateTime, ForeignKey
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .extensions import db


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    nom: Mapped[str] = mapped_column(String(1000), nullable=False)
    prenom: Mapped[str] = mapped_column(String(1000), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default='utilisateur')
    #cle:



class Epreuve(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom_epreuve: Mapped[str] = mapped_column(String(250), nullable=False)
    date_epreuve: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    image_filename: Mapped[str] = mapped_column(String(250), nullable=True)  # chemin ou nom du fichier image

    # Une épreuve a plusieurs offres
    offres = relationship("Offre", back_populates="epreuve", cascade="all, delete-orphan")





    def __repr__(self):
        return f'<Epreuve {self.nom_epreuve}>'

class Offre(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type_offre: Mapped[str] = mapped_column(String(250), nullable=False)
    nombre_personne: Mapped[int] = mapped_column(Integer, nullable=False)
    prix: Mapped[float] = mapped_column(Float, nullable=True)
    id_epreuve: Mapped[int] = mapped_column(Integer, ForeignKey('epreuve.id'), nullable=False)

    # L’offre appartient à une épreuve
    epreuve = relationship("Epreuve", back_populates="offres")

    def __repr__(self):
        return f"<Offre {self.type_offre} pour epreuve {self.id_epreuve}>"
