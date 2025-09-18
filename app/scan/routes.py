from flask import Blueprint, render_template, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from ..routes import roles_required
from ..models import Ticket
from app.extensions import db, login_manager




scan_routes = Blueprint("scan", __name__)

@scan_routes.route("/scan")
@login_required
@roles_required('admin', 'employe')
def scan():
    return render_template("scan.html")


@scan_routes.route("/api/validate_ticket/<ticket_id>")
@login_required
@roles_required('admin', 'employe')
def validate_ticket(ticket_id):

    ticket = Ticket.query.filter_by(id=ticket_id).first()

    # if ticket.status == "valide":
    #     ticket.status_tent -= 1
    #     ticket.status == "expire"
    #     return jsonify({"valid": "valide", "message": "Ticket valide !"})
    #
    # if ticket.status_tent <= 0:
    #     return jsonify({"valid": "expire", "message": "Ticket déjà utilisé"}), 400
    #
    # if ticket.status_tent < 0:
    #     ticket.status_tent = 0
    #
    # if not ticket:
    #     return jsonify({"valid": None, "message": "Ticket invalide"}), 404

    # Si le ticket n'existe pas
    if not ticket:
        return jsonify({"valid": False, "message": "Ticket inexistant, accès refusé"}), 404

    # Si le ticket a déja été utilisé
    if ticket.status == "invalide":
        return jsonify({"valid": False, "message": "expiration: Ticket déjà utilisé, accès refusé"}), 400

    # Si le ticket est valide -> on le rend invalide
    ticket.status = "invalide"
    db.session.commit()

    return jsonify({"valid": True, "message": "Ticket valide, accès autorisé"})
