import re
from datetime import datetime
from sqlalchemy.orm import validates
import pandas as pd
from app import db
import random
import string


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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
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
            return comite
        valid_comites = {"Presidencia", "Secretaría", "Programa", "Igualdad", "Sostenibilidad", "Finanzas", "Logística", "Comunicación"}
        comite_list = [c.strip() for c in comite.split(" | ") if c.strip()]
        if not set(comite_list).issubset(valid_comites):
            raise ValueError("Comité no válido.")
        return " | ".join(comite_list)
    

    @classmethod
    def from_excel_row(cls, row):
        def to_float(value):
            return float(value) if pd.notnull(value) else None

        def to_int(value):
            return int(value) if pd.notnull(value) else None
        
        def generate_file_path(uvus):
            random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            return f"docs/diplomas/{uvus}_{random_str}.pdf"

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
        
        
        
class DiplomaTemplate(db.Model):
    __tablename__ = 'diploma_templates'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), unique=True, nullable=False)
    custom_text = db.Column(db.String(500), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    

