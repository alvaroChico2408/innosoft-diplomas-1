import os
import re
import typing as t

from http import HTTPStatus
from datetime import timedelta
from werkzeug.exceptions import InternalServerError
from werkzeug.utils import secure_filename


from flask import Blueprint, Response
from flask import abort, current_app, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user

import os
import pandas as pd
from flask import flash, redirect, url_for
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from werkzeug.utils import secure_filename
from .models import Diploma
from .extensions import database as db 



from flask import flash, redirect, url_for, render_template, request
from werkzeug.utils import secure_filename
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from accounts.models import Diploma
from accounts.forms import EnterExcelHours



from accounts.decorators import authentication_redirect, guest_user_exempt
from accounts.email_utils import (
    send_reset_password,
    send_reset_email,
)
from accounts.extensions import database as db
from accounts.models import User
from accounts.forms import (
    RegisterForm,
    LoginForm,
    ForgotPasswordForm,
    ResetPasswordForm,
    ChangePasswordForm,
    ChangeEmailForm,
    EditUserProfileForm,
    EnterExcelHours
)



"""
This accounts blueprint defines routes and templates related to user management
within our application.
"""
accounts = Blueprint("accounts", __name__, template_folder="templates")


@accounts.route("/login_as_guest", methods=["GET", "POST"])
@authentication_redirect
def login_guest_user() -> Response:
    """
    Log in as a guest user with limited access.

    :return: Redirects to the homepage on success or the login page on failure.
    """
    if request.method == "POST":
        # Fetch the predefined guest user instance by username.
        test_user = User.get_user_by_username(username="test_user")

        if test_user:
            # Log in the guest user with a session duration of (1 day) only.
            login_user(test_user, remember=True, duration=timedelta(days=1))

            flash("You are logged in as a Guest User.", "success")
            return redirect(url_for("accounts.index"))

        flash("Something went wront.", "error")
        return redirect(url_for("accounts.login"))

    # Return a 404 error if accessed via GET
    return abort(HTTPStatus.NOT_FOUND)


@accounts.route("/register", methods=["GET", "POST"])
@authentication_redirect
def register() -> Response:
    """
    Handling user registration.
    If the user is already authenticated, they are redirected to the index page.

    This view handles both GET and POST requests:
    - GET: Renders the registration form and template.
    - POST: Processes the registration form, creates a new user, and sends a confirmation email.

    :return: Renders the registration template on GET request
    or redirects to login after successful registration.
    """
    form = RegisterForm()

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
        return redirect(url_for("accounts.login"))

    return render_template("register.html", form=form)


@accounts.route("/login", methods=["GET", "POST"])
@authentication_redirect
def login() -> Response:
    """
    Handling user login functionality.
    If the user is already authenticated, they are redirected to the index page.

    This view handles both GET and POST requests:
    - GET: Renders the login form and template.
    - POST: Validates the form and authenticates the user.

    :return: Renders the login template on GET request or redirects based on the login status.
    """
    form = LoginForm()  # A form class for Login Account.

    if form.validate_on_submit():
        username = form.data.get("username", None)
        password = form.data.get("password", None)
        remember = form.data.get("remember", True)

        # Attempt to authenticate the user from the database.
        user = User.authenticate(username=username, password=password)

        if not user:
            flash("Invalid username or password. Please try again.", "error")
        else:
            if not user.is_active:
                # User account is not active, send confirmation email.
                user.send_confirmation()

                flash(
                    "Your account is not activate. We sent a confirmation link to your email",
                    "error",
                )
                return redirect(url_for("accounts.login"))

            # Log the user in and set the session to remember the user for (15 days).
            login_user(user, remember=remember, duration=timedelta(days=15))

            flash("You are logged in successfully.", "success")
            return redirect(url_for("accounts.index"))

        return redirect(url_for("accounts.login"))

    return render_template("login.html", form=form)


