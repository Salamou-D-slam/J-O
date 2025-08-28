from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# Formulaire de connexion
class LoginForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe:", validators=[DataRequired()])
    submit = SubmitField("Se connecter")

# Formulaire d'inscription
class RegisterForm(FlaskForm):
    nom = StringField("Nom:", validators=[DataRequired()])
    prenom = StringField("Prenom:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe:", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmer le mot de passe:", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("S'inscrire")

# Formulaire de contact
class ContactForm(FlaskForm):
    nom = StringField("Nom:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    message = TextAreaField("Message:", validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Envoyer")

# Dashboards
class UpdateinfoForm(FlaskForm):
    new_nom = StringField("Nouveau Nom:",)
    new_prenom = StringField("Nouveau Prenom:",)
    new_email = StringField("Nouveau Email:", validators=[Email()])
    submit = SubmitField("Modifier")


# COTE ADMIN
class CreateuserForm(FlaskForm):
    nom = StringField("Nom:", validators=[DataRequired()])
    prenom = StringField("Prenom:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe:", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmer le mot de passe:", validators=[DataRequired(), EqualTo('password')])
    role = SelectField("Rôle:", choices=[
        ("utilisateur", "Utilisateur"),
        ("employe", "Employe"),
        ("admin", "Administrateur")
    ], validators=[DataRequired()])
    submit = SubmitField("Crée un nouvel utilisateur")

# Maj des roles utilisateurs
class UpdateroleForm(FlaskForm):
    new_role = SelectField("Rôle:", choices=[
        ("utilisateur", "Utilisateur"),
        ("employe", "Employe"),
        ("admin", "Administrateur")
    ], validators=[DataRequired()])
    submit = SubmitField("Mettre à jours")

# Barre de recharche des utilisateurs
class AdminrechercheForm(FlaskForm):
    query = StringField("Rechercher un utilisateur")
    submit = SubmitField("Rechercher")

class AddepreuvesForm(FlaskForm):
    nom = StringField("Nom:", validators=[DataRequired()])


