from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from ..crud import update_admin
from ..models import User, Ticket, Offre
from ..extensions import db
from ..routes import roles_required
from ..WTForms.forms import UpdateinfoForm, CreateuserForm, UpdateroleForm, AdminrechercheForm, DeleteuserForm

admin_routes = Blueprint('admin', __name__)




@admin_routes.route('/')
@login_required
@roles_required('admin')
def admin_dashboard():
    admin_recherche_form = AdminrechercheForm(request.args)
    create_user_form = CreateuserForm()
    update_role_form = UpdateroleForm()
    delete_user_form = DeleteuserForm()
    update_admin_form = UpdateinfoForm()

    user_info = db.session.query(User).filter_by(id=current_user.id).scalar()
    ticket = Ticket.query.filter_by(user_id=current_user.id).all()
    #offre = Offre.query.all()
    offres = Offre.query.order_by(Offre.bi_vendu.desc()).all()
    # search_query = request.args.get('q', '')
    search_query = admin_recherche_form.query.data or ''

    if search_query:
        users = db.session.execute(
            db.select(User).where(
                (User.nom.ilike(f'%{search_query}%')) | (User.prenom.ilike(f'%{search_query}%')) | (User.email.ilike(f'%{search_query}%'))
            )
        ).scalars().all()
    else:
        users = db.session.execute(db.select(User)).scalars().all()




        return render_template('admin_dashboard.html',user_info=user_info, users=users,
                               current_user=current_user, search_query=search_query,tickets=ticket, offres=offres,
                               create_user_form=create_user_form, update_role_form=update_role_form,
                               delete_user_form=delete_user_form, update_admin_form=update_admin_form
                               )



# @admin_routes.route('/', methods=['POST'])
# @login_required
# @roles_required('admin')
# def admin_dashboard_post():
#     create_user_form = CreateuserForm()
#     update_role_form = UpdateroleForm()
#     delete_user_form = DeleteuserForm()
#     update_admin_form = UpdateinfoForm()
#
#     # if 'create_user' in request.form:
#     if create_user_form.validate_on_submit() and create_user_form.create_user.data == 'create_user':
#
#         # email = request.form.get('email')
#         # nom = request.form.get('nom')
#         # prenom = request.form.get('prenom')
#         # password = request.form.get('password')
#         # role = request.form.get('role')
#
#         nom = create_user_form.nom.data
#         prenom = create_user_form.prenom.data
#         email = create_user_form.email.data
#         password = create_user_form.password.data
#         confirm_password = create_user_form.confirm_password.data
#         role = create_user_form.role.data
#
#
#         existing_user = db.session.execute(db.select(User).where(User.email == email)).scalar()
#         if existing_user:
#             flash("Email déjà utilisé.")
#             return redirect(url_for('admin.admin_dashboard'))
#
#         hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
#         new_user = User(email=email, nom=nom, prenom=prenom, password=hashed_password, role=role)
#         db.session.add(new_user)
#         db.session.commit()
#         flash(f"Utilisateur {nom} créé.")
#         return redirect(url_for('admin.admin_dashboard'))
#
#     # elif 'change_role' in request.form:
#     elif update_role_form.validate_on_submit() and update_role_form.update_role.data == 'update_role':
#         # user_id = request.form.get('user_id')
#         # selected_role = request.form.get('role')
#
#         user_id = update_role_form.user_id.data
#         selected_role = update_role_form.new_role.data
#
#         if selected_role in ['admin', 'employe', 'utilisateur']:
#             user = db.session.get(User, int(user_id))
#             if user:
#                 user.role = selected_role
#                 db.session.commit()
#                 flash(f"Rôle de {user.nom} {user.prenom} mis à jour.")
#             else:
#                 flash("Utilisateur non trouvé.")
#         else:
#             flash("Rôle invalide.")
#         return redirect(url_for('admin.admin_dashboard'))
#
#     # elif 'delete_user' in request.form:
#     elif delete_user_form.validate_on_submit() and delete_user_form.delete_user.data == 'delete_user':
#         user_id = update_role_form.user_id.data
#         user = db.session.get(User, int(user_id))
#         if user:
#             if int(user.id) == int(current_user.id):
#                 flash("Vous ne pouvez pas supprimer votre propre compte.")
#                 return redirect(url_for('admin.admin_dashboard'))
#             db.session.delete(user)
#             db.session.commit()
#             flash(f"Utilisateur {user.nom} {user.prenom} supprimé.")
#         else:
#             flash("Utilisateur non trouvé.")
#         return redirect(url_for('admin.admin_dashboard'))
#
#     # elif 'update_admin' in request.form:
#     elif update_admin_form.validate_on_submit() and update_admin_form.update_admin.data == 'update_admin':
#         #user = db.session.query(User).filter_by(id=current_user.id).scalar()
#         # user_id = request.form.get('user_id')
#         user_id = update_admin_form.user_id.data
#
#
#         # new_email = request.form.get('new_email')
#         # new_nom = request.form.get('new_nom')
#         # new_prenom = request.form.get('new_prenom')
#
#
#         new_nom = update_admin_form.new_nom.data
#         new_prenom = update_admin_form.new_prenom.data
#         new_email = update_admin_form.new_email.data
#
#         if user_id and user_id.isdigit():
#             user = db.session.get(User, int(user_id))
#         else:
#             flash("ID utilisateur invalide.")
#             return redirect(url_for('admin.admin_dashboard'))
#
#         if user:
#             # on bloque l’autoflush le temps du check
#             with db.session.no_autoflush:
#                 if new_email:
#                     existing_user = db.session.execute(
#                         db.select(User).where(User.email == new_email)
#                     ).scalar_one_or_none()
#
#                     if existing_user and existing_user.id != user.id:
#                         flash("Email déjà utilisé.")
#                         return redirect(url_for('admin.admin_dashboard'))
#
#                     user.email = new_email
#             if new_nom: user.nom = new_nom
#             if new_prenom: user.prenom = new_prenom
#
#             db.session.commit()
#             print(f"Mise à jour de l'user ID {current_user.id}")
#         else:
#             print("user non trouvé.")
#
#         return redirect(url_for('admin.admin_dashboard', create_user_form= create_user_form, update_role_form=update_role_form, delete_user_form=delete_user_form, update_admin_form=update_admin_form)
#



