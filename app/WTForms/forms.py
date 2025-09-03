from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, DateField, SubmitField, TextAreaField, SelectField, DecimalField,
                     DateTimeField, IntegerField, FileField, HiddenField, FormField)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
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
    update_role = HiddenField(default="change_role")
    update_role_user_id = HiddenField()
    new_role = SelectField("Nouveau rôle", choices=[
        ("utilisateur", "Utilisateur"),
        ("employe", "Employe"),
        ("admin", "Administrateur")], validators=[DataRequired()])
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
    new_email = StringField("Nouvel email", validators=[Email()])
    submit = SubmitField("Mettre à jour profil")

# EMPLOYE
class Updateinfo_employeForm(FlaskForm):
    update_employe = HiddenField(default="update_employe")
    update_info_user_id = HiddenField()
    new_nom = StringField("Nouveau nom")
    new_prenom = StringField("Nouveau prénom")
    new_email = StringField("Nouvel email", validators=[Email()])
    submit = SubmitField("Mettre à jour profil")

# UTILISATEUR
class Updateinfo_utilisateurForm(FlaskForm):
    update_utilisateur = HiddenField(default="update_utilisateur")
    update_info_user_id = HiddenField()
    new_nom = StringField("Nouveau nom")
    new_prenom = StringField("Nouveau prénom")
    new_email = StringField("Nouvel email", validators=[Email()])
    submit = SubmitField("Mettre à jour profil")


# EPREUVES FORMS
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

    new_submit = SubmitField("Modifier")

class EpreuvedetailForm(FlaskForm):
    submit = SubmitField("Suprrimer")

# FORMULAIRE DE PAIEMENT
class ParticipantForm(FlaskForm):
    # nom_pers1 = StringField("Nom", validators=[DataRequired()])
    # prenom_pers1 = StringField("Prénom", validators=[DataRequired()])
    # email_pers1 = StringField("Email", validators=[DataRequired(), Email()])

    pers1_nom = StringField("Nom", validators=[DataRequired()])
    pers1_prenom = StringField("Prénom", validators=[DataRequired()])
    pers1_email = StringField("Email", validators=[DataRequired(), Email()])

    pers2_nom = StringField("Nom")
    pers2_prenom = StringField("Prénom")

    pers3_nom = StringField("Nom")
    pers3_prenom = StringField("Prénom")

    pers4_nom = StringField("Nom")
    pers4_prenom = StringField("Prénom")

    nom_card = StringField("Nom card:", validators=[DataRequired()])
    card_number = IntegerField("Card number:", validators=[DataRequired()])
    expiration_card = IntegerField("Expiration card number:", validators=[DataRequired()])
    CVV_card = IntegerField("CV card:", validators=[DataRequired()])


    submit = SubmitField("Valider")

    def validate(self, offre_nombre_personne):

        # Validation dynamique selon le nombre de participants

        valid = super().validate()
        if not valid:
            return False
        # vérifier les champs supplémentaires selon le nombre de participants
        if offre_nombre_personne >= 2:
            if not self.pers2_nom.data or not self.pers2_prenom.data:
                self.pers2_nom.errors.append("Requis pour cette offre")
                self.pers2_prenom.errors.append("Requis pour cette offre")
                return False
        if offre_nombre_personne >= 3:
            if not self.pers3_nom.data or not self.pers3_prenom.data:
                self.pers3_nom.errors.append("Requis pour cette offre")
                self.pers3_prenom.errors.append("Requis pour cette offre")
                return False
        if offre_nombre_personne == 4:
            if not self.pers4_nom.data or not self.pers4_prenom.data:
                self.pers4_nom.errors.append("Requis pour cette offre")
                self.pers4_prenom.errors.append("Requis pour cette offre")
                return False
        return True

# TICKET PDF DL
class TicketForm(FlaskForm):
    ticket_id = HiddenField()
    submit = SubmitField("Valider")







