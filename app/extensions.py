from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager


class Base(DeclarativeBase): # Base commune à tous tes modèles SQLAlchemy
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Redirige à la page de login page si user n'est pas connecter
login_manager.login_message_category = 'info' # Message d'erreur en Boostrap