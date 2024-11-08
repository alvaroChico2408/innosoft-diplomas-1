from app.modules.diplomas.repositories import DiplomasRepository
from core.services.BaseService import BaseService


class DiplomasService(BaseService):
    def __init__(self):
        super().__init__(DiplomasRepository())
