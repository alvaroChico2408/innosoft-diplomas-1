from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileSize

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
        ],
    )
    submit = SubmitField("Generate Diplomas")