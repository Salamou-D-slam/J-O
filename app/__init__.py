from flask import Flask
import os
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap
from app.extensions import db, login_manager
from app.routes import main_routes
from app.admin.routes import admin_routes
from app.employe.routes import employe_routes
from app.paiement.routes import paiement_routes
from app.ticket.routes import ticket_routes
from app.scan.routes import scan_routes



def create_app():
    load_dotenv()  # Charge des variables du .env

    app = Flask(__name__)

    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads/image') # Config le chemin des envoi des images
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # La taille maximal (max 16MB)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URI') # Config la bdd
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Désactiver le système de signal de modification de SQLAlchemy

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


    db.init_app(app)
    login_manager.init_app(app) # Un gestionnaire d’authentification fourni par Flask-Login
    bootstrap = Bootstrap(app) # Pour utiliser le boostrap dans les templates Jinja2

    app.register_blueprint(main_routes)
    app.register_blueprint(admin_routes, url_prefix='/admin')
    app.register_blueprint(employe_routes, url_prefix='/employe')
    app.register_blueprint(paiement_routes, url_prefix='/paiement')
    app.register_blueprint(ticket_routes, url_prefix='/ticket')
    app.register_blueprint(scan_routes)

    # Crée toutes les tables
    with app.app_context():
        db.create_all()

    return app