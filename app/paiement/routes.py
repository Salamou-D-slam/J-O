from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from ..models import Offre, Ticket
from ..services.paiement_mock import FakePaymentGateway
from ..services.qrcode import generate_qr_code
from ..services.ticket_pdf import generer_ticket_pdf
from ..extensions import db, mail
from flask_mail import Message
from ..WTForms.forms import PaymentForm, PersonForm
import hashlib, os, logging

paiement_routes = Blueprint('paiement', __name__)

@paiement_routes.route('/<type_offre>', methods=['GET', 'POST'])
@login_required
def paiement_epreuve(type_offre):
    offre = Offre.query.filter_by(type_offre=type_offre).first()
    if not offre:
        return "Offre introuvable !"

    nb_personnes = offre.nombre_personne

    form = PaymentForm()

    # Ajuster dynamiquement le FieldList selon nombre de personnes
    while len(form.participants.entries) < nb_personnes:
        form.participants.append_entry()

    if request.method == "POST" and form.validate():
        # Paiement mock
        card_number = form.card_number.data
        montant = offre.prix
        gateway = FakePaymentGateway()
        result = gateway.process_paiement(card_number, montant)

        if result["status"] == "success":
            # Mise à jour de l'offre
            offre.bi_restant -= 1
            offre.bi_vendu += 1
            if offre.bi_restant < 0:
                offre.bi_restant = 0
                db.session.commit()
                return "Dommage, il ne reste plus de place!"

            # Création liste participants
            participants = []
            for p in form.participants.data:
                participants.append({
                    "nom": p["nom"],
                    "prenom": p["prenom"],
                    "email": p.get("email")
                })

            # Création du ticket
            ticket = Ticket(
                user_id=current_user.id,
                offre_id=offre.id,
                pers_data=participants,
                qr_code=""
            )
            db.session.add(ticket)
            db.session.commit()

            # Génération QR code
            clef_user_hashed = hashlib.sha256(ticket.user.clef_user.encode()).hexdigest()
            clef_ticket_hashed = hashlib.sha256(ticket.clef_ticket.encode()).hexdigest()
            qr_data = f"clef_user:{clef_user_hashed}|clef_ticket:{clef_ticket_hashed}"
            filename = f"ticket_{ticket.id}.png"
            base_path = os.path.join(current_app.root_path, 'static', 'uploads', 'qrcodes')
            generate_qr_code(qr_data, filename, base_path)
            ticket.qr_code = f"uploads/qrcodes/{filename}"
            db.session.commit()

            # Génération PDF
            pdf_path = generer_ticket_pdf(ticket)

            # Envoi mail au premier participant
            email = form.participants.entries[0].form.email.data
            if email:
                msg = Message(
                    subject="Réception de votre paiement et ticket JO 2024",
                    recipients=[email],
                    body="Bonjour, ci-joint votre ticket pour l'événement.",
                )
                full_pdf_path = os.path.join(current_app.static_folder, pdf_path)
                with open(full_pdf_path, "rb") as f:
                    msg.attach(
                        filename=f"ticket_{ticket.user.nom}_{ticket.offre.type_offre}_{ticket.id}.pdf",
                        content_type="application/pdf",
                        data=f.read()
                    )
                mail.send(msg)

            flash("Paiement accepté ✅")
            logging.info(f"Paiement mock effectué : ticket {ticket.id}, utilisateur {ticket.user_id}, montant {offre.prix}")

            # Redirection selon rôle
            if current_user.role == 'utilisateur':
                return redirect(url_for('utilisateur.utilisateur_dashboard'))
            elif current_user.role == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            elif current_user.role == 'employe':
                return redirect(url_for('employe.employe_dashboard'))

        else:
            return render_template('paiement_failure.html', error=result.get("error", "Erreur de paiement"))

    return render_template('paiement.html', offre=offre, form=form)
