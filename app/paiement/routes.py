from flask import Blueprint, render_template, request, current_app, send_file, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
import os
import hashlib
from ..models import Epreuve, Offre, User, Ticket
from ..services.paiement_mock import FakePaymentGateway
from ..services.qrcode import generate_qr_code
from ..services.ticket_pdf import generer_ticket_pdf
# from ..services.ticket_mail import send_ticket_email
from ..extensions import db,mail
from flask_mail import Message



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
        gateway = FakePaymentGateway() # " force_result="success" " Pour forcer le resultat en success
        result = gateway.process_paiement(card_number, montant) # Prend le prix direct de la bdd


        if result["status"] == "success":


            offre.bi_restant -= 1
            offre.bi_vendu += 1

            if offre.bi_restant < 0:
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
                    email = request.form.get(f"pers{i}_email")
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
                    qr_code=""
                )

                db.session.add(ticket)
                db.session.commit()

                # Génération QR code

                # Hash de la clef_user
                clef_user_hashed = hashlib.sha256(ticket.user.clef_user.encode()).hexdigest()

                # Hash de la clef_ticket
                clef_ticket_hashed = hashlib.sha256(ticket.clef_ticket.encode()).hexdigest()

                qr_data = f"clef_user:{clef_user_hashed}|clef_ticket:{clef_ticket_hashed}"
                filename = f"ticket_{ticket.id}.png"
                base_path = os.path.join(current_app.root_path, 'static', 'uploads', 'qrcodes')
                generate_qr_code(qr_data, filename, base_path)



                # Stocker le chemin relatif dans le ticket
                ticket.qr_code = f"uploads/qrcodes/{filename}"
                db.session.commit()  # commit avant envoi mail
                pdf_path = generer_ticket_pdf(ticket)
                #send_ticket_email(ticket.user, pdf_path)


                email = request.form.get("pers1_email")

                msg = Message(
                    subject="reception de votre paiement et ticket JO 2024",
                    recipients=[email],
                    body="Bonjour, ci-joint votre ticket pour l'événement.",
                )

                # Attacher le PDF depuis le disque
                full_pdf_path = os.path.join(current_app.static_folder, pdf_path)
                with open(full_pdf_path, "rb") as f:
                    msg.attach(
                        filename=f"ticket_{ticket.user.nom}_{ticket.offre.type_offre}_{ticket.id}.pdf",
                        content_type="application/pdf",
                        data=f.read()
                    )
                mail.send(msg)
                db.session.commit()

                flash("Paiement accepté ✅")
                #return render_template('paiement_success.html', status="success", ticket=ticket, ticket_id=ticket.id, qr_code=ticket.qr_code)
                if current_user.role == 'utilisateur':
                    return redirect(url_for('utilisateur.utilisateur_dashboard'))
                elif current_user.role == 'admin':
                    return redirect(url_for('admin.admin_dashboard'))
                elif current_user.role == 'employe':
                    return redirect(url_for('employe.employe_dashboard'))
        else:
            if offre.bi_restant < 0:
                offre.bi_restant = 0
                return ("Dommage, il ne reste plus de place!")
            return render_template('paiement_failure.html', error=result["error"])




    return render_template('paiement.html', offre=offre, error="Merci de saisir un numéro de carte valide.")
