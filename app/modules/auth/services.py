import os

from flask_login import login_user
from sqlalchemy.exc import IntegrityError
from flask_login import current_user

from app.modules.auth.models import User
from app.modules.auth.repositories import UserRepository
from app.modules.profile.models import UserProfile
from app.modules.profile.repositories import UserProfileRepository
from core.configuration.configuration import uploads_folder_name
from core.services.BaseService import BaseService
import hashlib


class AuthenticationService(BaseService):

    def __init__(self):
        super().__init__(UserRepository())
        self.user_profile_repository = UserProfileRepository()

    def login(self, email, password, remember=True):
        user = self.repository.get_by_email(email)
        if user is not None and user.check_password(password):
            login_user(user, remember=remember)
            return True
        return False

    def is_email_available(self, email: str) -> bool:
        return self.repository.get_by_email(email) is None

    def create_with_profile(self, **kwargs):
        try:
            email = kwargs.pop("email", None)
            password = kwargs.pop("password", None)
            name = kwargs.pop("name", None)
            surname = kwargs.pop("surname", None)

            if not email:
                raise ValueError("Email is required.")
            if not password:
                raise ValueError("Password is required.")
            if not name:
                raise ValueError("Name is required.")
            if not surname:
                raise ValueError("Surname is required.")

            if not self.is_email_available(email):
                return None, "The email address is already registered."

            user_data = {
                "email": email,
                "password": password,
                "active": False,
            }

            profile_data = {
                "name": name,
                "surname": surname,
                "email": email,
                "password": hashlib.sha256(password.encode()).hexdigest(),
            }

            user = self.create(commit=False, **user_data)
            profile_data["user_id"] = user.id
            self.user_profile_repository.create(**profile_data)
            self.repository.session.commit()
        except IntegrityError as e:
            self.repository.session.rollback()
            if "Duplicate entry" in str(e):
                return None, "The email address is already registered."
            return None, "An error occurred while creating the profile."
        except Exception:
            self.repository.session.rollback()
            return None, "Unexpected error occurred."
        return user

    def update_profile(self, user_id, email, **kwargs):
        user = self.repository.get_by_id(user_id)

        if not user:
            return None, "User not found."

        if email:
            user.email = email

        for key, value in kwargs.items():
            if hasattr(user.profile, key):
                setattr(user.profile, key, value)

        self.repository.session.add(user)
        self.user_profile_repository.session.add(user.profile)
        self.repository.session.commit()
        self.user_profile_repository.session.commit()
        return user

    def change_password(self, user_id, new_password):
        user = self.repository.get_by_id(user_id)
        if not user:
            return None, "User not found."

        # Actualizar contraseña en el modelo User
        user.set_password(new_password)

        # Actualizar también la contraseña en el UserProfile
        user_profile = user.profile
        if user_profile:
            user_profile.set_password(new_password)

        # Guardar cambios en la base de datos
        try:
            self.repository.session.add(user)
            if user_profile:
                self.user_profile_repository.session.add(user_profile)
            self.repository.session.commit()
            self.user_profile_repository.session.commit()
            return user, None
        except Exception as e:
            self.repository.session.rollback()
            return None, str(e)

    def get_authenticated_user(self) -> User | None:
        if current_user.is_authenticated:
            return current_user
        return None

    def get_authenticated_user_profile(self) -> UserProfile | None:
        if current_user.is_authenticated:
            return current_user.profile
        return None

    def temp_folder_by_user(self, user: User) -> str:
        return os.path.join(uploads_folder_name(), "temp", str(user.id))

    def get_by_email(self, email: str, active: bool = True) -> User:
        return self.repository.get_by_email(email, active)
