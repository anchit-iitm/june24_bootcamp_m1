from flask_mail import Message

from app import celery_app
from celery_tasker import FlaskTask
from mailer import mail


@celery_app.task(base=FlaskTask)
def helloWorld():
    print('hi wolrd')
    return 'hello world'

@celery_app.task(base=FlaskTask)
def add():
    x = 2
    y = 3
    return x+y

@celery_app.task(base=FlaskTask)
def cate_query():
    from database.models import Category
    cate = Category.query.filter_by(id=1).first()
    if cate:
        return cate.name
    return 'not found'

@celery_app.task(base=FlaskTask)
def mail_test():
    email_id = 'test@example.com'
    email_subject = 'test mail to check'
    email_body = 'hi, /n this is an test email please ignore. /n/nregards, /nGrocery store'

    msg = Message(subject=email_subject, recipients=[email_id], body=email_body)
    mail.send(msg)
    return 'ok'

@celery_app.task(base=FlaskTask)
def ex_daily():
    from database.models import User
    users = User.get_all_users()
    for user in users:
        # from datetime import datetime, timedelta
        email_subject = 'test mail to check'
        email_body = "Kindly check the attachment /n/nregards, /nGrocery store"
        report = "<html><body>"
        report += "<h1>No of total logins</h1>" 
        report += f"<p>logins: {user.login_count}</p>"
        report += "</body></html>"

        msg = Message(subject=email_subject, recipients=[user.email], body=email_body, sender='anchit@a.com')
        msg.html = report
        mail.send(msg)
    return 'all the mails are out'
