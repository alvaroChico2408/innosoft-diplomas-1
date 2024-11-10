import os
import re
import random
import string
import shutil
import typing as t
import io
from datetime import datetime, timedelta

import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

from sqlalchemy import Index, event, or_
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Mapper, validates
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.exc import IntegrityError
from wtforms import ValidationError

from werkzeug.exceptions import InternalServerError, HTTPException
from werkzeug.security import check_password_hash, generate_password_hash

from flask import url_for, current_app
from flask_login.mixins import UserMixin

from accounts.extensions import database as db
from accounts.utils import (
    get_unique_filename,
    remove_existing_file,
    unique_security_token,
    get_unique_id,
)



class BaseModel(db.Model):
    """
    A Base Model class for other models.
    """

    __abstract__ = True

    id = db.Column(
        db.String(38),
        primary_key=True,
        default=get_unique_id,
        nullable=False,
        unique=True,
    )

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(BaseModel, UserMixin):
    """
    A Base User model class.
    """

    __tablename__ = "user"

    username = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    active = db.Column(db.Boolean, default=False, nullable=False, server_default="0")
    change_email = db.Column(db.String(120), default="")

    @classmethod
    def authenticate(
        cls, username: t.AnyStr = None, password: t.AnyStr = None
    ) -> t.Optional["User"]:
        """
        Authenticates a user based on their username or email and password.

        :param username: The username or email of the user attempting to authenticate.
        :param password: The password of the user attempting to authenticate.

        :return: The authenticated user object if credentials are correct, otherwise None.
        """
        user = cls.query.filter(
            or_(
                cls.username == username,
                cls.email == username,
            )
        ).first()

        if user and user.check_password(password):
            return user

        return None

    @classmethod
    def create(cls, **kwargs):
        """
        Create a new user instance, set the password,
        and save it to the database.

        :return: The newly created user instance.

        :raises InternalServerError: If there is an error while creating or saving the user.
        """
        password = kwargs.get("password")

        try:
            user = cls(**kwargs)
            user.set_password(password)
            user.save()
        except Exception as e:
            # Handle database error by raising an internal server error.
            raise InternalServerError

        return user

    @classmethod
    def get_user_by_id(cls, user_id: t.AnyStr, raise_exception: bool = False):
        """
        Retrieves a user instance from the database
        based on their User ID.

        :param user_id: The ID of the user to retrieve instance.
        """
        if raise_exception:
            return cls.query.get_or_404(user_id)

        return cls.query.get(user_id)

    @classmethod
    def get_user_by_username(cls, username: t.AnyStr):
        """
        Retrieves a user instance from the database
        based on their username.

        :param username: The username of the user to retrieve.
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email: t.AnyStr):
        """
        Retrieves a user instance from the database
        based on their email address.

        :param email: The email address of the user to retrieve.
        """
        return cls.query.filter_by(email=email).first()

    def set_password(self, password: t.AnyStr):
        """
        Sets the password for the user after hashing it.

        :param password: The plain-text password to hash and set.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password: t.AnyStr) -> bool:
        """
        Checks if the provided password matches the hashed password.

        :param password: The plain-text password to check.
        """
        return check_password_hash(self.password, password)

    def generate_token(self, salt: str) -> t.AnyStr:
        """
        Generates a new security token for the user.

        :return: The newly created security token.
        """
        instance = UserSecurityToken.create_new(salt=salt, user_id=self.id)
        return instance.token

    @staticmethod
    def verify_token(
        token: t.AnyStr, salt: str, raise_exception: bool = True
    ) -> t.Union[t.Optional["UserSecurityToken"], HTTPException, None]:
        """
        Verifies whether a security token is valid and not expired.

        :param token: The security token to verify.
        :param raise_exception: If True, raises a 404 error if the token is not found. Defaults to True.

        :return: `True` if the token exists and is not expired, `False` otherwise.
        """
        instance = UserSecurityToken.query.filter_by(token=token, salt=salt)

        if raise_exception:
            token = instance.first_or_404()
        else:
            token = instance.first()

        if token and not token.is_expired:
            return token

        return None

    def send_confirmation(self):
        """
        Sends user's account confirmation email.
        """
        from accounts.email_utils import send_confirmation_mail

        send_confirmation_mail(self)

    @property
    def profile(self):
        """
        Retrieves the user's profile instance from the database.

        :return: The user's profile object, or None if no instance is found.
        """
        profile = Profile.query.filter_by(user_id=self.id).first()
        return profile

    @property
    def is_active(self) -> bool:
        """
        Checks if the user's account is active.

        :return: `True` if the user account is active, otherwise `False`.
        """
        return self.active

    def __repr__(self):
        return "<User '{}'>".format(self.username)