@accounts.route("/account/confirm", methods=["GET", "POST"])
def confirm_account() -> Response:
    """
    Handling account confirmation request via a token.
    If the token is valid and not expired, the user is activated.

    This view handles both GET and POST requests:
    - GET: Renders the account confirmation template.
    - POST: Activates the user account if the token is valid,
            logs the user in, and redirects to the index page.

    :return: Renders the confirmation template on GET request,
    redirects to login or index after POST.
    """
    token: str = request.args.get("token", None)

    # Verify the provided token and return token instance.
    auth_token = User.verify_token(
        token=token, salt=current_app.config["ACCOUNT_CONFIRM_SALT"]
    )

    if auth_token:
        # Retrieve the user instance associated with the token by providing user ID.
        user = User.get_user_by_id(auth_token.user_id, raise_exception=True)

        if request.method == "POST":
            try:
                # Activate the user's account and expire the token.
                user.active = True
                auth_token.expire = True

                # Commit changes to the database.
                db.session.commit()
            except Exception as e:
                # Handle database error that occur during the account activation.
                raise InternalServerError

            # Log the user in and set the session to remember the user for (15 days).
            login_user(user, remember=True, duration=timedelta(days=15))

            flash(
                f"Welcome {user.username}, You're registered successfully.", "success"
            )
            return redirect(url_for("accounts.index"))

        return render_template("confirm_account.html", token=token)

    # If the token is invalid, return a 404 error
    return abort(HTTPStatus.NOT_FOUND)


@accounts.route("/logout", methods=["GET", "POST"])
@login_required
def logout() -> Response:
    """
    Logs out the currently authenticated user
    and redirect them to the login page.

    :return: A redirect response to the login page with a success flash message.
    """
    # Log out the user and clear the session.
    logout_user()

    flash("You're logout successfully.", "success")
    return redirect(url_for("accounts.login"))


@accounts.route("/forgot/password", methods=["GET", "POST"])
@guest_user_exempt
def forgot_password() -> Response:
    """
    Handling forgot password requests by validating the provided email
    and sending a password reset link if the email is registered.

    This view handles both GET and POST requests:
    - GET: Renders the forgot password form and template.
    - POST: Validates the email and sends a reset link if the email exists in the system.

    :return: Renders the forgot password form on GET,
    redirects to login on success, or reloads the form on failure.
    """
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        email = form.data.get("email")

        # Attempt to find the user by email from the database.
        user = User.get_user_by_email(email=email)

        if user:
            # Send a reset password link to the user's email.
            send_reset_password(user)

            flash("A reset password link sent to your email. Please check.", "success")
            return redirect(url_for("accounts.login"))

        flash("Email address is not registered with us.", "error")
        return redirect(url_for("accounts.forgot_password"))

    return render_template("forgot_password.html", form=form)


@accounts.route("/password/reset", methods=["GET", "POST"])
def reset_password() -> Response:
    """
    Handling password reset requests.

    This function allows users to reset their password by validating a token
    and ensuring the new password meets security criteria.

    This view handles both GET and POST requests:
    - GET: Renders the reset password form and template, if the token is valid.
    - POST: Validates the form, checks password strength, and updates the user's password.

    :return: Renders the reset password form on GET,
    redirects to login on success, or reloads the form on failure.
    """
    token = request.args.get("token", None)

    # Verify the provided token and return token instance.
    auth_token = User.verify_token(
        token=token, salt=current_app.config["RESET_PASSWORD_SALT"]
    )

    if auth_token:
        form = ResetPasswordForm()  # A form class to Reset User's Password.

        if form.validate_on_submit():
            password = form.data.get("password")
            confirm_password = form.data.get("confirm_password")

            # Regex pattern to validate password strength.
            re_pattern = r"(?=^.{8,}$)(?=.*\d)(?=.*[!@#$%^&*]+)(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$"

            if not (password == confirm_password):
                flash("Your new password field's not match.", "error")
            elif not re.match(re_pattern, password):
                flash(
                    "Please choose strong password. It contains at least one alphabet, number, and one special character.",
                    "warning",
                )
            else:
                try:
                    # Retrieve the user by the ID from the token and update their password.
                    user = User.get_user_by_id(auth_token.user_id, raise_exception=True)
                    user.set_password(password)

                    # Mark the token as expired after the password is reset.
                    auth_token.expire = True

                    # Commit changes to the database.
                    db.session.commit()
                except Exception as e:
                    # Handle database error by raising an internal server error.
                    raise InternalServerError

                flash("Your password is changed successfully. Please login.", "success")
                return redirect(url_for("accounts.login"))

            return redirect(url_for("accounts.reset_password", token=token))

        return render_template("reset_password.html", form=form, token=token)

    # If the token is invalid, abort with a 404 Not Found status.
    return abort(HTTPStatus.NOT_FOUND)