@admin_routes.route('/ticket/<int:ticket_id>', methods=['GET', 'POST'] )
@login_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template('ticket_details.html', ticket=ticket)

@admin_routes.route('/', methods=['POST', 'GET'])
@login_required
@roles_required('admin')
def admin_update():
    user = db.session.query(User).filter_by(id=current_user.id).scalar()
    if request.method == 'POST':

        #Ramene les "name" des input HTML
        new_email = request.form.get('new_email')
        new_nom = request.form.get('new_nom')
        new_prenom = request.form.get('new_prenom')


        # if user:
        #     if new_email: user.email = new_email
        #     if new_nom: user.nom = new_nom
        #     if new_prenom: user.prenom = new_prenom
        #
        #     # existing_user = db.session.execute(db.select(User).where(User.email == new_email)).scalar()
        #     # if existing_user:
        #     #     flash("Email déjà utilisé.")
        #     #     return redirect(url_for('admin.admin_dashboard'))
        #
        #     db.session.commit()
        #     print(f"Mise à jour de l'user ID {current_user.id}")
        # else:
        #     print("user non trouvé.")

        update_admin(
            new_email = user.email,
            new_nom = user.nom,
            new_prenom = user.prenom
        )
        db.session.commit()
    redirect(url_for('admin.admin_dashboard'))


@admin_routes.route('/', methods=['POST'])
@login_required
@roles_required('admin')
def admin_create_user():
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


@admin_routes.route('/', methods=['POST'])
@login_required
@roles_required('admin')
def admin_change_role():
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

@admin_routes.route('/', methods=['POST'])
@login_required
@roles_required('admin')
def admin_delete_user():
    user_id = request.form.get('user_id')
    user = db.session.get(User, int(user_id))
    if user:
        if user.id == current_user.id:
            flash("Vous ne pouvez pas supprimer votre propre compte.")
            return redirect(url_for('admin.admin_dashboard'))
        db.session.delete(user)
        db.session.commit()
        flash(f"Utilisateur {user.nom} {user.prenom} supprimé.")
    else:
        flash("Utilisateur non trouvé.")
    return redirect(url_for('admin.admin_dashboard'))

