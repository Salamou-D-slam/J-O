from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from ..models import User
from ..extensions import db
from ..routes import roles_required


admin_routes = Blueprint('admin', __name__)




@admin_routes.route('/')
@login_required
@roles_required('admin')
def admin_dashboard():
    user_info = db.session.query(User).filter_by(id=current_user.id).scalar()
    search_query = request.args.get('q', '')
    if search_query:
        users = db.session.execute(
            db.select(User).where(
                (User.nom.ilike(f'%{search_query}%')) | (User.prenom.ilike(f'%{search_query}%')) | (User.email.ilike(f'%{search_query}%'))
            )
        ).scalars().all()
    else:
        users = db.session.execute(db.select(User)).scalars().all()
    return render_template('admin_dashboard.html',user_info=user_info, users=users, current_user=current_user, search_query=search_query)



@admin_routes.route('/', methods=['POST'])
@login_required
@roles_required('admin')
def admin_dashboard_post():
    if 'create_user' in request.form:
        email = request.form.get('email')
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        password = request.form.get('password')
        role = request.form.get('role')

        existing_user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if existing_user:
            flash("Email déjà utilisé.")
            return redirect(url_for('admin.admin_dashboard'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        new_user = User(email=email, nom=nom, prenom=prenom, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Utilisateur {nom} créé.")
        return redirect(url_for('admin.admin_dashboard'))

    elif 'change_role' in request.form:
        user_id = request.form.get('user_id')
        selected_role = request.form.get('role')
        if selected_role in ['admin', 'employe', 'utilisateur']:
            user = db.session.get(User, int(user_id))
            if user:
                user.role = selected_role
                db.session.commit()
                flash(f"Rôle de {user.nom} {user.prenom} mis à jour.")
            else:
                flash("Utilisateur non trouvé.")
        else:
            flash("Rôle invalide.")
        return redirect(url_for('admin.admin_dashboard'))

    elif 'delete_user' in request.form:
        user_id = request.form.get('user_id')
        user = db.session.get(User, int(user_id))
        if user:
            if int(user.id) == int(current_user.id):
                flash("Vous ne pouvez pas supprimer votre propre compte.")
                return redirect(url_for('admin.admin_dashboard'))
            db.session.delete(user)
            db.session.commit()
            flash(f"Utilisateur {user.nom} {user.prenom} supprimé.")
        else:
            flash("Utilisateur non trouvé.")
        return redirect(url_for('admin.admin_dashboard'))

    elif 'update_admin' in request.form:
        #user = db.session.query(User).filter_by(id=current_user.id).scalar()
        user_id = request.form.get('user_id')

        new_email = request.form.get('new_email')
        new_nom = request.form.get('new_nom')
        new_prenom = request.form.get('new_prenom')

        if user_id and user_id.isdigit():
            user = db.session.get(User, int(user_id))
        else:
            flash("ID utilisateur invalide.")
            return redirect(url_for('admin.admin_dashboard'))

        if user:
            # on bloque l’autoflush le temps du check
            with db.session.no_autoflush:
                if new_email:
                    existing_user = db.session.execute(
                        db.select(User).where(User.email == new_email)
                    ).scalar_one_or_none()

                    if existing_user and existing_user.id != user.id:
                        flash("Email déjà utilisé.")
                        return redirect(url_for('admin.admin_dashboard'))

                    user.email = new_email
            if new_nom: user.nom = new_nom
            if new_prenom: user.prenom = new_prenom

            db.session.commit()
            print(f"Mise à jour de l'user ID {current_user.id}")
        else:
            print("user non trouvé.")

        return redirect(url_for('admin.admin_dashboard'))



# @admin_routes.route('/', methods=['POST', 'GET'])
# @login_required
# @roles_required('admin')
# def admin_update():
#     user = db.session.query(User).filter_by(id=current_user.id).scalar()
#     if request.method == 'POST':
#
#         #Ramene les "name" des input HTML
#         new_email = request.form.get('new_email')
#         new_nom = request.form.get('new_nom')
#         new_prenom = request.form.get('new_prenom')
#
#
#         # if user:
#         #     if new_email: user.email = new_email
#         #     if new_nom: user.nom = new_nom
#         #     if new_prenom: user.prenom = new_prenom
#         #
#         #     # existing_user = db.session.execute(db.select(User).where(User.email == new_email)).scalar()
#         #     # if existing_user:
#         #     #     flash("Email déjà utilisé.")
#         #     #     return redirect(url_for('admin.admin_dashboard'))
#         #
#         #     db.session.commit()
#         #     print(f"Mise à jour de l'user ID {current_user.id}")
#         # else:
#         #     print("user non trouvé.")
#
#         update_admin(
#             new_email = user.email,
#             new_nom = user.nom,
#             new_prenom = user.prenom
#         )
#         db.session.commit()
#     redirect(url_for('admin.admin_dashboard'))


# @admin_routes.route('/', methods=['POST'])
# @login_required
# @roles_required('admin')
# def admin_create_user():
#     email = request.form.get('email')
#     nom = request.form.get('nom')
#     prenom = request.form.get('prenom')
#     password = request.form.get('password')
#     role = request.form.get('role')
#
#     existing_user = db.session.execute(db.select(User).where(User.email == email)).scalar()
#     if existing_user:
#         flash("Email déjà utilisé.")
#         return redirect(url_for('admin.admin_dashboard'))
#
#     hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
#     new_user = User(email=email, nom=nom, prenom=prenom, password=hashed_password, role=role)
#     db.session.add(new_user)
#     db.session.commit()
#     flash(f"Utilisateur {nom} créé.")
#     return redirect(url_for('admin.admin_dashboard'))
#
#
# @admin_routes.route('/', methods=['POST'])
# @login_required
# @roles_required('admin')
# def admin_change_role():
#     user_id = request.form.get('user_id')
#     selected_role = request.form.get('role')
#     if selected_role in ['admin', 'employe', 'utilisateur']:
#         user = db.session.get(User, int(user_id))
#         if user:
#             user.role = selected_role
#             db.session.commit()
#             flash(f"Rôle de {user.nom} {user.prenom} mis à jour.")
#         else:
#             flash("Utilisateur non trouvé.")
#     else:
#         flash("Rôle invalide.")
#     return redirect(url_for('admin.admin_dashboard'))
#
# @admin_routes.route('/', methods=['POST'])
# @login_required
# @roles_required('admin')
# def admin_delete_user():
#     user_id = request.form.get('user_id')
#     user = db.session.get(User, int(user_id))
#     if user:
#         if user.id == current_user.id:
#             flash("Vous ne pouvez pas supprimer votre propre compte.")
#             return redirect(url_for('admin.admin_dashboard'))
#         db.session.delete(user)
#         db.session.commit()
#         flash(f"Utilisateur {user.nom} {user.prenom} supprimé.")
#     else:
#         flash("Utilisateur non trouvé.")
#     return redirect(url_for('admin.admin_dashboard'))