@accounts.route("/change/password", methods=["GET", "POST"])
@login_required
@guest_user_exempt
def change_password() -> Response:
    """
    Handling user password change requests.

    This function allows authenticated users to change their password by
    verifying the old password and ensuring the new password meets security criteria.

    This view handles both GET and POST requests:
    - GET: Renders the change password form and template.
    - POST: Validates the form, checks old password correctness, ensures the new
      password meets security standards, and updates the user's password.

    :return: Renders the change password form on GET,
    redirects to index on success, or reloads the form on failure.
    """
    form = ChangePasswordForm()  # A form class to Change User's Password.

    if form.validate_on_submit():
        old_password = form.data.get("old_password")
        new_password = form.data.get("new_password")
        confirm_password = form.data.get("confirm_password")

        # Retrieve the fresh user instance from the database.
        user = User.get_user_by_id(current_user.id, raise_exception=True)

        # Regex pattern to validate password strength.
        re_pattern = (
            r"(?=^.{8,}$)(?=.*\d)(?=.*[!@#$%^&*]+)(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$"
        )

        if not user.check_password(old_password):
            flash("Your old password is incorrect.", "error")
        elif not (new_password == confirm_password):
            flash("Your new password field's not match.", "error")
        elif not re.match(re_pattern, new_password):
            flash(
                "Please choose strong password. It contains at least one alphabet, number, and one special character.",
                "warning",
            )
        else:
            try:
                # Update the user's password.
                user.set_password(new_password)

                # Commit changes to the database.
                db.session.commit()
            except Exception as e:
                # Handle database error by raising an internal server error.
                raise InternalServerError

            flash("Your password changed successfully.", "success")
            return redirect(url_for("accounts.index"))

        return redirect(url_for("accounts.change_password"))

    return render_template("change_password.html", form=form)


@accounts.route("/change/email", methods=["GET", "POST"])
@login_required
@guest_user_exempt
def change_email() -> Response:
    """
    Handling email change requests for the logged-in user.

    Methods:
        GET: Render the email change form and template.
        POST: Process the form submission to change the user's email.

    Returns:
        Response: The rendered change email template or a redirect after form submission.
    """
    form = ChangeEmailForm()  # A form class for Change Email Address.

    if form.validate_on_submit():
        email = form.data.get("email", None)

        # Retrieve the fresh user instance based on their ID.
        user = User.get_user_by_id(current_user.id, raise_exception=True)

        if email == user.email:
            flash("Email is already verified with your account.", "warning")
        elif User.query.filter(User.email == email, User.id != user.id).first():
            flash("Email address is already registered with us.", "warning")
        else:
            try:
                # Update the new email as the pending email change.
                user.change_email = email

                # Commit changes to the database.
                db.session.commit()
            except Exception as e:
                # Handle database error by raising an internal server error.
                raise InternalServerError

            # Send a reset email to the new email address.
            send_reset_email(user)

            flash(
                "A reset email link sent to your new email address. Please verify.",
                "success",
            )
            return redirect(url_for("accounts.index"))

        return redirect(url_for("accounts.change_email"))

    return render_template("change_email.html", form=form)


@accounts.route("/account/email/confirm", methods=["GET", "POST"])
def confirm_email() -> Response:
    """
    Handle email confirmation via a token sent to the user's new email address.

    Methods:
        GET: Render the email confirmation template with the token.
        POST: Confirm the email change by verifying the token.

    Returns:
        Response: The rendered confirm email template, or a redirect after confirmation.
    """
    token = request.args.get("token", None)

    # Verify the provided token and return token instance.
    auth_token = User.verify_token(
        token=token, salt=current_app.config["CHANGE_EMAIL_SALT"]
    )

    if auth_token:
        if request.method == "POST":
            # Retrieve the user by the ID from the token and update email details.
            user = User.get_user_by_id(auth_token.user_id, raise_exception=True)

            try:
                # Update new email address to user.
                user.email = user.change_email
                user.change_email = None

                # Mark the token as expired after the new email is set.
                auth_token.expire = True

                # Commit changes to the database.
                db.session.commit()
            except Exception as e:
                # Handle database error by raising an internal server error.
                raise InternalServerError

            flash("Your email address updated successfully.", "success")
            return redirect(url_for("accounts.index"))

        return render_template("confirm_email.html", token=token)

    # If the token is invalid, abort with a 404 Not Found status.
    return abort(HTTPStatus.NOT_FOUND)


