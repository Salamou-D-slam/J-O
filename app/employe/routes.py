from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User, Ticket
from ..extensions import db
from ..routes import roles_required
from ..WTForms.forms import Updateinfo_employeForm


employe_routes = Blueprint('employe', __name__)


@employe_routes.route('/', methods=['GET', 'POST'])
@login_required
@roles_required('employe')
def employe_dashboard():
    form = Updateinfo_employeForm()
    form.update_info_user_id.data = str(current_user.id)

    ticket = Ticket.query.filter_by(user_id=current_user.id).all()
    if "update_employe" in request.form and form.validate_on_submit():
        user_id = form.update_info_user_id.data
        new_nom = form.new_nom.data
        new_prenom = form.new_prenom.data
        new_email = form.new_email.data

        if not user_id:
            flash("Erreur : ID utilisateur manquant.")
            return redirect(url_for("employe.employe_dashboard"))

        user = db.session.get(User, int(user_id))
        if user:
            if new_email:
                existing_user = db.session.execute(
                    db.select(User).where(User.email == new_email)
                ).scalar_one_or_none()
                if existing_user and existing_user.id != user.id:
                    flash("Email déjà utilisé.")
                    return redirect(url_for("employe.employe_dashboard"))
                user.email = new_email
            if new_nom:
                user.nom = new_nom
            if new_prenom:
                user.prenom = new_prenom
            db.session.commit()
            flash("Profil mis à jour.")
        return redirect(url_for("employe.employe_dashboard"))
    return render_template('employe.html', nom=current_user.nom, prenom=current_user.prenom, role=current_user.role,tickets=ticket, form=form)

#
# @employe_routes.route('/', methods=['POST'])
# @login_required
# @roles_required('employe')
# def employe_dashboard_post():
#     if "update_admin" in request.form and form.validate_on_submit():
#         user_id = form.update_info_user_id.data
#         new_nom = form.new_nom.data
#         new_prenom = form.new_prenom.data
#         new_email = form.new_email.data
#
#         if not user_id:
#             flash("Erreur : ID utilisateur manquant.")
#             return redirect(url_for("admin.admin_dashboard"))
#
#         user = db.session.get(User, int(user_id))
#         if user:
#             if new_email:
#                 existing_user = db.session.execute(
#                     db.select(User).where(User.email == new_email)
#                 ).scalar_one_or_none()
#                 if existing_user and existing_user.id != user.id:
#                     flash("Email déjà utilisé.")
#                     return redirect(url_for("admin.admin_dashboard"))
#                 user.email = new_email
#             if new_nom:
#                 user.nom = new_nom
#             if new_prenom:
#                 user.prenom = new_prenom
#             db.session.commit()
#             flash("Profil mis à jour.")
#         return redirect(url_for("admin.admin_dashboard"))

# PAGE DE TICKET
@employe_routes.route('/ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template('ticket_details.html', ticket=ticket)
