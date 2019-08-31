from threading import Thread
from flask import current_app, render_template
from flask_mail import Message

from app.libs.extentions import mail


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message('[BrBlog]' + ' ' + subject,
                  sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.html = render_template(template, **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr