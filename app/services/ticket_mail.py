# from flask_login import current_user
# from flask_mail import Message
# from ..extensions import mail
# from ..models import Epreuve, Offre, User, Ticket
# from ..services.ticket_pdf import generer_ticket_pdf
#
#
# def send_ticket_email(user, pdf_buffer):
#     ticket = Ticket.query.filter_by(user_id=current_user.id)
#     msg = Message(
#         subject="reception de votre paiement et ticket JO 2024",
#         recipients=[user.email],
#         body="Bonjour, ci-joint votre ticket pour l'événement."
#     )
#
#     # Attacher le PDF
#     msg.attach(
#         filename=f"ticket_{ticket.user.nom}_{ticket.offre.type_offre}_{ticket.id}.pdf",
#         content_type="application/pdf",
#         data=pdf_buffer.read()
#     )
#
#     mail.send(msg)
