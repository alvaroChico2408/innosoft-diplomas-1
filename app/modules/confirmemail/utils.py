
from app.modules.auth.models import User 
from flask import current_app, render_template, url_for
from app.modules.auth.utils import get_full_url  
from app.modules.mail.services import send_mail

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