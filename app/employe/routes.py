from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User, Ticket
from ..extensions import db
from ..routes import roles_required

employe_routes = Blueprint('employe', __name__)


@employe_routes.route('/')
@login_required
@roles_required('employe')
def employe_dashboard():
    ticket = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('employe.html', nom=current_user.nom, prenom=current_user.prenom, role=current_user.role,tickets=ticket)


@employe_routes.route('/', methods=['POST'])
@login_required
@roles_required('employe')
def employe_dashboard_post():
    if 'update_employe' in request.form:
        # user = db.session.query(User).filter_by(id=current_user.id).scalar()
        user_id = request.form.get('user_id')


        new_email = request.form.get('new_email')
        new_nom = request.form.get('new_nom')
        new_prenom = request.form.get('new_prenom')

        if user_id and user_id.isdigit():
            user = db.session.get(User, int(user_id))
        else:
            flash("ID utilisateur invalide.")
            return redirect(url_for('employe.employe_dashboard'))

        if user:
            # on bloque l’autoflush le temps du check
            with db.session.no_autoflush:
                if new_email:
                    existing_user = db.session.execute(
                        db.select(User).where(User.email == new_email)
                    ).scalar_one_or_none()

                    if existing_user and existing_user.id != user.id:
                        flash("Email déjà utilisé.")
                        return redirect(url_for('employe.employe_dashboard'))

                    user.email = new_email

            if new_nom: user.nom = new_nom
            if new_prenom: user.prenom = new_prenom

            db.session.commit()
            print(f"Mise à jour de l'user ID {current_user.id}")
        else:
            print("user non trouvé.")

        return redirect(url_for('employe.employe_dashboard'))

# PAGE DE TICKET
@employe_routes.route('/ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template('ticket_details.html', ticket=ticket)
