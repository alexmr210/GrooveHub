from flask import render_template
from flask_mail import Message
from config import config as p


def send_reset_email(user):
    """
    Envía un correo electrónico al usuario con un enlace para restablecer su contraseña.
    Args:
        user: El usuario al que se enviará el correo electrónico.
    Returns:
        None
    """
    token = user.get_reset_token()  # Token para confirmar la identidad del usuario
    msg = Message()
    msg.subject = "Restablece tu contraseña"
    msg.sender = (
        p.MAIL_USERNAME
    )  # Tomamos la dirección de email de los datos del usuario en la base de datos
    msg.recipients = [user.correoElectronico]
    msg.html = render_template("auth/reset_email.html", user=user, token=token)
