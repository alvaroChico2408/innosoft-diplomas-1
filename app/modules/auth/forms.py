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
from app.modules.auth.validators import  StrongUsername, StrongNames, StrongPassword, Unique

from flask_wtf.form import FlaskForm
from flask_wtf.file import FileAllowed, FileSize
from app.modules.auth.models import User


class SignupForm(FlaskForm):

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
    submit = SubmitField("Continue")



class LoginForm(FlaskForm):

    username = StringField(
        "Username", validators=[DataRequired(), Length(1, 30)]
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 20)])
    remember = BooleanField("Remember me", validators=[DataRequired()])
    submit = SubmitField("Continue")

