from flask import Flask
import os
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap5
from app.extensions import db
from app.routes import main_routes, auth_routes

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URI')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    load_dotenv()  # Charge les variables du .env
    db.init_app(app)
    Bootstrap5(app)

    app.register_blueprint(main_routes)  # si routes en blueprint
    app.register_blueprint(auth_routes)

    with app.app_context():
        db.create_all()

    return app