class Profile(BaseModel):
    """
    A User profile model class.
    """

    __tablename__ = "user_profile"

    bio = db.Column(db.String(200), default="")
    avator = db.Column(db.String(250), default="")

    user_id = db.Column(
        db.String(38), db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    user = db.Relationship("User", foreign_keys=[user_id])

    def set_avator(self, profile_image):
        """
        Set a new avatar for the user by removing the existing avatar (if any), saving the new one,
        and updating the user's avatar field in the database.

        :param profile_image: The uploaded image file to be set as the new avatar.

        :raises InternalServerError: If there is an error during the file-saving process.
        """
        from config import UPLOAD_FOLDER

        if self.avator:
            path = os.path.join(UPLOAD_FOLDER, self.avator)
            remove_existing_file(path=path)

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(os.path.join(UPLOAD_FOLDER), exist_ok=True)

        self.avator = get_unique_filename(profile_image.filename)

        try:
            # Save the new avatar file to the file storage.
            profile_image.save(os.path.join(UPLOAD_FOLDER, self.avator))
        except Exception as e:
            # Handle exceptions that might occur during file saving.
            print("Error saving avatar: %s" % e)
            raise InternalServerError

    def __repr__(self):
        return "<Profile '{}'>".format(self.user.username)


class UserSecurityToken(BaseModel):
    """
    A token class for storing security token for url.
    """

    __tablename__ = "user_token"

    __table_args__ = (
        Index("ix_user_token_token", "token"),
        Index("ix_user_token_expire", "expire"),
    )

    token = db.Column(
        db.String(72), default=unique_security_token, nullable=False, unique=True
    )

    salt = db.Column(db.String(20), nullable=False)

    expire = db.Column(db.Boolean, default=False, nullable=False, server_default="0")

    user_id = db.Column(
        db.String(38), db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    user = db.Relationship("User", foreign_keys=[user_id])

    @classmethod
    def create_new(cls, **kwargs) -> t.AnyStr:
        """
        Creates a new security token instance for a user
        and saves it to the database.

        :param user_id: The ID of the user for whom the token is being created.
        :return: The generated security token string.

        :raises InternalServerError: If there is an error saving the token to the database.
        """
        try:
            instance = cls(**kwargs)
            instance.save()
        except Exception as e:
            raise InternalServerError

        return instance

    @property
    def is_expired(self) -> bool:
        """
        Checks if the token has expired based
        on its creation time and expiration period.
        """
        if not self.expire:
            expiry_time = self.created_at + timedelta(minutes=15)
            current_time = datetime.now()

            if not expiry_time <= current_time:
                return False

        self.delete()
        return True

    @classmethod
    def is_exists(cls, token: t.AnyStr = None):
        """
        Check if a token already exists in the database.

        :param token: The token to check for existence.

        :return: The first instance found with the specified token,
        or None if not found.
        """
        return cls.query.filter_by(token=token).first()

    def __repr__(self):
        return "<Token '{}' by {}>".format(self.token, self.user)


@event.listens_for(User, "after_insert")
def create_profile_for_user(
    mapper: Mapper, connection: Connection, target: DeclarativeMeta
):
    # Create a Profile instance for the recently created user.
    profile = Profile(user_id=target.id)

    # Execute an INSERT statement to add the user's profile table to the database.
    connection.execute(Profile.__table__.insert(), {"user_id": profile.user_id})
    
    
class Diploma(db.Model):
    __tablename__ = "diploma"

    id = db.Column(db.Integer, primary_key=True)
    apellidos = db.Column(db.String(120), nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    uvus = db.Column(db.String(120), unique=True, nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    perfil = db.Column(db.String(120), unique=True, nullable=False)
    participacion = db.Column(db.String(20), nullable=False)
    comite = db.Column(db.String(255), nullable=True)
    evidencia_aleatoria = db.Column(db.Float, nullable=True)
    horas_de_evidencia_aleatoria = db.Column(db.Float, nullable=True)
    eventos_asistidos = db.Column(db.Integer, nullable=True)
    horas_de_asistencia = db.Column(db.Float, nullable=True)
    reuniones_asistidas = db.Column(db.Integer, nullable=True)
    horas_de_reuniones = db.Column(db.Float, nullable=True)
    bono_de_horas = db.Column(db.Float, nullable=True)
    evidencias_registradas = db.Column(db.Integer, nullable=True)
    horas_de_evidencias = db.Column(db.Float, nullable=True)
    horas_en_total = db.Column(db.Float, nullable=True)
    file_path = db.Column(db.String(255), unique=True, nullable=False)
    sent = db.Column(db.Boolean, default=False, nullable=False, server_default="0")

    @validates('correo')
    def validate_correo(self, key, correo):
        if not re.match(r"^[a-zA-Z0-9_.+-]+@(alum\.)?us\.es$", correo):
            raise ValueError("Correo no tiene un formato válido.")
        return correo

    @validates('perfil')
    def validate_perfil(self, key, perfil):
        if not re.match(r"^https://www\.evidentia\.cloud/2024/profiles/view/\d+$", perfil):
            raise ValueError("Perfil debe comenzar con https://www.evidentia.cloud/2024/profiles/view/ seguido de un número.")
        return perfil

    @validates('participacion')
    def validate_participacion(self, key, participacion):
        valid_types = ["ORGANIZATION", "INTERMEDIATE", "ASSISTANCE"]
        if participacion not in valid_types:
            raise ValueError(f"Participación no válida. Debe ser uno de: {', '.join(valid_types)}.")
        return participacion

    @validates('comite')
    def validate_comite(self, key, comite):
        if comite is None:
            return comite # Comité es opcional        
        valid_comites = {"Presidencia", "Secretaría", "Programa", "Igualdad", "Sostenibilidad", "Finanzas", "Logística", "Comunicación"}
        # Usar `split` y eliminar elementos vacíos
        comite_list = [c.strip() for c in comite.split(" | ") if c.strip()]
        if not set(comite_list).issubset(valid_comites):
            raise ValueError("Comité no válido.")
        # Unir la lista filtrada en caso de que haya espacios extra
        return " | ".join(comite_list)
    
    @classmethod
    def from_excel_row(cls, row):
        def to_float(value):
            return float(value) if pd.notnull(value) else None

        def to_int(value):
            return int(value) if pd.notnull(value) else None

        return cls(
            apellidos=row["Apellidos"],
            nombre=row["Nombre"],
            uvus=row["Uvus"],
            correo=row["Correo"],
            perfil=row["Perfil"],
            participacion=row["Participación"],
            comite=row["Comité"] if pd.notnull(row["Comité"]) else None,
            evidencia_aleatoria=to_float(row["Evidencia aleatoria"]),
            horas_de_evidencia_aleatoria=to_float(row["Horas de evidencia aleatoria"]),
            eventos_asistidos=to_int(row["Eventos asistidos"]),
            horas_de_asistencia=to_float(row["Horas de asistencia"]),
            reuniones_asistidas=to_int(row["Reuniones asistidas"]),
            horas_de_reuniones=to_float(row["Horas de reuniones"]),
            bono_de_horas=to_float(row["Bono de horas"]),
            evidencias_registradas=to_int(row["Evidencias registradas"]),
            horas_de_evidencias=to_float(row["Horas de evidencias"]),
            horas_en_total=to_float(row["Horas en total"]),
            file_path=generate_file_path(row["Uvus"])
        )
    
 # método para generar la ruta del diploma
def generate_file_path(uvus):
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return f"diplomas/{uvus}_{random_str}.pdf"
        
# función realizará la validación de la estructura del archivo y los datos específicos de cada campo. Si se detecta algún error, 
# lanzará una excepción y no guardará los datos.
def validate_and_save_excel(file):
    try:
        df = pd.read_excel(file)
        print("Archivo Excel leído exitosamente.")
    except Exception as e:
        print("Error al leer el archivo Excel:", e)
        raise ValidationError("Error reading the Excel file. Please make sure it's a valid .xlsx file.")

    # Verifica que las columnas coincidan
    expected_columns = [
        "Apellidos", "Nombre", "Uvus", "Correo", "Perfil", "Participación", "Comité",
        "Evidencia aleatoria", "Horas de evidencia aleatoria", "Eventos asistidos",
        "Horas de asistencia", "Reuniones asistidas", "Horas de reuniones", "Bono de horas",
        "Evidencias registradas", "Horas de evidencias", "Horas en total"
    ]

    if list(df.columns) != expected_columns:
        print("Estructura de columnas en el archivo:", df.columns)
        raise ValidationError("Excel columns do not match the expected structure.")

    # Verificar unicidad de 'uvus', 'correo' y 'perfil'
    unique_uvus = set()
    unique_correos = set()
    unique_perfiles = set()
    records = []

    for index, row in df.iterrows():
        # Validar UVUS, Correo y Perfil
        if row["Uvus"] in unique_uvus:
            raise ValidationError(f"Duplicated UVUS found in row {index + 1}.")
        if row["Correo"] in unique_correos:
            raise ValidationError(f"Duplicated email found in row {index + 1}.")
        if row["Perfil"] in unique_perfiles:
            raise ValidationError(f"Duplicated profile found in row {index + 1}.")

        unique_uvus.add(row["Uvus"])
        unique_correos.add(row["Correo"])
        unique_perfiles.add(row["Perfil"])

        # Crear instancia de Diploma desde la fila actual
        try:
            diploma = Diploma.from_excel_row(row)
            records.append(diploma)
        except Exception as e:
            print(f"Error al crear Diploma en la fila {index + 1}: {e}")
            raise ValidationError(f"Error in row {index + 1}: {e}")

    # Guardar todos los registros en una transacción
    try:
        db.session.bulk_save_objects(records)
        db.session.commit()
        print("Datos guardados exitosamente en la base de datos.")
        try:
            generate_all_pdfs()
        except Exception as e:
            print("Error al generar los PDFs:", e)
            raise ValidationError("Error generating PDFs. Please try again.")
    except IntegrityError as e:
        db.session.rollback()
        print("Error de integridad al guardar los datos:", e)
        raise ValidationError("Error saving data. Ensure all records are unique.")
    except Exception as e:
        db.session.rollback()
        print("Error inesperado al guardar los datos:", e)
        raise ValidationError("An error occurred while saving data to the database.")
    

def text_pdf_format(texto, ancho_maximo, can):
    palabras = texto.split()
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        if can.stringWidth(linea_actual + " " + palabra) <= ancho_maximo:
            linea_actual += (palabra + " ")
        else:
            lineas.append(linea_actual.strip())
            linea_actual = palabra + " "

    if linea_actual:
        lineas.append(linea_actual.strip())

    return lineas

def generate_pdf(diploma, plantilla_pdf):
    # leemos el PDF plantilla para obtener sus dimensiones
    lector = PdfReader(plantilla_pdf)
    pagina = lector.pages[0]
    ancho = float(pagina.mediabox.width)  
    alto = float(pagina.mediabox.height)  

    # creamos un PDF temporal con el texto deseado
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(ancho, alto))
    texto = f"Enhorabuena {diploma.nombre} {diploma.apellidos}, has participado en las jornadas Innosoft como {diploma.participacion}"

    # configuramos la fuente y el tamaño
    can.setFont("Times-Roman", 26)

    # calculamos el ancho máximo disponible y dividir el texto en líneas
    ancho_maximo = ancho * 0.60 
    lineas = text_pdf_format(texto, ancho_maximo, can)

    # calculamos la posición inicial para centrar el texto verticalmente
    altura_total_texto = len(lineas) * 40  
    coordenada_y = (alto / 2.25) + (altura_total_texto / 2)

    # dibujamos cada línea centrada
    for linea in lineas:
        ancho_texto = can.stringWidth(linea)
        coordenada_x = (ancho - ancho_texto) / 2  
        can.drawString(coordenada_x, coordenada_y, linea)
        coordenada_y -= 40  

    can.save()

    # movemos a la posición del principio
    packet.seek(0)
    nuevo_pdf = PdfReader(packet)
    
    # añadimos texto sobre la plantilla
    writer = PdfWriter()
    pagina.merge_page(nuevo_pdf.pages[0])
    writer.add_page(pagina)

    # creamos la ruta de la carpeta donde se guardarán los diplomas
    folder_path = os.path.join(current_app.root_path, "..", "diplomas")
    folder_path = os.path.abspath(folder_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    # usamos el nombre de archivo de la función generate_pdf
    file_path = os.path.join(folder_path, os.path.basename(diploma.file_path))
    
    # guardamos el nuevo diploma con el nombre de archivo deseado
    with open(file_path, "wb") as output_pdf:
        writer.write(output_pdf)


# función para generar los PDFs para todos los diplomas
def generate_all_pdfs():   
    # creamos la ruta de la carpeta donde se guardarán los diplomas
    folder_path = os.path.join(current_app.root_path, "..", "diplomas")
    folder_path = os.path.abspath(folder_path)
    # eliminamos la carpeta si ya existe y tiene contenido
    if os.path.exists(folder_path) and os.listdir(folder_path):  
        shutil.rmtree(folder_path)  
       
    diplomas = Diploma.query.all() 
    for diploma in diplomas:
        generate_pdf(diploma,"docs/Plantilla diploma.pdf")