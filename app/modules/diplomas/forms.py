from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

class UploadExcelForm(FlaskForm):
    hours_excel = FileField('Sube tu archivo Excel', validators=[DataRequired()])
    submit = SubmitField('Generar Diplomas')
