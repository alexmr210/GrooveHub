from threading import Thread
from flask import render_template
from flask_mail import Message
from app import mail, app
from config import config as p

def send_email_thread(msg):
    with app.app_context():
        mail.send(msg)

def send_mail():
    msg = Message()
    msg.subject = "Email Subject"
    msg.recipients = ['alejandro3martin@gmail.com']
    msg.sender = p.MAIL_USERNAME
    msg.body = 'Email body'
    Thread(target=send_email_thread, args=(msg)).start()

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message()
    msg.subject = "Restablece tu contraseña"
    msg.sender = p.MAIL_USERNAME
    msg.recipients = [user.correoElectronico]
    msg.html = render_template('auth/reset_email.html',
                                user=user, 
                                token=token)
    mail.send(msg)