@accounts.route("/")
@accounts.route("/home")
@login_required
def index() -> Response:
    """
    Render the homepage for authenticated users.

    :return: Renders the `index.html` template.
    """
    return render_template("index.html")


@accounts.route("/profile", methods=["GET", "POST"])
@login_required
@guest_user_exempt
def profile() -> Response:
    """
    Handling the user's profile page,
    allowing them to view and edit their profile information.

    Methods:
        GET: Render the profile template with the user's current information.
        POST: Update the user's profile with the submitted form data.

    Returns:
        Response: The rendered profile template or a redirect after form submission.
    """
    form = EditUserProfileForm()  # A form class to Edit User's Profile.

    # Retrieve the fresh user instance based on their ID.
    user = User.get_user_by_id(current_user.id, raise_exception=True)

    if form.validate_on_submit():
        username = form.data.get("username")
        first_name = form.data.get("first_name")
        last_name = form.data.get("last_name")
        profile_image = form.data.get("profile_image")
        about = form.data.get("about")

        # Check if the new username already exists and belongs to a different user.
        username_exist = User.query.filter(
            User.username == username, User.id != current_user.id
        ).first()

        if username_exist:
            flash("Username already exists. Choose another.", "error")
        else:
            try:
                # Update the user's profile details.
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.profile.bio = about

                # Handle profile image upload if provided.
                if profile_image and getattr(profile_image, "filename"):
                    user.profile.set_avator(profile_image)

                # Commit changes to the database.
                db.session.commit()
            except Exception as e:
                # Handle database error by raising an internal server error.
                raise InternalServerError

            flash("Your profile update successfully.", "success")
            return redirect(url_for("accounts.index"))

        return redirect(url_for("accounts.profile"))

    return render_template("profile.html", form=form)

'''
@accounts.route('/generate_diplomas', methods=['GET', 'POST'])
def generate_diplomas():
    form = EnterExcelHours()
    if form.validate_on_submit():
        file = form.hours_excel.data
        if file:
            procesar_excel(file)
    return render_template('generate_diplomas.html', form=form)
'''


@accounts.route("/credenciales")
@login_required
def credenciales() -> Response:
    return render_template("credenciales.html")


@accounts.route("/carteles")
@login_required
def carteles() -> Response:
    return render_template("carteles.html")



