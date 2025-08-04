from flask import Flask
import os
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap
from app.extensions import db, login_manager
from app.routes import main_routes
from app.admin.routes import admin_routes

def create_app():
    load_dotenv()  # Charge des variables du .env

    app = Flask(__name__)

    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads') #Pour configuer le chemin des envoi des images
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # La taille maximal (max 16MB)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URI')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


    db.init_app(app)
    login_manager.init_app(app)
    bootstrap = Bootstrap(app)

    app.register_blueprint(main_routes)
    app.register_blueprint(admin_routes, url_prefix='/admin')

    with app.app_context():
        db.create_all()

    return app