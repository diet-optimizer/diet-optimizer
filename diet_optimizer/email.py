from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from __init__ import mail
import smtplib

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    #msg = Message(app.config['DIET_OPTIMIZER_MAIL_SUBJECT_PREFIX'] + ' ' + subject,sender=app.config['DIET_OPTIMIZER_MAIL_SENDER'], recipients=[to])
    msg = Message(subject,sender = 'diet.optimizer@gmail.com', recipients = [to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

