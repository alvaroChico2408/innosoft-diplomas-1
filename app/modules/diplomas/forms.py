from flask_wtf import FlaskForm
from wtforms import SubmitField


class DiplomasForm(FlaskForm):
    submit = SubmitField('Save diplomas')
