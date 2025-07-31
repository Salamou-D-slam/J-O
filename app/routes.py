from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash, current_app
from .models import Epreuve
from .extensions import db
from app.crud import add_epreuve_if_not_exists, get_epreuve_by_id, update_epreuve, delete_epreuve #,add_default_offres_for_epreuve
from werkzeug.utils import secure_filename
import os

main_routes = Blueprint('main', __name__)
auth_routes = Blueprint('auth', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#PAGE D'ACCUEIL
@main_routes.route('/')
def home():
    epreuves = Epreuve.query.all()
    return render_template('index.html', epreuves=epreuves)

#PAGE ADD
@main_routes.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":

        #Ramene les "name" des input HTML
        nom_epreuve = request.form.get('nom_epreuve')
        date_epreuve = request.form.get('date_epreuve')
        image = request.files.get('image')

        prix_solo = float(request.form['prix_solo'])
        prix_duo = float(request.form['prix_duo'])
        prix_family = float(request.form['prix_family'])

        #Met la sécurité et le chemin des images uploads
        filename = secure_filename(image.filename)
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        #CREATE des épreuves et leurs offres
        add_epreuve_if_not_exists(
            nom_epreuve= nom_epreuve,
            date_epreuve = date_epreuve,
            filename = filename,

            prix_solo = prix_solo,
            prix_duo = prix_duo,
            prix_family = prix_family
        )

        return redirect(url_for('main.home'))
    return render_template('add.html')


#PAGE DE UPADATE
@main_routes.route('/update/<int:epreuve_id>', methods=['GET', 'POST'])
def update(epreuve_id):
    epreuve = get_epreuve_by_id(epreuve_id)
    if request.method == 'POST':

        #Ramene les "name" des input HTML
        new_nom_epreuve = request.form.get('nom_epreuve')
        new_date_epreuve = request.form.get('date_epreuve')
        new_image = request.files.get('image')

        # Met la sécurité et le chemin des images uploads
        new_filename = None
        if new_image and new_image.filename != '':
            new_filename = secure_filename(new_image.filename)
            new_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename))

        new_prix_solo = request.form.get('prix_solo')
        new_prix_duo = request.form.get('prix_duo')
        new_prix_family = request.form.get('prix_family')

        # Les convertir en float si présents
        new_prix_solo = float(new_prix_solo) if new_prix_solo else None
        new_prix_duo = float(new_prix_duo) if new_prix_duo else None
        new_prix_family = float(new_prix_family) if new_prix_family else None



        update_epreuve(
            epreuve_id,
            new_nom_epreuve,
            new_date_epreuve,
            new_filename,
            new_prix_solo,
            new_prix_duo,
            new_prix_family

        )
        return redirect(url_for('main.home'))
    return render_template('update.html', epreuve=epreuve)

#DELETE
@main_routes.route('/delete/<int:epreuve_id>', methods=['POST'])
def delete(epreuve_id):
    delete_epreuve(epreuve_id)
    return redirect(url_for('main.home'))