from flask import Flask
import os
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap
from app.extensions import db, login_manager, mail, csrf
from app.routes import main_routes
from app.admin.routes import admin_routes
from app.employe.routes import employe_routes
from app.paiement.routes import paiement_routes
from app.ticket.routes import ticket_routes
from app.scan.routes import scan_routes
from app.utilisateur.routes import utilisateur_routes



def create_app(test_config=None):
    load_dotenv()  # Charge des variables du .env

    app = Flask(__name__)


    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads/image') # Config le chemin des envoi des images
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # La taille maximal (max 16MB)

    # app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URI') # Config la bdd

    if os.getenv("DOCKER"):  # une variable qu’on définit uniquement dans docker-compose
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI_DOCKER")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Désactiver le système de signal de modification de SQLAlchemy

    # Si on passe une config de test, on écrase
    if test_config:
        app.config.update(test_config)

    print("👉 DB utilisée :", app.config["SQLALCHEMY_DATABASE_URI"])  # Debug

    db.init_app(app)


    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    # Configure les infos pour le mail de l'entreprise
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER') # L’adresse du serveur SMTP (celui qui envoie les mails)
    app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT")) # Le port de communication avec le serveur SMTP.
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') # Active la sécurité TLS (Transport Layer Security).
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME') # L’adresse mail expéditrice (l'adresse qui envoie les mails)
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD') # Mot de passe ddu compte expéditrice Gmail
    app.config['MAIL_DEFAULT_SENDER'] = ('Site JO', os.getenv('MAIL_DEFAULT_SENDER'))# Nom affiché dans la boîte mail

    # initialise l'extensions
    mail.init_app(app)

    # intialise CSRF pour WTForms
    csrf.init_app(app)


    login_manager.init_app(app) # Un gestionnaire d’authentification fourni par Flask-Login
    bootstrap = Bootstrap(app) # Pour utiliser le boostrap dans les templates Jinja2

    app.register_blueprint(main_routes)
    app.register_blueprint(admin_routes, url_prefix='/admin')
    app.register_blueprint(employe_routes, url_prefix='/employe')
    app.register_blueprint(utilisateur_routes, url_prefix='/utilisateur')
    app.register_blueprint(paiement_routes, url_prefix='/paiement')
    app.register_blueprint(ticket_routes, url_prefix='/ticket')
    app.register_blueprint(scan_routes)

    # Crée toutes les tables
    with app.app_context():
        db.create_all()

    return app