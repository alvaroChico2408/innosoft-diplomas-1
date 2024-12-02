from flask import render_template, redirect, url_for, request
from flask_login import current_user, logout_user
from app.modules.auth import auth_bp
from app.modules.auth.decorators import guest_required
from app.modules.auth.forms import LoginForm
from app.modules.auth.services import AuthenticationService
from app.modules.confirmemail.services import ConfirmemailService
from app.modules.profile.services import UserProfileService

authentication_service = AuthenticationService()
user_profile_service = UserProfileService()
confirmemail_service = ConfirmemailService()


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
