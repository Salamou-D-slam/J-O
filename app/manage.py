from app import create_app
from app.crud import add_epreuve_if_not_exists, get_all_epreuves, get_epreuve_by_id, update_epreuve, delete_epreuve
from app.models import Epreuve
from sqlalchemy import Integer, String, Float, select, delete, text


app = create_app()  # doit renvoyer juste app

#CREATE
#with app.app_context():
    # add_epreuve_if_not_exists("Harry Potter", "J. K. Rowling", 9.3)



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

#DELETE
# with app.app_context():
#       delete_epreuve()