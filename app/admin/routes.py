from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from ..models import User
from ..extensions import db

admin_routes = Blueprint('admin', __name__)

def role_required(role):
    def decorator(f):
        from functools import wraps
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@admin_routes.route('/')
@login_required
@role_required('admin')
def admin_dashboard():
    search_query = request.args.get('q', '')
    if search_query:
        users = db.session.execute(
            db.select(User).where(
                (User.nom.ilike(f'%{search_query}%')) | (User.prenom.ilike(f'%{search_query}%')) | (User.email.ilike(f'%{search_query}%'))
            )
        ).scalars().all()
    else:
        users = db.session.execute(db.select(User)).scalars().all()
    return render_template('admin_dashboard.html', users=users, current_user=current_user, search_query=search_query)



@admin_routes.route('/', methods=['POST'])
@login_required
@role_required('admin')
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
            if user.id == current_user.id:
                flash("Vous ne pouvez pas supprimer votre propre compte.")
                return redirect(url_for('admin.admin_dashboard'))
            db.session.delete(user)
            db.session.commit()
            flash(f"Utilisateur {user.nom} {user.prenom} supprimé.")
        else:
            flash("Utilisateur non trouvé.")
        return redirect(url_for('admin.admin_dashboard'))

    @admin_routes.route('/')
    @login_required
    @role_required('employe')
    def employe_panel():
        render_template("employe.html")
