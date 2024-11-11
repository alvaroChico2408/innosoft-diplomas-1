from app.modules.diplomas.models import Diploma
from core.repositories.BaseRepository import BaseRepository


class DiplomasRepository(BaseRepository):
    def __init__(self):
        super().__init__(Diploma)
