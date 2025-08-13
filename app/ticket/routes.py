from flask import Blueprint, render_template, request, make_response, current_app
from flask_login import login_required
import base64
from weasyprint import HTML
import os
from ..models import Epreuve, Offre, User, Ticket


ticket_routes = Blueprint('ticket', __name__)


#PAGE DE PAIEMENT
@ticket_routes.route('/<int:ticket_id>', methods=['GET', 'POST'] )
@login_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template('ticket_details.html', ticket=ticket)

@ticket_routes.route('/<int:ticket_id>/pdf')
@login_required
def ticket_pdf(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    # Rendu HTML du ticket (tu peux réutiliser ton template)
    html_content = render_template('ticket_details.html', ticket=ticket)

    # Générer le PDF depuis le HTML
    pdf = HTML(string=html_content).write_pdf()

    # Définir le chemin de sauvegarde
    pdf_folder = os.path.join(current_app.static_folder, 'uploads', 'tickets')
    os.makedirs(pdf_folder, exist_ok=True)  # Crée le dossier si inexistant
    pdf_filename = f'ticket_{ticket.id}.pdf'
    pdf_path = os.path.join(pdf_folder, pdf_filename)

    # Sauvegarder le PDF
    with open(pdf_path, 'wb') as f:
        f.write(pdf)

    # Retourner le chemin relatif pour stocker en base si besoin
    return f'uploads/tickets/{pdf_filename}'


    #Retourner le PDF en téléchargement
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=ticket_{ticket.id}.pdf'
    return response
