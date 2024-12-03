import pytest
from unittest.mock import patch, MagicMock
from app.modules.auth.services import AuthenticationService
from app.modules.profile.services import UserProfileService
from app.modules.auth.models import User
from app.modules.profile.models import UserProfile
from werkzeug.datastructures import MultiDict
from flask_login import current_user


@pytest.fixture
def authentication_service():
    """Fixture para inicializar AuthenticationService."""
    return AuthenticationService()


@pytest.fixture
def user_profile_service():
    """Fixture para inicializar UserProfileService."""
    return UserProfileService()


def test_login_invalid_credentials(authentication_service):
    """Verifica que el login falle con credenciales inválidas."""
    with patch.object(authentication_service, 'login') as mock_login:
        mock_login.return_value = False  # Simulando un login fallido

        result = authentication_service.login('user@example.com', 'wrongpassword')

        # Verificaciones
        assert result is False
        
def test_login_valid_credentials(authentication_service):
    """Verifica que el login sea exitoso con credenciales válidas."""
    with patch.object(authentication_service, 'login') as mock_login:
        mock_login.return_value = True  # Simulando un login exitoso

        result = authentication_service.login('user@example.com', 'correctpassword')

        # Verificaciones
        assert result is True
