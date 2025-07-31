from flask import current_app
from app.models import Epreuve, Offre
from app.extensions import db


#------------------------------------------------EPREUVE----------------------------------------

#CREATE une éprevue s'elle n'existe pas
def add_epreuve_if_not_exists(nom_epreuve, date_epreuve,prix_solo, prix_duo, prix_family, filename=None):

    # Vérifier si l’épreuve existe déjà
    existing_epreuve = Epreuve.query.filter_by(nom_epreuve=nom_epreuve).first()
    if  existing_epreuve:
        print("Epreuve déjà existante")
        return

    #Crée l’épreuve

    new_epreuve = Epreuve(
        nom_epreuve = nom_epreuve,
        date_epreuve = date_epreuve,
        image_filename = filename
    )

    #Crée les offres liées

    solo = Offre(type_offre='solo', nombre_personne=1, prix=prix_solo)
    duo = Offre(type_offre='duo', nombre_personne=2, prix=prix_duo)
    family = Offre(type_offre='family', nombre_personne=4, prix=prix_family)

    new_epreuve.offres.extend([solo, duo, family])

    db.session.add(new_epreuve)
    db.session.commit()
    print(f"Epreuve '{nom_epreuve}' et ses offres créées.")


#CREATE les 3 offres par défaut automatiquement

# def add_default_offres_for_epreuve(nom_epreuve):
#     epreuve = Epreuve.query.filter_by(nom_epreuve=nom_epreuve).first()
#     if not epreuve:
#         print(f"Epreuve '{nom_epreuve}' non trouvée.")
#         return
#
#
#
#     offres = [
#         ("Solo", 1, 25.0),
#         ("Duo", 2, 40.0),
#         ("Family", 4, 80.0)
#     ]
#
#     for type_offre, nombre_personne, prix in offres:
#         existing_offre = Offre.query.filter_by(type_offre=type_offre, id_epreuve=epreuve.id).first()
#         if not existing_offre:
#             new_offre = Offre(
#                 type_offre=type_offre,
#                 nombre_personne=nombre_personne,
#                 prix=prix,
#                 id_epreuve=epreuve.id
#             )
#             db.session.add(new_offre)
#             print(f"Offre '{type_offre}' ajoutée pour '{nom_epreuve}'.")
#         else:
#             print(f"Offre '{type_offre}' déjà présente pour '{nom_epreuve}'.")
#     db.session.commit()



#CREATE une offre manuellement
def add_offre_to_epreuve(epreuve_id, type_offre, nombre_personne, prix):
    epreuve = db.session.get(Epreuve, epreuve_id)
    if epreuve:
        new_offre = Offre(
            type_offre=type_offre,
            nombre_personne=nombre_personne,
            prix=prix,
            epreuve=epreuve  # on lie l'offre directement à l'épreuve
        )
        db.session.add(new_offre)
        db.session.commit()
        print(f"Ajouté offre '{type_offre}' à l'épreuve '{epreuve.nom_epreuve}'")
    else:
        print("Epreuve non trouvée")


#READ ONE
def get_epreuve_by_id(epreuve_id):
    epreuve = db.session.get(Epreuve, epreuve_id)  # cherche l'épreuve avec id=1
    if epreuve:
        print(f"Epreuve: {epreuve.nom_epreuve}, Date: {epreuve.date_epreuve}, Image_url: {epreuve.image_filename}")
        print("Offres associées :")

        for offre in epreuve.offres: #Jointure
            print(f"- {offre.type_offre}, {offre.nombre_personne} pers, {offre.prix} €")
    else:
        print("epreuve non trouvé")


#READ ALL
def get_all_epreuves():
    return Epreuve.query.all()



#UPDATE
def update_epreuve(epreuve_id, new_nom_epreuve=None, new_date_epreuve=None, new_image_filename=None):
    epreuve = Epreuve.query.get(epreuve_id)
    if epreuve:
        if new_nom_epreuve: epreuve.nom_epreuve = new_nom_epreuve
        if new_date_epreuve: epreuve.date_epreuve = new_date_epreuve
        if new_image_filename: epreuve.image_filename = new_image_filename
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
# def add_offre_if_not_exists(type_offre, nombre_personne, prix):
#     existing_offre = Epreuve.query.filter_by(type_offre=type_offre).first()
#     if not existing_offre:
#         new_offre = Epreuve(type_offre=type_offre, nombre_personne=nombre_personne, prix=prix)
#         db.session.add(new_offre)
#         db.session.commit()
#         print(f"Ajouté : {type_offre}")
#     else:
#         print(f"Déjà présent : {type_offre}")


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
def update_offre(offre_id, new_type_offre=None, new_nombre_personne=None, new_prix=None):
    offre = Epreuve.query.get(Offre, offre_id)
    if offre:
        if new_type_offre: offre.type_offre = new_type_offre
        if new_nombre_personne: offre.nombre_personne = new_nombre_personne
        if new_prix: offre.priw = new_prix
        db.session.commit()
        print(f"Mise à jour du livre ID {offre_id}")
    else:
        print("Livre non trouvé.")


# DELETE
def delete_offre(offre_id):
    offre = Offre.query.get(offre_id)
    if offre:
        db.session.delete(offre)
        db.session.commit()
        print(f"Livre ID {offre_id} supprimé.")
    else:
        print("Livre non trouvé.")




# ------------------------------------------------------------------------------------------------------