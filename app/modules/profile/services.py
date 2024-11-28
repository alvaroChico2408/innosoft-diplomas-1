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
            updated_data = {key: value for key, value in form.data.items() if value}
            updated_instance = self.update(user_profile_id, **updated_data)

            user_profile = self.get_by_id(user_profile_id)
            email = form.email.data
            
            self.auth_service.update_profile(current_user.id, email)
            self.repository.session.add(user_profile)
            self.repository.session.commit()
            return updated_instance, None

        return None, form.errors

        