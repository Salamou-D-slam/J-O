from flask import Blueprint, render_template, request,abort, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
import logging
from ..models import User, Ticket, Offre
from ..extensions import db
from ..routes import roles_required
from ..WTForms.forms import AdminrechercheForm, CreateuserForm, UpdateroleForm, DeleteuserForm, UpdateinfoForm



admin_routes = Blueprint('admin', __name__)




@admin_routes.route("/", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def admin_dashboard():
    admin_recherche_form = AdminrechercheForm(request.args)
    create_user_form = CreateuserForm()
    update_admin_form = UpdateinfoForm()
    update_admin_form.update_info_user_id.data = str(current_user.id)

    # Infos utilisateur connecté
    user_info = db.session.query(User).filter_by(id=current_user.id).scalar()
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    offres = Offre.query.order_by(Offre.bi_vendu.desc()).all()

    # Mise à jour profil admin
    if "update_admin" in request.form and update_admin_form.validate_on_submit():
        user_id = update_admin_form.update_info_user_id.data
        new_nom = update_admin_form.new_nom.data
        new_prenom = update_admin_form.new_prenom.data
        new_email = update_admin_form.new_email.data

        if not user_id:
            flash("Erreur : ID utilisateur manquant.")
            return redirect(url_for("admin.admin_dashboard"))

        user = db.session.get(User, int(user_id))
        if user:
            if new_email:
                existing_user = db.session.execute(
                    db.select(User).where(User.email == new_email)
                ).scalar_one_or_none()
                if existing_user and existing_user.id != user.id:
                    flash("Email déjà utilisé.")
                    return redirect(url_for("admin.admin_dashboard"))
                user.email = new_email
            if new_nom:
                user.nom = new_nom
            if new_prenom:
                user.prenom = new_prenom
            db.session.commit()
            flash("Profil mis à jour.")

            # Log
            logging.info(f"Profil admin mis à jour : ID {user.id}, email {user.email}")
        return redirect(url_for("admin.admin_dashboard"))

    # Recherche utilisateur
    search_query = admin_recherche_form.query.data or ""
    if search_query:
        users = db.session.execute(
            db.select(User).where(
                (User.nom.ilike(f"%{search_query}%"))
                | (User.prenom.ilike(f"%{search_query}%"))
                | (User.email.ilike(f"%{search_query}%"))
                | (User.role.ilike(f"%{search_query}%"))
            )
        ).scalars().all()
    else:
        users = db.session.execute(db.select(User)).scalars().all()


    # Création d'utilisateurs
    if "create_user" in request.form and create_user_form.validate_on_submit():
        nom = create_user_form.nom.data
        prenom = create_user_form.prenom.data
        email = create_user_form.email.data
        password = create_user_form.password.data
        role = create_user_form.role.data

        existing_user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if existing_user:
            flash("Email déjà utilisé.")
            return redirect(url_for("admin.admin_dashboard"))

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
        new_user = User(email=email, nom=nom, prenom=prenom, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Utilisateur {nom} créé.")

        # Log
        logging.info(f"Nouvel utilisateur créé : {email}, ID : {new_user.id}, rôle : {role}")
        return redirect(url_for("admin.admin_dashboard"))


    # Mise à jour rôle utilisateur
    update_role_forms = {u.id: UpdateroleForm() for u in users}
    delete_user_forms = {u.id: DeleteuserForm() for u in users}
    for u in users:
        # Formulaire changement rôle
        role_form = UpdateroleForm()
        role_form.new_role.data = u.role
        role_form.update_role_user_id.data = str(u.id)
        update_role_forms[u.id] = role_form

        # Formulaire suppression
        del_form = DeleteuserForm()
        del_form.delete_user_user_id.data = str(u.id)
        delete_user_forms[u.id] = del_form

    # Vérifie quel formulaire a été soumis
    if request.method == "POST":

        # Check suppression
        if "delete_user" in request.form:
            user_id = request.form.get("delete_user_user_id")
            user = db.session.get(User, int(user_id))

            if user.id == current_user.id:
                flash("Vous ne pouvez pas supprimer votre propre compte.")
            else:
                db.session.delete(user)
                db.session.commit()
                flash(f"Utilisateur {user.nom} {user.prenom} supprimé.")

                # Log
                logging.info(f"Utilisateur supprimé : ID {user.id}, email : {user.email}")
            return redirect(url_for("admin.admin_dashboard"))

        # Vérifie changement rôle
        user_id = request.form.get('update_role_user_id')
        form = update_role_forms[int(user_id)]
        new_role = request.form.get(form.new_role.name)
        if new_role in ['admin', 'employe', 'utilisateur']:
            user = db.session.get(User, int(user_id))
            if user:
                user.role = new_role
                db.session.commit()
                flash(f"Rôle de {user.nom} {user.prenom} mis à jour en {new_role}.")
                # Log
                logging.info(f"Rôle utilisateur modifié : ID {user.id}, nouveau rôle : {new_role}")
            else:
                flash("Utilisateur non trouvé.")
        else:
            flash("Rôle invalide.")


        return redirect(url_for('admin.admin_dashboard'))



    return render_template(
        "admin_dashboard.html",
        user_info=user_info,
        users=users,
        current_user=current_user,
        search_query=search_query,
        tickets=tickets,
        offres=offres,
        create_user_form=create_user_form,
        update_admin_form=update_admin_form,
        update_role_forms=update_role_forms,
        delete_user_forms=delete_user_forms,
        admin_recherche_form=admin_recherche_form,
    )

#-----------------------------------PAGE DE TICKET--------------------------------
@admin_routes.route('/ticket/<int:ticket_id>', methods=['GET', 'POST'] )
@login_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.user_id != current_user.id:
        abort(403)
    return render_template('ticket_details.html', ticket=ticket)