'''
def procesar_excel(file):
    # Ruta de subida de los archivos
    UPLOAD_FOLDER = os.path.join("uploads", "processed_excels")
    PDF_FOLDER = os.path.join("uploads", "pdf_diplomas")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(PDF_FOLDER, exist_ok=True)
    
    # Guardar el archivo subido
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    # Leer el archivo Excel
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        flash("Error al leer el archivo Excel. Asegúrate de que el archivo está en el formato correcto.", "warning")
        return redirect(url_for("accounts.generate_diplomas"))

    # Validar las columnas del archivo
    expected_columns = [
        "apellidos", "nombre", "uvus", "correo", "perfil", "participacion", "comite",
        "evidencia_aleatoria", "horas_de_evidencia_aleatoria", "eventos_asistidos",
        "horas_de_asistencia", "reuniones_asistidas", "horas_de_reuniones", "bono_de_horas",
        "evidencias_registradas", "horas_de_evidencias", "horas_en_total"
    ]
    if list(df.columns) != expected_columns:
        flash(f"Las columnas del archivo no coinciden con las esperadas: {expected_columns}", "warning")
        return redirect(url_for("accounts.generate_diplomas"))

    # Procesar cada fila del Excel
    errores = []
    for _, row in df.iterrows():
        try:
            diploma = Diploma(
                apellidos=validar_apellidos(row["apellidos"]),
                nombre=validar_nombre(row["nombre"]),
                uvus=validar_uvus(row["uvus"]),
                correo=validar_correo(row["correo"]),
                perfil=validar_perfil(row["perfil"]),
                participacion=validar_participacion(row["participacion"]),
                comite=validar_comite(row["comite"]),
                evidencia_aleatoria=row["evidencia_aleatoria"] or None,
                horas_de_evidencia_aleatoria=row["horas_de_evidencia_aleatoria"] or None,
                eventos_asistidos=row["eventos_asistidos"] or None,
                horas_de_asistencia=float(row["horas_de_asistencia"]),
                reuniones_asistidas=int(row["reuniones_asistidas"]),
                horas_de_reuniones=float(row["horas_de_reuniones"]),
                bono_de_horas=row["bono_de_horas"] or None,
                evidencias_registradas=int(row["evidencias_registradas"]),
                horas_de_evidencias=float(row["horas_de_evidencias"]),
                horas_en_total=float(row["horas_en_total"]),
            )
            db.session.add(diploma)
            generar_pdf(diploma, PDF_FOLDER)
        except ValueError as e:
            errores.append(f"Error en fila {row['uvus']}: {str(e)}")

    # Confirmar cambios o mostrar errores
    if errores:
        flash("Errores encontrados en el archivo:", "warning")
        for error in errores:
            flash(error, "warning")
    else:
        db.session.commit()
        flash("Diplomas procesados exitosamente y PDFs generados.", "success")

    return redirect(url_for("accounts.index"))

def generar_pdf(diploma, pdf_folder):
    pdf_path = os.path.join(pdf_folder, f"{diploma.uvus}_diploma.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.drawString(100, 800, f"Diploma de: {diploma.nombre} {diploma.apellidos}")
    c.drawString(100, 780, f"UVUS: {diploma.uvus}")
    c.drawString(100, 760, f"Correo: {diploma.correo}")
    # Añadir más datos según se requiera
    c.save()

import re

def validar_apellidos(apellidos):
    if not isinstance(apellidos, str) or len(apellidos.split()) not in [1, 2]:
        raise ValueError("Apellidos deben ser 1 o 2 palabras.")
    return apellidos

def validar_nombre(nombre):
    if not isinstance(nombre, str):
        raise ValueError("Nombre debe ser un string.")
    return nombre

def validar_uvus(uvus):
    if not isinstance(uvus, str):
        raise ValueError("UVUS debe ser un string.")
    return uvus

def validar_correo(correo):
    pattern = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(pattern, correo):
        raise ValueError("Correo no válido.")
    return correo

def validar_perfil(perfil):
    if not perfil.startswith("https://www.evidentia.cloud/2024/profiles/view/"):
        raise ValueError("Perfil debe comenzar con https://www.evidentia.cloud/2024/profiles/view/")
    return perfil

def validar_participacion(participacion):
    if participacion not in ["ORGANIZATION", "INTERMEDIATE", "ASSISTANCE"]:
        raise ValueError("Participación no válida.")
    return participacion

def validar_comite(comite):
    comites_validos = {"Comunicación", "Secretaría", "Finanzas", "Programa", "Logística", "Sostenibilidad", "Presidencia"}
    if not set(comite.split(", ")).issubset(comites_validos):
        raise ValueError("Comité no válido.")
    return comite

'''



# Carpeta única para guardar el archivo Excel y los PDFs generados
PDF_FOLDER = os.path.join("uploads", "pdf_diplomas")
os.makedirs(PDF_FOLDER, exist_ok=True)


@accounts.route('/generate_diplomas', methods=['GET', 'POST'])
def generate_diplomas():
    form = EnterExcelHours()
    if form.validate_on_submit():
        file = form.hours_excel.data
        if file:
            # Llamar a procesar_excel solo si se subió un archivo válido
            errores = procesar_excel(file)
            if errores:
                # Mostrar errores específicos en el archivo de Excel
                for error in errores:
                    flash(error, "warning")
            else:
                flash("Diplomas procesados exitosamente y PDFs generados.", "success")
            return redirect(url_for("accounts.index"))
    return render_template('generate_diplomas.html', form=form)


