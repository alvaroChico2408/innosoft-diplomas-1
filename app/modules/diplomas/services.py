from app.modules.diplomas.repositories import DiplomasRepository
from core.services.BaseService import BaseService
from app.modules.diplomas.models import Diploma
from sqlalchemy.exc import IntegrityError
from wtforms import ValidationError
from app import db
import pandas as pd
import os
import shutil
from flask import current_app
import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas


class DiplomasService(BaseService):
    
    def __init__(self):
        super().__init__(DiplomasRepository())


    # función realizará la validación de la estructura del archivo y los datos específicos de cada campo. Si se detecta algún error, 
    # lanzará una excepción y no guardará los datos.
    def validate_and_save_excel(self, file, template):
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
                self.generate_all_pdfs(template)
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


    # función para generar los PDFs para todos los diplomas
    def generate_all_pdfs(self,plantilla_pdf):
        # creamos la ruta de la carpeta donde se guardarán los diplomas
        folder_path = os.path.join(current_app.root_path, "..", "diplomas")
        folder_path = os.path.abspath(folder_path)
        # eliminamos la carpeta si ya existe y tiene contenido
        if os.path.exists(folder_path) and os.listdir(folder_path):
            shutil.rmtree(folder_path)

        diplomas = Diploma.query.all()
        for diploma in diplomas:
            self.generate_pdf(diploma, plantilla_pdf)            
            
            
    def generate_pdf(self, diploma, plantilla_pdf):
        # obtenemos la ruta completa del archivo PDF de la plantilla
        plantilla_pdf_path = os.path.abspath(plantilla_pdf.file_path)
        
        # verificamos que el archivo exista antes de intentar abrirlo
        if not os.path.exists(plantilla_pdf_path):
            raise FileNotFoundError(f"El archivo de plantilla no se encontró en {plantilla_pdf_path}")
        
        # leemos el PDF plantilla para obtener sus dimensiones
        lector = PdfReader(plantilla_pdf_path)
        pagina = lector.pages[0]
        ancho = float(pagina.mediabox.width)
        alto = float(pagina.mediabox.height)

        # creamos un PDF temporal con el texto deseado
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(ancho, alto))
        
        # generamos el texto personalizado reemplazando los marcadores
        texto_personalizado = self.generate_custom_text(plantilla_pdf.custom_text, diploma)
        
        # configuramos la fuente y el tamaño
        can.setFont("Times-Roman", 26)

        # calculamos el ancho máximo disponible y dividir el texto en líneas
        ancho_maximo = ancho * 0.60
        lineas = self.text_pdf_format(texto_personalizado, ancho_maximo, can)

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
        folder_path = os.path.join(current_app.root_path, "../docs/diplomas")
        folder_path = os.path.abspath(folder_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)

        # usamos el nombre de archivo de la función generate_pdf
        file_path = os.path.join(folder_path, os.path.basename(diploma.file_path))

        # guardamos el nuevo diploma con el nombre de archivo deseado
        with open(file_path, "wb") as output_pdf:
            writer.write(output_pdf)


    def generate_custom_text(self, custom_text, diploma):
        """
        Reemplaza los marcadores en el texto personalizado con los valores del diploma.
        Los marcadores están definidos entre corchetes, e.g., [nombre], [apellidos].
        """
        if not custom_text:
            # Texto predeterminado si no hay texto personalizado
            return f"Enhorabuena {diploma.nombre} {diploma.apellidos}, has participado en las jornadas Innosoft como {diploma.participacion}"
        
        # Diccionario con los atributos del diploma
        atributos = {
            "nombre": diploma.nombre,
            "apellidos": diploma.apellidos,
            "uvus": diploma.uvus,
            "correo": diploma.correo,
            "perfil": diploma.perfil,
            "participacion": diploma.participacion,
            "comite": diploma.comite
        }

        # Reemplazar cada marcador en el texto personalizado
        for marcador, valor in atributos.items():
            marcador_formateado = f"[{marcador}]"
            custom_text = custom_text.replace(marcador_formateado, str(valor))
        
        return custom_text

            
            
    def text_pdf_format(self, texto, ancho_maximo, can):
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

    def generate_preview_with_text(self, template_path, custom_text):
        try:
            # Leer el archivo de plantilla
            reader = PdfReader(template_path)
            page = reader.pages[0]

            # Obtener dimensiones de la página
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)

            # Crear un PDF temporal con el texto superpuesto
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=(width, height))

            # Configuración del texto
            can.setFont("Times-Roman", 26)
            text_width = width * 0.8
            text_lines = self.text_pdf_format(custom_text, text_width, can)

            # Posicionar el texto centrado verticalmente
            y_position = height / 2 + len(text_lines) * 15
            for line in text_lines:
                text_x = (width - can.stringWidth(line)) / 2
                can.drawString(text_x, y_position, line)
                y_position -= 30

            can.save()
            packet.seek(0)

            # Leer el PDF temporal con el texto
            temp_pdf = PdfReader(packet)
            temp_page = temp_pdf.pages[0]

            # Combinar la página temporal con el texto en la plantilla original
            page.merge_page(temp_page)

            # Crear un archivo temporal para guardar el PDF final
            temp_dir = os.path.join(current_app.root_path, "docs")
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir, exist_ok=True)

            temp_path = os.path.join(temp_dir, "temp_preview.pdf")
            writer = PdfWriter()
            writer.add_page(page)

            with open(temp_path, "wb") as output_file:
                writer.write(output_file)

            return temp_path
        except Exception as e:
            print(f"Error al generar vista previa: {e}")
            raise