from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, DateField, SubmitField, TextAreaField, SelectField, DecimalField,
                     DateTimeField, IntegerField, FileField, HiddenField, FormField)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, optional
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
class AdminrechercheForm(FlaskForm):
    query = StringField("Recherche")
    submit = SubmitField("Rechercher")


class CreateuserForm(FlaskForm):
    create_user = HiddenField(default="create_user")
    nom = StringField("Nom", validators=[DataRequired()])
    prenom = StringField("Prénom", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    role = SelectField("Rôle", choices=[
        ("utilisateur", "Utilisateur"),
        ("employe", "Employe"),
        ("admin", "Administrateur")], validators=[DataRequired()])
    submit = SubmitField("Créer utilisateur")


class UpdateroleForm(FlaskForm):
    update_role = HiddenField()
    update_role_user_id = HiddenField()
    new_role = SelectField("Nouveau rôle", choices=[
        ("admin", "Administrateur"),
        ("employe", "Employe"),
        ("utilisateur", "Utilisateur")
        ], validators=[DataRequired()])
    submit = SubmitField("Changer rôle")


class DeleteuserForm(FlaskForm):
    delete_user = HiddenField(default="delete_user")
    delete_user_user_id = HiddenField()
    delete = SubmitField("Supprimer")

# ADMIN
class UpdateinfoForm(FlaskForm):
    update_admin = HiddenField(default="update_admin")
    update_info_user_id = HiddenField()
    new_nom = StringField("Nouveau nom")
    new_prenom = StringField("Nouveau prénom")
    new_email = StringField("Nouvel email", validators=[Optional(),Email()])
    submit = SubmitField("Mettre à jour profil")

# EMPLOYE
class Updateinfo_employeForm(FlaskForm):
    update_employe = HiddenField(default="update_employe")
    update_info_user_id = HiddenField()
    new_nom = StringField("Nouveau nom")
    new_prenom = StringField("Nouveau prénom")
    new_email = StringField("Nouvel email", validators=[Optional(),Email()])
    submit = SubmitField("Mettre à jour profil")

# UTILISATEUR
class Updateinfo_utilisateurForm(FlaskForm):
    update_utilisateur = HiddenField(default="update_utilisateur")
    update_info_user_id = HiddenField()
    new_nom = StringField("Nouveau nom")
    new_prenom = StringField("Nouveau prénom")
    new_email = StringField("Nouvel email", validators=[Optional(),Email()])
    submit = SubmitField("Mettre à jour profil")


# EPREUVES FORMS
class AddepreuvesForm(FlaskForm):
    nom_epreuve = StringField("Nom de l'épreuve:", validators=[DataRequired()])
    # date_epreuve = DateTimeField("Date de l'épreuve:", format="%Y-%m-%d %H:%M", validators=[DataRequired()])
    date_epreuve = DateField("Date de l'épreuve:", format="%Y-%m-%d", validators=[DataRequired()])

    image = FileField("Image de l’epreuve:", validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], "Seulement des images JPG/PNG"),
        FileRequired("Une image est obligatoire")
    ])

    epreuve_submit = SubmitField("Ajouter l'épreuve")


class UpdateepreuvesForm(FlaskForm):
    new_nom_epreuve = StringField("Nom de l'épreuve:", validators=[Optional()])
    # new_date_epreuve = DateTimeField("Date de l'épreuve:", format="%Y-%m-%d %H:%M", validators=[DataRequired()])
    new_date_epreuve = DateField("Date de l'épreuve:", format="%Y-%m-%d", validators=[Optional()])

    new_prix_solo = DecimalField("Prix solo:", validators=[Optional()])
    new_nbr_place_solo = IntegerField("Nombre de place:", validators=[Optional()])

    new_prix_duo = DecimalField("Prix duo:", validators=[Optional()])
    new_nbr_place_duo = IntegerField("Nombre de place:", validators=[Optional()])

    new_prix_family = DecimalField("Prix family:", validators=[Optional()])
    new_nbr_place_family = IntegerField("Nombre de place:", validators=[Optional()])

    new_image = FileField("Image de l’epreuve:", validators=[Optional(),
        FileAllowed(['jpg', 'png', 'jpeg'], "Seulement des images JPG/PNG"),
    ])

    new_submit = SubmitField("Soumettre la Modification")

class EpreuvedetailForm(FlaskForm):
    submit = SubmitField("Suprrimer l'épreuve")


# Formulaire d'offres
class AddoffreForm(FlaskForm):
    nom_offre = StringField("Nom de l'offre:", validators=[DataRequired()])
    nombre_personne = IntegerField("Nombre de personnes:", validators=[DataRequired()])
    prix = DecimalField("Prix de l'offre:", validators=[DataRequired()])
    nbr_place = IntegerField("Nombre de place disponibles:", validators=[DataRequired()])

    submit = SubmitField("Ajouter l'offre")

class OffreUpdateForm(FlaskForm):
    new_nom_offre = StringField("Nom de l'offre:", validators=[Optional()])
    new_nombre_personne = IntegerField("Nombre de personnes:", validators=[Optional()])
    new_prix = DecimalField("Prix de l'offre:", validators=[Optional()])
    new_nbr_place = IntegerField("Nombre de place disponibles:", validators=[Optional()])

    new_submit = SubmitField("Ajouter l'offre")
    delete_submit = SubmitField("Supprimer l'offre")

from flask_wtf import FlaskForm
from wtforms import StringField, FormField, FieldList, SubmitField
from wtforms.validators import DataRequired

# Formulaire pour un participant
class PersonForm(FlaskForm):
    nom = StringField("Nom", validators=[DataRequired()])
    prenom = StringField("Prénom", validators=[DataRequired()])
    email = StringField("Email", validators=[Email()])  # facultatif

# Formulaire de paiement complet
class PaymentForm(FlaskForm):
    participants = FieldList(FormField(PersonForm), min_entries=1)
    nom_card = StringField("Nom card:", validators=[DataRequired()])
    card_number = IntegerField("Card number:", validators=[DataRequired()])
    expiration_card = IntegerField("Expiration card number:", validators=[DataRequired()])
    CVV_card = IntegerField("CV card:", validators=[DataRequired()])
    submit = SubmitField("Payer")


# TICKET PDF DL
class TicketForm(FlaskForm):
    ticket_id = HiddenField()
    submit = SubmitField("Valider")







