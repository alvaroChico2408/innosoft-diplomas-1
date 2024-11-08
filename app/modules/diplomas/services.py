from app.modules.diplomas.repositories import DiplomasRepository
from core.services.BaseService import BaseService
import pandas as pd

class DiplomasService(BaseService):
    def __init__(self):
        super().__init__(DiplomasRepository())

    def validate_and_save_excel(self, file):
        """Procesa un archivo Excel y genera diplomas"""
        try:
            # Cargar el archivo Excel usando pandas
            df = pd.read_excel(file)
            print("Archivo Excel cargado con éxito")
            
            # Aquí puedes realizar validaciones adicionales
            print(df.head())  # Imprimir las primeras filas para depuración
            
            # TODO: Implementar la lógica para guardar los datos y generar diplomas
            # Puedes utilizar DiplomasRepository para interactuar con la base de datos
            return True
        except Exception as e:
            print(f"Error al procesar el archivo Excel: {str(e)}")
            raise ValueError(f"Error al procesar el archivo Excel: {str(e)}")