def procesar_excel(file):
    """
    Procesa el archivo Excel, valida el contenido, y genera PDFs si es exitoso.
    """
    # Guardar el archivo Excel en `PDF_FOLDER`
    filename = secure_filename(file.filename)
    file_path = os.path.join(PDF_FOLDER, filename)
    file.save(file_path)
    
    # Leer el archivo Excel
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        return [f"Error al leer el archivo Excel: {str(e)}"]

    # Validar las columnas del archivo
    expected_columns = [
        "apellidos", "nombre", "uvus", "correo", "perfil", "participacion", "comite",
        "evidencia_aleatoria", "horas_de_evidencia_aleatoria", "eventos_asistidos",
        "horas_de_asistencia", "reuniones_asistidas", "horas_de_reuniones", "bono_de_horas",
        "evidencias_registradas", "horas_de_evidencias", "horas_en_total"
    ]
    if list(df.columns) != expected_columns:
        return [f"Las columnas del archivo no coinciden con las esperadas: {expected_columns}"]

    # Procesar cada fila del Excel
    errores = []
    for _, row in df.iterrows():
        try:
            diploma = Diploma(
                apellidos=validar_apellidos(row["apellidos"]),
                nombre=validar_nombre(row["nombre"]),
                uvus=validar_uvus(row["uvus"]),
                correo=validar_correo(row["correo"]),
                perfil=validar_perfil(row["perfil"]),
                participacion=validar_participacion(row["participacion"]),
                comite=validar_comite(row["comite"]),
                evidencia_aleatoria=row["evidencia_aleatoria"] or None,
                horas_de_evidencia_aleatoria=row["horas_de_evidencia_aleatoria"] or None,
                eventos_asistidos=row["eventos_asistidos"] or None,
                horas_de_asistencia=float(row["horas_de_asistencia"]),
                reuniones_asistidas=int(row["reuniones_asistidas"]),
                horas_de_reuniones=float(row["horas_de_reuniones"]),
                bono_de_horas=row["bono_de_horas"] or None,
                evidencias_registradas=int(row["evidencias_registradas"]),
                horas_de_evidencias=float(row["horas_de_evidencias"]),
                horas_en_total=float(row["horas_en_total"]),
            )
            db.session.add(diploma)
            generar_pdf(diploma)  # Genera el PDF para cada diploma
        except ValueError as e:
            errores.append(f"Error en fila {row['uvus']}: {str(e)}")

    # Confirmar cambios si no hubo errores
    if not errores:
        db.session.commit()

    return errores


def generar_pdf(diploma):
    """
    Genera un PDF en blanco para cada diploma con los datos proporcionados.
    """
    pdf_path = os.path.join(PDF_FOLDER, f"{diploma.uvus}_diploma.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.drawString(100, 800, f"Diploma de: {diploma.nombre} {diploma.apellidos}")
    c.drawString(100, 780, f"UVUS: {diploma.uvus}")
    c.drawString(100, 760, f"Correo: {diploma.correo}")
    # Añadir más datos según se requiera
    c.save()



# Funciones de validación
def validar_apellidos(apellidos):
    if not isinstance(apellidos, str) or len(apellidos.split()) not in [1, 2]:
        raise ValueError("Apellidos deben ser 1 o 2 palabras.")
    return apellidos

def validar_nombre(nombre):
    if not isinstance(nombre, str):
        raise ValueError("Nombre debe ser un string.")
    return nombre

def validar_uvus(uvus):
    if not isinstance(uvus, str):
        raise ValueError("UVUS debe ser un string.")
    return uvus

def validar_correo(correo):
    pattern = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(pattern, correo):
        raise ValueError("Correo no válido.")
    return correo

def validar_perfil(perfil):
    if not perfil.startswith("https://www.evidentia.cloud/2024/profiles/view/"):
        raise ValueError("Perfil debe comenzar con https://www.evidentia.cloud/2024/profiles/view/")
    return perfil

def validar_participacion(participacion):
    if participacion not in ["ORGANIZATION", "INTERMEDIATE", "ASSISTANCE"]:
        raise ValueError("Participación no válida.")
    return participacion

def validar_comite(comite):
    comites_validos = {"Comunicación", "Secretaría", "Finanzas", "Programa", "Logística", "Sostenibilidad", "Presidencia"}
    if not set(comite.split(", ")).issubset(comites_validos):
        raise ValueError("Comité no válido.")
    return comite
