from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash, current_app
from .models import Epreuve
from .extensions import db
from app.crud import add_epreuve_if_not_exists, get_all_epreuves, get_epreuve_by_id, update_epreuve, delete_epreuve #,add_default_offres_for_epreuve
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


@auth_routes.route('/connexion')
def login():
    pass