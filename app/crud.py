from flask import current_app
from app.models import Epreuve
from app.extensions import db


#------------------------------------------------EPREUVE----------------------------------------

#CREATE
def add_epreuve_if_not_exists(nom_epreuve, date_epreuve, imag_filename):
    existing_epreuve = Epreuve.query.filter_by(nom_epreuve=nom_epreuve).first()
    if not existing_epreuve:
        new_epreuve = Epreuve(nom_epreuve=nom_epreuve, date_epreuve=date_epreuve, imag_filename=imag_filename)
        db.session.add(new_epreuve)
        db.session.commit()
        print(f"Ajouté : {nom_epreuve}")
    else:
        print(f"Déjà présent : {nom_epreuve}")

#READ ONE
def get_epreuve_by_id(epreuve_id):
    epreuve = db.session.get(Epreuve, epreuve_id)  # cherche le livre avec id=1
    if epreuve:
        print(epreuve.nom_epreuve, epreuve.date_epreuve, epreuve.imag_filename)
    else:
        print("epreuve non trouvé")


#READ ALL
def get_all_epreuves():
    return Epreuve.query.all()



#UPDATE
def update_epreuve(epreuve_id, new_nom_epreuve=None, date_epreuve=None, new_imag_filename=None):
    epreuve = Epreuve.query.get(epreuve_id)
    if epreuve:
        if new_nom_epreuve: epreuve.title = new_nom_epreuve
        if new_imag_filename: epreuve.author = new_imag_filename
        db.session.commit()
        print(f"Mise à jour de l'épreuve ID {epreuve_id}")
    else:
        print("Livre non trouvé.")

#DELETE
def delete_epreuve(epreuve_id):
    epreuve = Epreuve.query.get(epreuve_id)
    if epreuve:
        db.session.delete(epreuve)
        db.session.commit()
        print(f"Livre ID {epreuve_id} supprimé.")
    else:
        print("Livre non trouvé.")

#------------------------------------------------------------------------------------------------------


# ------------------------------------------------OFFRE----------------------------------------

# CREATE
def add_offre_if_not_exists(type_offre, nombre_personne, prix):
    existing_offre = Epreuve.query.filter_by(type_offre=type_offre).first()
    if not existing_offre:
        new_offre = Epreuve(type_offre=type_offre, nombre_personne=nombre_personne, prix=prix)
        db.session.add(new_offre)
        db.session.commit()
        print(f"Ajouté : {type_offre}")
    else:
        print(f"Déjà présent : {type_offre}")


# READ ONE
def get_offre_by_id(offre_id):
    offre = db.session.get(Epreuve, offre_id)  # cherche le livre avec id=1
    if offre:
        print(offre.type_offre, offre.nombre_personne, offre.prix)
    else:
        print("Livre non trouvé")


# READ ALL
def get_all_offres():
    return Epreuve.query.all()


# UPDATE
def update_offre(offre_id, new_type_offre=None, nombre_personne=None, new_prix=None):
    offre = Epreuve.query.get(offre_id)
    if offre:
        if new_type_offre: offre.title = new_type_offre
        if new_prix: offre.author = new_prix
        db.session.commit()
        print(f"Mise à jour du livre ID {offre_id}")
    else:
        print("Livre non trouvé.")


# DELETE
def delete_offre(offre_id):
    offre = Epreuve.query.get(offre_id)
    if offre:
        db.session.delete(offre)
        db.session.commit()
        print(f"Livre ID {offre_id} supprimé.")
    else:
        print("Livre non trouvé.")

# ------------------------------------------------------------------------------------------------------