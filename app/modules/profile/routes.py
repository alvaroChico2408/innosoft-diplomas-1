from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required

from app.modules.profile import profile_bp
from app.modules.auth.services import AuthenticationService
from app.modules.profile.forms import UserProfileForm
from app.modules.profile.services import UserProfileService

from flask_login import current_user
from app.modules.profile.forms import ChangePasswordForm


@profile_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    auth_service = AuthenticationService()
    profile = auth_service.get_authenticated_user_profile()
    if not profile:
        return redirect(url_for("public.index"))

    # Mantener el campo de contraseña vacío al cargar el formulario
    form = UserProfileForm(
        name=profile.name,
        surname=profile.surname,
        email=profile.email
    )
    
    if request.method == "POST":
        service = UserProfileService()
        result, errors = service.update_profile(profile.id, form)
        return service.handle_service_response(
            result, errors, "profile.edit_profile", "Profile updated successfully", "profile/edit.html", form
        )

    return render_template("profile/edit.html", form=form, profile=profile)



@profile_bp.route("/profile/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        new_password = form.password.data
        confirm_password = form.confirm_password.data

        if new_password != confirm_password:
            form.confirm_password.errors.append("Passwords must match.")
            return render_template("profile/change_password.html", form=form)

        # Actualizamos la contraseña tanto en User como en UserProfile
        auth_service = AuthenticationService()
        result, error = auth_service.change_password(current_user.id, new_password)

        if error:
            form.password.errors.append(error)
            return render_template("profile/change_password.html", form=form)

        # Flash de mensaje de éxito
        flash("Password updated successfully", "success")
        return redirect(url_for("profile.edit_profile"))

    return render_template("profile/change_password.html", form=form)


