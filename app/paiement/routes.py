from flask import Blueprint, render_template, request
from flask_login import login_user, logout_user, login_required, current_user

from ..models import Epreuve, Offre, User
from ..services.paiement_mock import FakePaymentGateway


paiement_routes = Blueprint('paiement', __name__)


#PAGE DE PAIEMENT
@paiement_routes.route('/<type_offre>', methods=['GET', 'POST'] )
@login_required
def paiement_epreuve(type_offre):

    offre = Offre.query.filter_by(type_offre=type_offre).first()

    if request.method == 'POST':
        card_number = request.form.get('card_number')
        montant = offre.prix

        # Création du mock
        gateway = FakePaymentGateway()
        result = gateway.process_paiement(card_number, montant) # Prend le prix direct de la bdd

        if result["status"] == "success":
            return render_template('paiement_success.html', transaction_id=result["transaction_id"])
        else:
            return render_template('paiement_failure.html', error=result["error"])


    return render_template('paiement.html', offre=offre, error="Merci de saisir un numéro de carte valide.")
