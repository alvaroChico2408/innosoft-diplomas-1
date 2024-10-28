import re

from wtforms import ValidationError
import pandas as pd



class Unique(object):
    """
    Validator that checks if a field value is unique in the database.
    """

    def __init__(self, instance=None, field=None, message=None):
        self.instance = instance
        self.field = field
        self.message = message

    def __call__(self, form, field):
        if self.instance.query.filter(self.field == field.data).first():
            if not self.message:
                self.message = "{} already exists.".format(field.name)
            raise ValidationError(self.message)



class StrongNames(object):
    """
    Validator that checks if a field contains only alphabetic characters.
    """

    def __init__(self, message=None):
        self.message = message
        if not self.message:
            self.message = "Field contains only alphabet."

    def __call__(self, form, field):
        if not re.match("^[a-zA-Z]+$", field.data):
            raise ValidationError(self.message)



class StrongUsername(object):
    """
    Validator that checks if a username contains only allowed characters.

    Allowed characters: A-Z, a-z, 0-9, underscore (_), hyphen (-), and period (.).
    """

    def __init__(self, message=None):
        self.message = message
        if not self.message:
            self.message = "Username contain only (A-Za-z0-9_-.) characters."

    def __call__(self, form, field):
        username = field.data
        if not re.match("^[a-zA-Z0-9_.-]+$", username):
            raise ValidationError(self.message)



class StrongPassword(object):
    """
    Validator that checks if a password is strong.

    A strong password must contain at least 8 characters, one uppercase letter,
    one lowercase letter, one digit, and one special character from (!@#$%^&*).
    """

    def __init__(self, message=None):
        self.message = message
        if not self.message:
            self.message = "Please choose a strong password."

    def __call__(self, form, field):
        password = field.data
        if not re.match(
            r"(?=^.{8,}$)(?=.*\d)(?=.*[!@#$%^&*]+)(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$",
            password,
        ):
            raise ValidationError(self.message)



# A PARTIR DE AQUI HAY QUE SACAR LA VALIDACIÓN DEL EXCEL (leerlo y comprobar los campos)
'''
def _procesar_excel(file):
    UPLOAD_FOLDER = os.path.join("uploads", "processed_excels")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Eliminar archivos antiguos en la carpeta
    for existing_file in os.listdir(UPLOAD_FOLDER):
        if existing_file.endswith('.xlsx') or existing_file.endswith('.xls'):
            os.remove(os.path.join(UPLOAD_FOLDER, existing_file))

    # Guardar el archivo subido
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Leer y validar el archivo Excel
    try:
        df = pd.read_excel(file_path)
        ExcelValidator.validate_structure(df)
        for index, row in df.iterrows():
            ExcelValidator.validate_row_data(row, index)
        return df
    except ValidationError as e:
        flash(str(e), "warning")
        return None
    except Exception:
        flash("Error al leer el archivo. Asegúrate de que esté en el formato correcto (.xlsx).", "warning")
        return None
'''
'''
class ExcelValidator(object):
    """
    Main validator that orchestrates all individual row validations
    and structure validation for the Excel file.
    """

    def __init__(self, message=None):
        self.message = message or "The Excel file is not valid. Please check the structure and data."
        self.structure_validator = ColumnStructureValidator()
        self.email_validator = EmailValidator()
        self.profile_validator = ProfileValidator()
        self.participation_validator = ParticipationValidator()
        self.committee_validator = CommitteeValidator()

    def __call__(self, form, field):
        try:
            # Interpretar el contenido del campo como un DataFrame
            file = field.data
            df = pd.read_excel(file)
            
            # Validar la estructura de columnas
            self.structure_validator(df)

            # Validar los datos de cada fila
            for index, row in df.iterrows():
                self.email_validator(row, index)
                self.profile_validator(row, index)
                self.participation_validator(row, index)
                self.committee_validator(row, index)
        except ValidationError as e:
            raise ValidationError(f"Error in row {index + 1}: {str(e)}")
        except Exception:
            raise ValidationError("Error reading the Excel file. Ensure it is a .xlsx file with the correct format.")

class ColumnStructureValidator(object):
    """Validator that checks if an Excel file has the expected column structure."""

    expected_columns = [
        "Apellidos", "Nombre", "Uvus", "Correo", "Perfil", "Participación", "Comité",
        "Evidencia aleatoria", "Horas de evidencia aleatoria", "Eventos asistidos",
        "Horas de asistencia", "Reuniones asistidas", "Horas de reuniones", "Bono de horas",
        "Evidencias registradas", "Horas de evidencias", "Horas en total"
    ]

    def __init__(self, message=None):
        self.message = message or f"The columns of the file do not match the expected ones: {self.expected_columns}"

    def __call__(self, df):
        if list(df.columns) != self.expected_columns:
            raise ValidationError(self.message)


class EmailValidator(object):
    """Validator for validating email format to match alum.us.es or us.es patterns."""

    def __init__(self, message=None):
        self.message = message or "Email must end in '@alum.us.es' or '@us.es'."

    def __call__(self, row, index):
        # pattern to match emails ending with '@alum.us.es' or '@us.es'
        if not re.match(r"^[a-zA-Z0-9._%+-]+@(alum\.)?us\.es$", row["Correo"]):
            raise ValidationError(f"Error in row {index + 1}: {self.message}")


class ProfileValidator(object):
    """Validator for checking the profile URL format."""

    def __init__(self, message=None):
        self.message = message or "Profile URL must start with https://www.evidentia.cloud/2024/profiles/view/"

    def __call__(self, row, index):
        if not row["Perfil"].startswith("https://www.evidentia.cloud/2024/profiles/view/"):
            raise ValidationError(f"Error in row {index + 1}: {self.message}")


class ParticipationValidator(object):
    """Validator for checking participation type."""

    def __init__(self, message=None):
        self.message = message or "Participation type is invalid."

    def __call__(self, row, index):
        if row["Participación"] not in ["ORGANIZATION", "INTERMEDIATE", "ASSISTANCE"]:
            raise ValidationError(f"Error in row {index + 1}: {self.message}")


class CommitteeValidator(object):
    """Validator for checking valid committee names."""

    valid_committees = {"Presidencia", "Secretaría", "Programa", "Igualdad", "Sostenibilidad", "Finanzas", "Logística", "Comunicación"}

    def __init__(self, message=None):
        self.message = message or "Invalid committee name."

    def __call__(self, row, index):
        committees = row["Comité"].split(" | ") if row["Comité"] else []
        
        # Check if all committees in the cell are valid or if it's blank
        if not set(committees).issubset(self.valid_committees):
            raise ValidationError(f"Error in row {index + 1}: {self.message}")
'''