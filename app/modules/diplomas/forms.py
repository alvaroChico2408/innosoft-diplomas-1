from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileSize
from app.modules.diplomas.models import DiplomaTemplate


class UploadExcelForm(FlaskForm):
    hours_excel = FileField(
        "Excel to generate diplomas",
        validators=[
            DataRequired(message="You didn't introduce any file."),
            FileAllowed(["xlsx"], "Please upload an Excel file (.xlsx) only."),
            FileSize(
                max_size=20 * 1024 * 1024,  # 500 MB
                message="File size should not exceed 500 MB.",
            )
        ]
    )
    template = SelectField("Select Template", choices=[], validators=[DataRequired()])
    submit = SubmitField("Generate Diplomas")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar las plantillas desde la base de datos
        self.template.choices = [(t.id, t.filename) for t in DiplomaTemplate.query.all()]

class UploadTemplateForm(FlaskForm):
    pdf_file = FileField('Plantilla PDF', validators=[
        DataRequired(),
        FileAllowed(['pdf'], 'Solo se permiten archivos PDF')
    ])
    custom_text = StringField('Texto personalizado', validators=[DataRequired()])
    submit = SubmitField('Subir plantilla')