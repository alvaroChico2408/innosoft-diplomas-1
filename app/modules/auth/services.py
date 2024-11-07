import os
from flask_login import login_user, current_user
from app.modules.auth.models import User
from app.modules.auth.repositories import UserRepository
from app.modules.profile.models import UserProfile
from app.modules.profile.repositories import UserProfileRepository
from core.configuration.configuration import uploads_folder_name
from core.services.BaseService import BaseService

from flask import flash


class AuthenticationService(BaseService):

    def __init__(self):
        super().__init__(UserRepository())
        self.user_profile_repository = UserProfileRepository()

    def login(self, username, password, remember=True):
        user = self.repository.get_by_username(username)
        if user is not None and user.check_password(password):
            login_user(user, remember=remember)
            print(current_user.is_authenticated)

            return True

        return False

    def is_email_available(self, email: str) -> bool:
        return self.repository.get_by_email(email) is None

    def create_with_profile(self, **kwargs):
        try:
            email = kwargs.pop("email", None)
            password = kwargs.pop("password", None)
            first_name = kwargs.pop("first_name", None)
            last_name = kwargs.pop("last_name", None)

            if not email:
                raise ValueError("Email is required.")
            if not password:
                raise ValueError("Password is required.")
            if not first_name:
                raise ValueError("First name is required.")
            if not last_name:
                raise ValueError("Last name is required.")

            user_data = {
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "active": False,
            }

            user = self.repository.create(**user_data)

            # Create the profile associated with the user
            profile_data = {
                "user_id": user.id,
                "name": first_name,
                "surname": last_name,
            }
            self.user_profile_repository.create(**profile_data)

            self.repository.session.commit()
        except Exception as exc:
            self.repository.session.rollback()
            raise exc
        return user

    def update_profile(self, user_profile_id, form):
        if form.validate():
            updated_instance = self.user_profile_repository.update(user_profile_id, **form.data)
            return updated_instance, None

        return None, form.errors

    def get_authenticated_user(self) -> User | None:
        if current_user.is_authenticated:
            return current_user
        return None

    def get_authenticated_user_profile(self) -> UserProfile | None:
        if current_user.is_authenticated and current_user.profile:
            return current_user.profile
        return None

    def temp_folder_by_user(self, user: User) -> str:
        return os.path.join(uploads_folder_name(), "temp", str(user.id))

    def get_by_email(self, email: str, active: bool = True) -> User:
        return self.repository.get_by_email(email, active)
