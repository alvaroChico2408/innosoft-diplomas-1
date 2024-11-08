from app.modules.diplomas.models import Diplomas
from core.repositories.BaseRepository import BaseRepository


class DiplomasRepository(BaseRepository):
    def __init__(self):
        super().__init__(Diplomas)
