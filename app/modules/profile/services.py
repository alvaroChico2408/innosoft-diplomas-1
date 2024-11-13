from app.modules.profile.repositories import UserProfileRepository
from core.services.BaseService import BaseService
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from app.modules.auth.services import AuthenticationService 


class UserProfileService(BaseService):
    def __init__(self):
        super().__init__(UserProfileRepository())
        self.auth_service = AuthenticationService()

    
    def update_profile(self, user_profile_id, form):
        if form.validate():
            updated_instance = self.update(user_profile_id, **form.data)
            
            email = form.email.data
            password = form.password.data if form.password.data else None

            updated_user= self.auth_service.update_profile(self.user_id, email, password, **form.data)

            return updated_instance, None

        return None, form.errors
        
'''
class UserProfileService(BaseService):
    def __init__(self):
        super().__init__(UserProfileRepository())

    def update_profile(self, user_profile_id, form):
        if form.validate():
            updated_instance = self.update(user_profile_id, **form.data)
            return updated_instance, None

        return None, form.errors

'''