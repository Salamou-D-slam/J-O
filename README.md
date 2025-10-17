# Jeux Olympique - Application de Billetterie

Application web développée avec **Flask**, **Jinja2**, et **PostgreSQL**, permettant la gestion des billets pour les Jeux Olympiques 2024.

lien de l'application hébérgé: https://jeux-olympique.fly.dev/
---
## Fonctionnalités

- Page d'accueil : Présentation de l'événement.

- Page des épreuves : Affichage des différents épreuves disponibles.
  
- Page d'une épreuve : Affichage des détails de l'épreuve et ses trois offre qu'on peut acheter avec leurs dtail (prix, place etc...).
  
- Page de paiement: Un formulaire pour payer l'offre choisi (rappeleons que ce n'est qu'une simulation et pas un vrai paiement).
  
- Fonctionnalité d'envoi de mail: Après avoir acheter une offre, on reçoit un mail qui contient les informations du ticket ainsi qu'un QR code. On peut envoyer un message à l'administration sous de mail grâce à la page de contact (vous pourrez vérifier vos mils envoyé depuis votre boite mail)
  
- Page contact : le formulaire de contact .

- Page de profil : Espace de profil, ou on peut consulter nos informations personnelle et les modifier. On peut aussi voir nos ticket acheté et les télécharger.

- Validation de ticket: L'administrateur et l'employé peuvent valider vos ticket grâce au numéro de ticket.
  
- CRUD: L'administrateur et/ou l'employé peuvent crée, lire, mettre à jour et supprimer:
    - Des épreuves
    - Des utilisateurs
  
## Technologies utilisées
- HTML5
- CSS3 (avec un peu de SASS)
- BOOTSTRAP
- JavaScript
- Python avec Jinja2
- Base de données: PostgresSQL
- Outils de déploiement: Fly.io

## 1️⃣ Installation locale
- ## Prérequis

- Python 3.13+
- Docker
- Docker Compose
- Compte Fly.io pour déploiement (optionnel)

### Cloner le projet
```bash
git clone J-O
cd "Jeux Olympique"



# Créer un environnement virtuel et installer les dépendances

python -m venv .venv

## Activer l'environnement

# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Flask
flask run

# Ou avec Gunicorn (production locale)
gunicorn -w 4 -b 0.0.0.0:8000 main:app

### 2️⃣ Utilisation avec Docker

# Construire l’image Docker
docker build -t jeux-olympique .


# Lancer le conteneur
docker run -p 8000:8000 jeux-olympique
# L’application sera accessible sur http://localhost:8000
# Vérifiez bien les port dans le fichier dockerfile et docker compose.yml

### 3️⃣ Déploiement sur Fly.io

#Installer Fly CLI dans le poweshell (lancez le en mode administrateur si ça ne marche pas)
curl -L https://fly.io/install.sh | sh

# Se connecter à Fly.io
fly auth login

#Lancer l’application et créer l’app Fly
fly launch
#Lors de la configuration, vous pouvez créer un Managed Postgres si nécessaire.

#Déployer une mise à jour
fly deploy

#Configurer les variables d’environnement
fly secrets set SECRET_KEY=<votre_secret>
fly secrets set DATABASE_URL=<url_de_votre_bdd>
fly secrets set DATABASE_TEST_URI=<url_de_votre_bdd_test>
fly secrets set ADMIN_MDP=<votre_mdp_espace_admin>
fly secrets set MAIL_USERNAME=<mail_qui_envoi_auto_le_ticket_par_mail>
fly secrets set MAIL_DEFAULT_SENDER=<email_defaut_sender>
fly secrets set MAIL_JO=<mail_qui_reçoit_les_msg_contact>



