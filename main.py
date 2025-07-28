from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
load_dotenv()  # Charge les variables du .env
Bootstrap5(app)


class formFront(FlaskForm):
    pass

#Page d'accueil
@app.route("/")
def home():
    return render_template("home.html")




