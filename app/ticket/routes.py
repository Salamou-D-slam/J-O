from flask import Blueprint, render_template,send_file
from flask_login import login_required
import os
from ..models import Epreuve, Offre, User, Ticket
from ..services.ticket_pdf import generer_ticket_pdf


ticket_routes = Blueprint('ticket', __name__)


# #PAGE DE PAIEMENT
# @ticket_routes.route('/<int:ticket_id>', methods=['GET', 'POST'] )
# @login_required
# def ticket_detail(ticket_id):
#     ticket = Ticket.query.get_or_404(ticket_id)
#     return render_template('ticket_details.html', ticket=ticket)


@ticket_routes.route('/<int:ticket_id>/pdf', methods=['POST'])
@login_required
def ticket_pdf(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    pdf_path = generer_ticket_pdf(ticket)
    return send_file(os.path.join("static", pdf_path),
                     as_attachment=True,
                     download_name=f"ticket_{ticket.user.nom}_{ticket.offre.type_offre}_{ticket.id}.pdf")


