from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, TextAreaField, SelectField, DecimalField, DateTimeField, IntegerField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileAllowed, FileRequired



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
    nom_epreuve = StringField("Nom de l'épreuve:", validators=[DataRequired()])
    # date_epreuve = DateTimeField("Date de l'épreuve:", format="%Y-%m-%d %H:%M", validators=[DataRequired()])
    date_epreuve = DateField("Date de l'épreuve:", format="%Y-%m-%d", validators=[DataRequired()])

    prix_solo = DecimalField("Prix solo:", validators=[DataRequired()])
    nbr_place_solo = IntegerField("Nombre de place:", validators=[DataRequired()])

    prix_duo = DecimalField("Prix duo:", validators=[DataRequired()])
    nbr_place_duo = IntegerField("Nombre de place:", validators=[DataRequired()])

    prix_family = DecimalField("Prix family:", validators=[DataRequired()])
    nbr_place_family = IntegerField("Nombre de place:", validators=[DataRequired()])

    image = FileField("Image de l’epreuve:", validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], "Seulement des images JPG/PNG"),
        FileRequired("Une image est obligatoire")
    ])

    submit = SubmitField("Ajouter")





