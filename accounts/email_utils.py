import os
import typing as t
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug.exceptions import ServiceUnavailable

from flask import current_app, render_template, url_for
from accounts.models import User
from accounts.utils import get_full_url


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


def send_confirmation_mail(user: User = None):
    subject: str = "Verify Your Account"
    token: str = user.generate_token(salt=current_app.config["ACCOUNT_CONFIRM_SALT"])
    verification_link: str = get_full_url(url_for("accounts.confirm_account", token=token))

    context = render_template(
        "emails/verify_account.txt",
        username=user.username,
        verification_link=verification_link,
    )

    send_mail(subject=subject, recipients=[user.email], body=context)


def send_reset_password(user: User = None):
    subject: str = "Reset Your Password"
    token: str = user.generate_token(salt=current_app.config["RESET_PASSWORD_SALT"])
    reset_link: str = get_full_url(url_for("accounts.reset_password", token=token))

    context = render_template(
        "emails/reset_password.txt", username=user.username, reset_link=reset_link
    )

    send_mail(subject=subject, recipients=[user.email], body=context)


def send_reset_email(user: User = None):
    subject: str = "Confirm Your Email Address"
    token: str = user.generate_token(salt=current_app.config["CHANGE_EMAIL_SALT"])
    confirmation_link: str = get_full_url(url_for("accounts.confirm_email", token=token))

    context = render_template(
        "emails/reset_email.txt",
        username=user.username,
        confirmation_link=confirmation_link,
    )

    send_mail(subject=subject, recipients=[user.change_email], body=context)
