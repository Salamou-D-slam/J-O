from flask import current_app
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm



def generer_ticket_pdf(ticket):


    pdf_folder = os.path.join(current_app.static_folder, 'uploads', 'tickets')
    os.makedirs(pdf_folder, exist_ok=True) # Crée le dossier s'il n'existe pas

    pdf_filename = f"ticket_{ticket.user.nom}_{ticket.offre.type_offre}_{ticket.id}.pdf"
    pdf_path = os.path.join(pdf_folder, pdf_filename)

    # Création du PDF
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Infos Ticket
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20 * mm, height - 30 * mm, f"Ticket n°{ticket.id}")

    c.setFont("Helvetica", 12)
    c.drawString(20 * mm, height - 45 * mm, f"Nom : {ticket.user.nom} {ticket.user.prenom}")
    c.drawString(20 * mm, height - 55 * mm, f"Email : {ticket.user.email}")
    c.drawString(20 * mm, height - 70 * mm, f"Offre : {ticket.offre.type_offre}")
    c.drawString(20 * mm, height - 80 * mm, f"Épreuve : {ticket.offre.epreuve.nom_epreuve}")
    c.drawString(20 * mm, height - 90 * mm, f"Date : {ticket.offre.epreuve.date_epreuve.strftime('%d/%m/%Y %H:%M')}")
    c.drawString(20 * mm, height - 100 * mm, f"Prix : {ticket.offre.prix} €")
   # c.drawString(20 * mm, height - 120 * mm, f"Personnes concernés : {ticket.pers_data}")


    # Rendre ma table qui en jsonb en liste python
    personnes = ticket.pers_data or []
    emails = ticket.pers_data or []

    c.setFont("Helvetica-Bold", 14)
    c.drawString(20 * mm, height - 120 * mm, "Personnes concernées :")

    y_position = height - 130 * mm
    c.setFont("Helvetica", 12)

    for p in personnes:
        nom = p.get("nom", "")
        prenom = p.get("prenom", "")
        email = p.get("email", "")

        # Afficher seulement si au moins nom ou prénom
        if nom or prenom:
            text = f"- {prenom} {nom}"
            if email:  # ajouter l'email si présent
                text += f" - {email}"

        c.drawString(25 * mm, y_position, f"- {prenom} {nom} - {email}")
        y_position -= 8 * mm
        c.drawString(20 * mm, height - 60 * mm, f"Email de réception du ticket : {email}")


    # QR Code
    qr_path = os.path.join(current_app.static_folder, 'uploads', 'qrcodes', f"ticket_{ticket.id}.png")
    # Vu que le qr code est déja crée dans la route du paiement, je dois juste le trouver grace aux chemin


    # Insérer QR code dans le PDF
    c.drawImage(qr_path, 150 * mm, height - 80 * mm, width=40 * mm, height=40 * mm)

    c.showPage()
    c.save()

    return f"uploads/tickets/{pdf_filename}"
