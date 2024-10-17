import os
import typing as t

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from werkzeug.exceptions import ServiceUnavailable

from flask import current_app, render_template, url_for
from accounts.models import User
from accounts.utils import get_full_url


def send_mail(subject: t.AnyStr, recipients: t.List[str], body: t.Text):
    """
    Sends an email using SendGrid.

    :param subject: The subject of the email.
    :param recipients: A list of recipient email addresses.
    :param body: The body content of the email.

    :raises ValueError: If the `SENDGRID_API_KEY` environment variable is not set.
    :raises ServiceUnavailable: If the SendGrid service is unavailable.
    """
    sender: str = os.environ.get("SENDGRID_SENDER_EMAIL", None)
    api_key: str = os.environ.get("SENDGRID_API_KEY", None)

    if not sender:
        raise ValueError("`SENDGRID_SENDER_EMAIL` environment variable is not set")
    
    if not api_key:
        raise ValueError("`SENDGRID_API_KEY` environment variable is not set")

    message = Mail(
        from_email=sender,
        to_emails=recipients,
        subject=subject,
        html_content=body  # SendGrid can handle both HTML and text content
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(f"Email sent with status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise ServiceUnavailable(
            description=(
                "The SendGrid mail service is currently not available. "
                "Please try later or contact the developers team."
            )
        )


def send_confirmation_mail(user: User = None):
    subject: str = "Verify Your Account"

    token: str = user.generate_token(salt=current_app.config["ACCOUNT_CONFIRM_SALT"])

    verification_link: str = get_full_url(
        url_for("accounts.confirm_account", token=token)
    )

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

    confirmation_link: str = get_full_url(
        url_for("accounts.confirm_email", token=token)
    )

    context = render_template(
        "emails/reset_email.txt",
        username=user.username,
        confirmation_link=confirmation_link,
    )

    send_mail(subject=subject, recipients=[user.change_email], body=context)
