from flask import flash, render_template, redirect, url_for, request, Response, abort
from flask_login import login_user
from flask_login import current_user, logout_user
from pymysql import IntegrityError

from app.modules.auth import auth_bp
from app.modules.auth.decorators import guest_required, authentication_redirect
from app.modules.auth.forms import SignupForm, LoginForm
from app.modules.auth.services import AuthenticationService
from app.modules.confirmemail.services import ConfirmemailService
from app.modules.profile.services import UserProfileService
from app.modules.auth.models import User
from datetime import timedelta
from http import HTTPStatus



from app import db

authentication_service = AuthenticationService()
user_profile_service = UserProfileService()
confirmemail_service = ConfirmemailService()

@auth_bp.route("/signup", methods=["GET", "POST"])
@authentication_redirect
def show_signup_form() -> Response:
    """
        Registro de usuarios, borrar cuando vayamos a entregar
    """
    
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    
    form = SignupForm()
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
        return redirect(url_for("auth.login"))
    return render_template("auth/signup_form.html", form=form)


'''
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
'''

@auth_bp.route("/login", methods=["GET", "POST"])
@guest_required
def login() -> Response:
    """
    Log in as a guest user with limited access.

    :return: Redirects to the homepage on success or the login page on failure.
    """
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = LoginForm()
    print("hola1")

    if request.method == 'POST': #and form.validate_on_submit():
        
        test_user = User.get_user_by_username(username=form.username.data)

        if test_user:
            if authentication_service.login(form.username.data, form.password.data):
                print(current_user.is_authenticated)
                print("hola3")
                return redirect(url_for('public.index'))
        else:
            return render_template("auth/login_form.html", form=form, error='Invalid credentials')

    return render_template('auth/login_form.html', form=form)
        

        

    # Return a 404 error if accessed via GET
    return abort(HTTPStatus.NOT_FOUND)
    


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))
