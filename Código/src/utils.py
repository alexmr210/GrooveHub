from flask import render_template
from flask_mail import Message
from config import config as p
import config
from flask_mail import Mail


def send_reset_email(user):
    """
    Envía un correo electrónico al usuario con un enlace para restablecer su contraseña.
    Args:
        user: El usuario al que se enviará el correo electrónico.
    Returns:
        None
    """
    mail = Mail(config.app)
    token = user.get_reset_token()  # Token para confirmar la identidad del usuario
    msg = Message()
    msg.subject = "Restablece tu contraseña"
    msg.sender = (
        p.MAIL_TECH
    )  # Tomamos la dirección de email de los datos del usuario en la base de datos
    msg.recipients = [user.email]
    msg.html = render_template("auth/reset_email.html", user=user, token=token)
    mail.send(msg)


def send_modification_email(diskData):
    mail = Mail(config.app)
    msg = Message()
    msg.subject = "Solicitud de modificación de un disco"
    msg.sender = p.MAIL_TECH
    msg.recipients = [p.MAIL_TECH]
    msg.html = render_template("collection/modify_mail.html", diskData=diskData)
    mail.send(msg)


def not_empty(input_list):
    for item in input_list:
        if item != "":
            return True
    return False
