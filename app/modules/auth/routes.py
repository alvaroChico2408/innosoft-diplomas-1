from flask import flash, render_template, redirect, url_for, request, Response
from flask_login import current_user, logout_user
from pymysql import IntegrityError

from app.modules.auth import auth_bp
from app.modules.auth.decorators import guest_required, authentication_redirect
from app.modules.auth.forms import SignupForm, LoginForm
from app.modules.auth.services import AuthenticationService
from app.modules.confirmemail.services import ConfirmemailService
from app.modules.profile.services import UserProfileService
from app.modules.auth.models import User

from app import db

authentication_service = AuthenticationService()
user_profile_service = UserProfileService()
confirmemail_service = ConfirmemailService()

'''
@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = SignupForm()
    if form.validate_on_submit():

        email = form.email.data
        if not authentication_service.is_email_available(email):
            flash(f'Email {email} is already in use', 'danger')
            return render_template("auth/signup_form.html", form=form)

        try:
            # We try to create the user
            user = authentication_service.create_with_profile(**form.data)
            confirmemail_service.send_confirmation_email(user.email)
        except IntegrityError as exc:
            db.session.rollback()
            if 'Duplicate entry' in str(exc):
                flash(f'Email {email} is already in use', 'danger')
            else:
                flash(f'Error creating user: {exc}', 'danger')
            return render_template("auth/signup_form.html", form=form)

        return redirect(url_for("public.index"))

    return render_template("auth/signup_form.html", form=form)
'''
@auth_bp.route("/signup", methods=["GET", "POST"])
@authentication_redirect
def show_signup_form() -> Response:
    """
    Handling user registration.
    If the user is already authenticated, they are redirected to the index page.

    This view handles both GET and POST requests:
    - GET: Renders the registration form and template.
    - POST: Processes the registration form, creates a new user, and sends a confirmation email.

    :return: Renders the registration template on GET request
    or redirects to login after successful registration.

    """
    
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = SignupForm()
    print(form.data)
    print(form.errors)
    print("----")
    print(form.validate_on_submit())
    if form.validate_on_submit():
        username = form.data.get("username")
        first_name = form.data.get("first_name")
        last_name = form.data.get("last_name")
        email = form.data.get("email")
        password = form.data.get("password")
        # Attempt to create a new user and save to the database.
        user = User.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )

        # Sends account confirmation mail to the user.
        user.send_confirmation()

        flash(
            "A confirmation link sent to your email. Please verify your account.",
            "success",
        )
        return redirect(url_for("auth/login_form.html"))

    return render_template("auth/signup_form.html", form=form)



@auth_bp.route('/login', methods=['GET', 'POST'])
@guest_required
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():

        if authentication_service.login(form.email.data, form.password.data):
            return redirect(url_for('public.index'))

        return render_template("auth/login_form.html", form=form, error='Invalid credentials')

    return render_template('auth/login_form.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))
