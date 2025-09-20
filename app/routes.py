from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash, current_app, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import os
from flask_mail import Message
from .models import Epreuve, Offre, User
from .extensions import db, login_manager, mail
from .crud import update_epreuve, add_epreuve_if_not_exists, get_epreuve_by_id, update_epreuve, delete_epreuve
from .WTForms.forms import LoginForm, RegisterForm, AddepreuvesForm, UpdateepreuvesForm, ContactForm, EpreuvedetailForm

main_routes = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Fonction pour autoriser un ou plusieurs rôles à accéder à la page
def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Connexion requise.")
                return redirect(url_for('auth.login'))
            if current_user.role not in roles:
                flash("Accès refusé.")
                return redirect(url_for('main.home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

#-------------------------------------------------PAGE D'ACCUEIL--------------------------


@main_routes.route('/')
def home():
    return render_template('index.html')



#-------------------------------------------------AUTHENTIFICAATION-------------------------------

# REGISTER
@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        nom = form.nom.data
        prenom = form.prenom.data
        email = form.email.data
        password = form.password.data

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

    return render_template('register.html', form=form)


# LOGIN
@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # Vérifie si POST + validation
        email = form.email.data
        password = form.password.data

        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Connecté avec succès.")
            # Redirection selon rôle
            if user.role == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            elif user.role == 'employe':
                return redirect(url_for('employe.employe_dashboard'))
            else:
                return redirect(url_for('utilisateur.utilisateur_dashboard'))
        else:
            flash("Email ou mot de passe incorrect.")
    return render_template('login.html', form=form)

# LOGOUT
@main_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Déconnecté.")
    return redirect(url_for('main.home'))

# CREATION D'UN ADMIN (a faire qu'une fois)

@main_routes.route('/create-admin')
def create_admin():
    hashed_password = generate_password_hash("joadmin2024", method='pbkdf2:sha256', salt_length=8)
    admin = User(email="jose@gmail.com", nom="Jose", prenom="Admin", password=hashed_password, role="admin")

    existing_user = db.session.execute(db.select(User).where(User.email == "jose@gmail.com")).scalar()
    # Pour vérifier si le compte existe déja pour éviter des erreurs
    if existing_user:
        flash("Compte déja existant, connecte-toi plutôt.")
        return redirect(url_for('main.login'))
    db.session.add(admin)
    db.session.commit()
    return "✅ Admin créé avec succès !"


#-------------------------------------------------EPREUVES FRONT-------------------------------

# PAGE ALL EPREUVES
@main_routes.route('/epreuves')
def all_epreuve_front():
    epreuves = Epreuve.query.all()
    return render_template('all_epreuve_front.html', epreuves=epreuves)


#PAGE D'EPREUVE DETAILS
@main_routes.route('/epreuves-<nom_epreuve>', methods=['GET', 'POST'])
def epreuve_details_front(nom_epreuve):
    form = EpreuvedetailForm()
    epreuve = Epreuve.query.filter_by(nom_epreuve=nom_epreuve).first()
    if not epreuve:
        return "Epreuve non trouvée", 404
    return render_template('epreuve_front.html', epreuve=epreuve, form=form)



#-------------------------------------------------EPREUVES BACK-------------------------------

# PAGE ALL EPREUVES
@main_routes.route('/epreuvesback')
@login_required
@roles_required('admin', 'employe')
def all_epreuve():
    epreuves = Epreuve.query.all()
    return render_template('all_epreuve.html', epreuves=epreuves)


#PAGE ADD epreuves
@main_routes.route('/add_epreuves', methods=["GET", "POST"])
@login_required
@roles_required('admin', 'employe')
def add_epreuves():
    form = AddepreuvesForm()
    # if request.method == "POST":
    if form.validate_on_submit():


        nom_epreuve = form.nom_epreuve.data
        date_epreuve = form.date_epreuve.data
        image = form.image.data


        prix_solo = form.prix_solo.data
        prix_duo = form.prix_duo.data
        prix_family = form.prix_family.data

        nbr_place_solo = form.nbr_place_solo.data
        nbr_place_duo = form.nbr_place_duo.data
        nbr_place_family = form.nbr_place_family.data

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
            prix_family = prix_family,

            nbr_place_solo = nbr_place_solo,
            nbr_place_duo =nbr_place_duo,
            nbr_place_family = nbr_place_family
        )

        return redirect(url_for('main.all_epreuve'))
    return render_template('add.html', form=form)


#PAGE D'EPREUVE DETAILS

@main_routes.route('/epreuvesback-<nom_epreuve>', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'employe')
def epreuve_details(nom_epreuve):
    form = EpreuvedetailForm()
    epreuve = Epreuve.query.filter_by(nom_epreuve=nom_epreuve).first()
    if not epreuve:
        return "Epreuve non trouvée", 404

    return render_template('epreuve.html', epreuve=epreuve, form=form)



#PAGE DE UPADATE
@main_routes.route('/update/<int:epreuve_id>', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'employe')
def update(epreuve_id):
    form = UpdateepreuvesForm()
    epreuve = get_epreuve_by_id(epreuve_id)
    # if request.method == 'POST':
    if form.validate_on_submit():


        new_nom_epreuve = form.new_nom_epreuve.data
        new_date_epreuve = form.new_date_epreuve.data
        new_image = form.new_image.data

        # Met la sécurité et le chemin des images uploads
        new_filename = None
        if new_image and new_image.filename != '':
            new_filename = secure_filename(new_image.filename)
            new_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename))


        new_prix_solo = form.new_prix_solo.data
        new_prix_duo = form.new_prix_duo.data
        new_prix_family = form.new_prix_family.data

        # Les convertir en float si présents
        new_prix_solo = float(new_prix_solo) if new_prix_solo else None
        new_prix_duo = float(new_prix_duo) if new_prix_duo else None
        new_prix_family = float(new_prix_family) if new_prix_family else None

        new_nbr_place_solo = form.new_nbr_place_solo.data
        new_nbr_place_duo = form.new_nbr_place_duo.data
        new_nbr_place_family = form.new_nbr_place_family.data



        update_epreuve(
            epreuve_id,
            new_nom_epreuve,
            new_date_epreuve,
            new_filename,
            new_prix_solo,
            new_prix_duo,
            new_prix_family,
            new_nbr_place_solo,
            new_nbr_place_duo,
            new_nbr_place_family
        )
        return redirect(url_for('main.all_epreuve'))
    return render_template('update.html', epreuve=epreuve, form=form)

# DELETE
@main_routes.route('/delete/<int:epreuve_id>', methods=['POST'])
@login_required
@roles_required('admin', 'employe')
def delete(epreuve_id):
    delete_epreuve(epreuve_id)
    return redirect(url_for('main.all_epreuve'))


# PAGE DE CONTACT
@main_routes.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if request.method == "POST":
        nom = form.nom.data
        email = form.email.data
        message_user = form.message.data

        msg = Message(
            subject=f"Nouveau message de {nom}", # L'objet du mail
            recipients=[os.getenv('MAIL_JO')],  # Adresse de l'entreprise (adresse qui reçoit le mail)
            body=f"De: {nom} <{email}>\n\n{message_user}" # le message
        )
        msg.reply_to = email # Pour que l'email de l'utilisateur sera utilisé comme destinataire en cas de réponse

        mail.send(msg) # Pour envoyer l'email
        flash("Votre message a bien été envoyé ✅")
        return redirect(url_for("main.contact"))

    return render_template("contact.html", form=form)










