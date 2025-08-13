import os
import qrcode

def generate_and_save_qr_code(data: str, filename: str, base_path: str):
    """
    Génère un QR code pour la data, et sauvegarde dans base_path/filename

    Args:
        data: chaîne à encoder dans le QR code
        filename: nom du fichier (ex: "ticket_123.png")
        base_path: chemin absolu du dossier où sauvegarder le fichier (ex: "static/uploads/qr_codes/")
    """
    qr = qrcode.QRCode(
        version=1,
        #error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    full_path = os.path.join(base_path, filename)
    img.save(full_path)

    return full_path
