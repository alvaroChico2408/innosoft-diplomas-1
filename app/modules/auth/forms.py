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

'''
class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    surname = StringField('Surname', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
'''

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

'''
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')
    
'''

class LoginForm(FlaskForm):

    username = StringField(
        "Username or Email Address", validators=[DataRequired(), Length(5, 150)]
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 20)])
    remember = BooleanField("Remember me", validators=[DataRequired()])
    submit = SubmitField("Continue")

