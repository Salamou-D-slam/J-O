from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from ..routes import roles_required
from functools import wraps

employe_bp = Blueprint('employe', __name__)


@employe_bp.route('/')
@login_required
@roles_required('employe')
def employe_dashboard():
    return render_template('employe.html', nom=current_user.nom, prenom=current_user.prenom, role=current_user.role)
