from app.modules.profile.repositories import UserProfileRepository
from core.services.BaseService import BaseService
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from app.modules.auth.services import AuthenticationService 
from flask_login import current_user
import hashlib


class UserProfileService(BaseService):
    def __init__(self):
        super().__init__(UserProfileRepository())
        self.auth_service = AuthenticationService()

    
    def update_profile(self, user_profile_id, form):
        if form.validate():
            updated_instance = self.update(user_profile_id, **form.data)
            user_profile = self.get_by_id(user_profile_id)
            email = form.email.data
            password = form.password.data if form.password.data else None
            self.auth_service.update_profile(current_user.id, email, password)
            self.repository.session.add(user_profile)
            self.repository.session.commit()
            return updated_instance, None

        return None, form.errors
        