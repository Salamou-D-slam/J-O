from app import create_app
from app.crud import add_epreuve_if_not_exists, get_all_epreuves, get_epreuve_by_id, update_epreuve, delete_epreuve
from app.models import Epreuve, Offre
from sqlalchemy import Integer, String, Float, select, delete, text
from app.extensions import db
from sqlalchemy import text



app = create_app()  # doit renvoyer juste app


#CREATE
#with app.app_context():
    # epreuve = add_epreuve_if_not_exists("100m hommes", "2025-08-10 15:00:00", "100m.jpg")
    # add_default_offres_for_epreuve("100m hommes")



#READ
# with app.app_context():
#     get_epreuve_by_id(1)

#READ ALL
# with app.app_context():
#     stmt = select(Book)  # construit une requête SELECT * FROM epreuve
#     epreuves = get_all_epreuves()
#     for epreuve in epreuves:
#         print(f"Title: {epreuve.nom_epreuve}; Author: {epreuve.image_filename}")

#UPDATE
# with app.app_context():
#    update_epreuve(6, new_nom_epreuve = "")
#    update_offre(6, new_prix = "")

#DELETE
# with app.app_context():
#        delete_epreuve(6)

# with app.app_context():
#     db.session.execute(delete(Epreuve))
#     db.session.execute(text("ALTER SEQUENCE epreuve_id_seq RESTART WITH 1;"))
#     db.session.commit()
#     print("Séquence réinitialisée.")

# DELETE les table et les recrée
with app.app_context():
    db.drop_all()
    db.create_all()


