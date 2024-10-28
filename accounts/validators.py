import re

from wtforms import ValidationError


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


class ExcelValidator:
    """Validator for Excel file structure and data."""
    expected_columns = [
        "Apellidos", "Nombre", "Uvus", "Correo", "Perfil", "Participación", "Comité",
        "Evidencia aleatoria", "Horas de evidencia aleatoria", "Eventos asistidos",
        "Horas de asistencia", "Reuniones asistidas", "Horas de reuniones", "Bono de horas",
        "Evidencias registradas", "Horas de evidencias", "Horas en total"
    ]

    @classmethod
    def validate_structure(cls, df):
        """Check if the Excel file has the expected columns."""
        if list(df.columns) != cls.expected_columns:
            raise ValidationError(f"Las columnas del archivo no coinciden con las esperadas: {cls.expected_columns}")

    @staticmethod
    def validate_row_data(row, index):
        """Validate each field in a row."""
        errors = []
        if not isinstance(row["Apellidos"], str) or len(row["Apellidos"].split()) not in [1, 2]:
            errors.append(f"Error en fila {index + 1}: Apellidos deben ser 1 o 2 palabras.")
        if not isinstance(row["Nombre"], str):
            errors.append(f"Error en fila {index + 1}: Nombre debe ser un string.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", row["Correo"]):
            errors.append(f"Error en fila {index + 1}: Correo no tiene un formato válido.")
        if not row["Perfil"].startswith("https://www.evidentia.cloud/2024/profiles/view/"):
            errors.append(f"Error en fila {index + 1}: Perfil debe comenzar con https://www.evidentia.cloud/2024/profiles/view/")
        if row["Participación"] not in ["ORGANIZATION", "INTERMEDIATE", "ASSISTANCE"]:
            errors.append(f"Error en fila {index + 1}: Participación no válida.")
        
        comites_validos = {"Comunicación", "Secretaría", "Finanzas", "Programa", "Logística", "Sostenibilidad", "Presidencia"}
        if not set(row["Comité"].split(", ")).issubset(comites_validos):
            errors.append(f"Error en fila {index + 1}: Comité no válido.")
        
        if errors:
            raise ValidationError(" ".join(errors))