from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
import logging
import os

class Base(DeclarativeBase): # Base commune à tous tes modèles SQLAlchemy
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Redirige à la page de login page si user n'est pas connecter
login_manager.login_message_category = 'info' # Message d'erreur en Boostrap

mail = Mail()
csrf = CSRFProtect()


# Créer le dossier logs si inexistant
if not os.path.exists('logs'):
    os.mkdir('logs')

# Configuration globale du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s', # format des logs
    handlers = [
    logging.FileHandler('logs/app.log', encoding='utf-8'),  # fichier UTF-8
    logging.StreamHandler()  # affiche aussi les logs dans la console
]
)