from wtforms.fields import (
    StringField,
    PasswordField,
    EmailField,
    BooleanField,
    SubmitField,
    FileField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Email

from flask_wtf.form import FlaskForm
from flask_wtf.file import FileAllowed, FileSize

from accounts.models import User
from accounts.validators import Unique, StrongNames, StrongUsername, StrongPassword
 

class RegisterForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(1, 30),
            StrongUsername(),
            Unique(
                User, User.username, message="Username already exists choose another."
            ),
        ],
    )
    first_name = StringField(
        "First Name", validators=[DataRequired(), Length(3, 20), StrongNames()]
    )
    last_name = StringField(
        "Last Name", validators=[DataRequired(), Length(3, 20), StrongNames()]
    )
    email = EmailField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(),
            Length(8, 150),
            Unique(User, User.email, message="User already registered with us."),
        ],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(8, 20), StrongPassword()]
    )
    remember = BooleanField(
        "I agree & accept all terms of services. ", validators=[DataRequired()]
    )
    submit = SubmitField("Continue")


class LoginForm(FlaskForm):

    username = StringField(
        "Username or Email Address", validators=[DataRequired(), Length(5, 150)]
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 20)])
    # recaptcha = RecaptchaField()
    remember = BooleanField("Remember me", validators=[DataRequired()])
    submit = SubmitField("Continue")


class ForgotPasswordForm(FlaskForm):

    email = EmailField(
        "Email Address", validators=[DataRequired(), Length(8, 150), Email()]
    )
    remember = BooleanField(
        "I agree & accept all terms of services.", validators=[DataRequired()]
    )
    submit = SubmitField("Send Reset Link")


class ResetPasswordForm(FlaskForm):

    password = PasswordField(
        "Password", validators=[DataRequired(), Length(8, 20), StrongPassword()]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), Length(8, 20), StrongPassword()]
    )
    remember = BooleanField("Remember me", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ChangePasswordForm(FlaskForm):

    old_password = PasswordField(
        "Old Password", validators=[DataRequired(), Length(8, 20)]
    )
    new_password = PasswordField(
        "New Password", validators=[DataRequired(), Length(8, 20)]
    )
    confirm_password = PasswordField(
        "Confirm New Password", validators=[DataRequired(), Length(8, 20)]
    )
    remember = BooleanField("Remember me", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ChangeEmailForm(FlaskForm):

    email = EmailField(
        "Email Address", validators=[DataRequired(), Length(8, 150), Email()]
    )
    remember = BooleanField(
        "I agree & accept all terms of services.", validators=[DataRequired()]
    )
    submit = SubmitField("Send Confirmation Mail")


class EditUserProfileForm(FlaskForm):

    username = StringField(
        "Username", validators=[DataRequired(), Length(1, 30), StrongUsername()]
    )
    first_name = StringField(
        "First Name", validators=[DataRequired(), Length(3, 25), StrongNames()]
    )
    last_name = StringField(
        "Last Name", validators=[DataRequired(), Length(3, 25), StrongNames()]
    )
    profile_image = FileField(
        "Profile Image",
        validators=[
            FileAllowed(["jpg", "jpeg", "png", "svg"], "Please upload images only."),
            FileSize(
                max_size=1000000,
                message="Profile image size should not greater than 1MB.",
            ),
        ],
    )
    about = TextAreaField("About")
    submit = SubmitField("Save Profile")
    


from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize
from wtforms import FileField, SubmitField, ValidationError
import pandas as pd
import io
import re
from .validators import ExcelValidator

class EnterExcelHours(FlaskForm):
    hours_excel = FileField(
        "Excel to generate diplomas",
        validators=[
            FileAllowed(["xlsx"], "Please upload an Excel file (.xlsx) only."),
            FileSize(
                max_size=500 * 1024 * 1024,  # 500 MB
                message="File size should not exceed 500 MB.",
            ),
        ],
    )
    submit = SubmitField("Generate Diplomas")

def validate_hours_excel(self, field):
        if field.data:
            try:
                # Cargar el archivo y leer los datos en un DataFrame
                file_stream = io.BytesIO(field.data.read())
                df = pd.read_excel(file_stream)

                # Validar si el archivo está vacío
                if df.empty:
                    raise ValidationError("El archivo Excel está vacío. Por favor, carga un archivo con datos.")
                
                # Validar la estructura del archivo
                ExcelValidator.validate_structure(df)
                
                # Validar cada fila en el DataFrame
                for index, row in df.iterrows():
                    ExcelValidator.validate_row_data(row, index)

            except ValidationError as e:
                raise e  # Re-lanzar el ValidationError para mostrarlo en la pantalla
            except Exception:
                raise ValidationError("Error al leer el archivo. Asegúrate de que el archivo esté en el formato correcto (.xlsx).")
            finally:
                field.data.seek(0)  # Reiniciar el puntero del archivo