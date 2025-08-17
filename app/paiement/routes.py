from flask import Blueprint, render_template, request, current_app, send_file
from flask_login import login_user, logout_user, login_required, current_user
import qrcode
import os
import json
from datetime import datetime

from ..models import Epreuve, Offre, User, Ticket
from ..services.paiement_mock import FakePaymentGateway
from ..services.qrcode import generate_qr_code
from ..extensions import db
from ..services.ticket_pdf import generer_ticket_pdf




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
        gateway = FakePaymentGateway(force_result="success")
        result = gateway.process_paiement(card_number, montant) # Prend le prix direct de la bdd

        if result["status"] == "success":


            offre.bi_restant -= 1
            offre.bi_vendu += 1

            if offre.bi_restant < 0:
                offre.bi_restant = 0
                return ("Dommage, il ne reste plus de place!")


            else:
                # pers1_nom = request.form.get("pers1_nom")
                # pers1_prenom = request.form.get("pers1_prenom")
                # pers1_email = request.form.get("pers1_email")
                #
                # pers2_nom = request.form.get("pers2_nom")
                # pers2_prenom = request.form.get("pers2_prenom")
                #
                # pers3_nom = request.form.get("pers3_nom")
                # pers3_prenom = request.form.get("pers3_prenom")
                #
                # pers4_nom = request.form.get("pers4_nom")
                # pers4_prenom = request.form.get("pers4_prenom")
                participants = []

                for i in range(1, 5):
                    nom = request.form.get(f"pers{i}_nom")
                    prenom = request.form.get(f"pers{i}_prenom")
                    email = request.form.get(f"pers{i}_email")  # optionnel pour i>1
                    if nom and prenom:  # on ajoute seulement si remplis
                        participant = {"nom": nom, "prenom": prenom}
                        if email:
                            participant["email"] = email
                        participants.append(participant)


                ticket = Ticket(
                    user_id=current_user.id,
                    offre_id=offre.id,

                    pers_data=participants,
                    # pers1_nom = pers1_nom,
                    # pers1_prenom = pers1_prenom,
                    # pers1_email = pers1_email,
                    #
                    # pers2_nom = pers2_nom,
                    # pers2_prenom = pers2_prenom,
                    #
                    # pers3_nom = pers3_nom,
                    # pers3_prenom = pers3_prenom,
                    #
                    # pers4_nom = pers4_nom,
                    # pers4_prenom = pers4_prenom,
                    qr_code=""  # provisoire, on le remplira après génération
                )

                db.session.add(ticket)
                db.session.commit()

                # Génération QR code
                qr_data = f"clef_user:{ticket.user.clef_user}|clef_ticket:{ticket.clef_ticket}"
                filename = f"ticket_{ticket.id}.png"
                base_path = os.path.join(current_app.root_path, 'static', 'uploads', 'qrcodes')
                generate_qr_code(qr_data, filename, base_path)



                # Stocker le chemin relatif dans le ticket
                ticket.qr_code = f"uploads/qrcodes/{filename}"
                db.session.commit()


                return render_template('paiement_success.html', status="success", ticket=ticket, ticket_id=ticket.id, qr_code=ticket.qr_code ) #transaction_id=result["transaction_id"]
        else:
            return render_template('paiement_failure.html', error=result["error"])




    return render_template('paiement.html', offre=offre, error="Merci de saisir un numéro de carte valide.")
