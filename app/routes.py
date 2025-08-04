from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.crud import add_epreuve_if_not_exists, get_epreuve_by_id, update_epreuve, delete_epreuve , get_epreuve_by_nom_epreuve #add_default_offres_for_epreuve
from werkzeug.utils import secure_filename
import os
from .models import Epreuve, Offre, User
from .extensions import db, login_manager

main_routes = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


#-------------------------------------------------PAGE D'ACCUEIL--------------------------


@main_routes.route('/')
def home():
    return render_template('index.html')



#-------------------------------------------------AUTHENTIFICAATION-------------------------------

# LOGIN
@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        password = request.form.get('password')

        existing_user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if existing_user:
            flash("Email déjà utilisé, connecte-toi plutôt.")
            return redirect(url_for('main.login'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        new_user = User(email=email, nom=nom,prenom=prenom, password=hashed_password, role='utilisateur')
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash("Inscription réussie!")
        return redirect(url_for('main.home'))

    return render_template('register.html')


# REGISTER
@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Connecté avec succès.")
            # Redirection selon rôle
            if user.role == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            elif user.role == 'employe':
                return redirect(url_for('admin.employe_panel'))
            else:
                return redirect(url_for('main.home'))
        else:
            flash("Email ou mot de passe incorrect.")
    return render_template('login.html')

# LOGOUT
@main_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Déconnecté.")
    return redirect(url_for('main.home'))

# CREATION D'UN ADMIN (a faire qu'une fois)

# @main_routes.route('/create-admin')
# def create_admin():
#     hashed_password = generate_password_hash("joadmin2024", method='pbkdf2:sha256', salt_length=8)
#     admin = User(email="admin@gmail.com", nom="Jose", prenom="Admin", password=hashed_password, role="admin")
#     db.session.add(admin)
#     db.session.commit()
#     return "✅ Admin créé avec succès !"
#-------------------------------------------------EPREUVES-------------------------------
# PAGE ALL EPREUVES
@main_routes.route('/epreuves')
def all_epreuve():
    epreuves = Epreuve.query.all()
    return render_template('all_epreuve.html', epreuves=epreuves)

#PAGE ADD epreuves
@main_routes.route('/epreuves', methods=["GET", "POST"])
def add_epreuves():
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

        return redirect(url_for('main.all_epreuve'))
    return render_template('add.html')


#PAGE D'EPREUVE DETAILS

@main_routes.route('/epreuves-<nom_epreuve>', methods=['GET', 'POST'])
def epreuve_details(nom_epreuve):

    epreuve = Epreuve.query.filter_by(nom_epreuve=nom_epreuve).first()
    if not epreuve:
        return "Epreuve non trouvée", 404

    return render_template('epreuve.html', epreuve=epreuve)


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
        return redirect(url_for('main.all_epreuve'))
    return render_template('update.html', epreuve=epreuve)

#DELETE
@main_routes.route('/delete/<int:epreuve_id>', methods=['POST'])
def delete(epreuve_id):
    delete_epreuve(epreuve_id)
    return redirect(url_for('main.all_epreuve'))



#PAGE DE PAYEMENT
@main_routes.route('/paiement/<int:offre_id>')
def paiement_epreuve(offre_id):
    return render_template('paiement.html')







