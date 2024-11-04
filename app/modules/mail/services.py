
import os

from flask_mail import Mail, Message
from app.modules.mail.repositories import MailRepository
from core.services.BaseService import BaseService


class MailService(BaseService):

    def __init__(self):
        super().__init__(MailRepository())
        self.mail = None
        self.sender = None

    def init_app(self, app):
        app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.office365.com')
        app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', '587'))
        app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
        app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False') == 'True'
        app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'diplomasinnosoft2024@gmail.com')
        app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'diplomasInnosoft2024')
        app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

        self.mail = Mail(app)
        self.sender = app.config['MAIL_USERNAME']

    def send_email(self, subject, recipients, body, html_body=None):
        msg = Message(subject, sender=self.sender, recipients=recipients)
        msg.body = body
        if html_body:
            msg.html = html_body

        self.mail.send(msg)
'''
import os
import typing as t
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from werkzeug.exceptions import ServiceUnavailable

def send_mail(subject: t.AnyStr, recipients: t.List[str], body: t.Text):
    """
    Sends an email using Gmail SMTP.

    :param subject: The subject of the email.
    :param recipients: A list of recipient email addresses.
    :param body: The body content of the email.

    :raises ValueError: If required environment variables are not set.
    :raises ServiceUnavailable: If the SMTP service is unavailable.
    """
    sender: str = os.environ.get("SMTP_USERNAME", None)
    password: str = os.environ.get("SMTP_PASSWORD", None)

    if not sender or not password:
        raise ValueError("`SMTP_USERNAME` or `SMTP_PASSWORD` environment variable is not set")

    # Set up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender, password)
            server.sendmail(sender, recipients, message.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise ServiceUnavailable(
            description="The Gmail SMTP service is currently not available. "
                        "Please try later or contact the developers team."
        )

'''