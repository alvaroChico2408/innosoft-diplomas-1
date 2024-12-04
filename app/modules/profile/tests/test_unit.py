import pytest
from unittest.mock import patch, MagicMock
from app.modules.profile.services import UserProfileService
from werkzeug.datastructures import MultiDict
from flask_login import current_user
#from app import create_app

@pytest.fixture
def user_profile_service():
    """Fixture para inicializar UserProfileService."""
    return UserProfileService()


def test_update_profile_invalid_form(user_profile_service):
    """Verifica que el perfil no se actualice cuando el formulario no es válido."""
    with patch.object(user_profile_service, 'update') as mock_update, \
         patch.object(user_profile_service, 'get_by_id') as mock_get_by_id, \
         patch.object(user_profile_service.auth_service, 'update_profile') as mock_update_profile, \
         patch('flask_login.utils._get_user') as mock_current_user:

        # Simulando el objeto current_user
        mock_user = MagicMock()
        mock_user.id = 1  # Estableciendo el ID de current_user
        mock_current_user.return_value = mock_user  # Reemplazamos current_user por el mock

        # Simulando los datos
        user_profile_mock = MagicMock()
        user_profile_mock.id = 1
        mock_get_by_id.return_value = user_profile_mock

        form_mock = MagicMock()
        form_mock.validate.return_value = False  # Formulario no válido
        form_mock.errors = {'email': ['Invalid email address']}

        # Llamando al método que estamos probando
        result, message = user_profile_service.update_profile(1, form_mock)

        # Verificaciones
        mock_update.assert_not_called()
        mock_update_profile.assert_not_called()

        assert result is None
        assert message == form_mock.errors

def test_update_profile_valid_form(user_profile_service):
    """Verifica que el perfil se actualice cuando el formulario es válido."""
    with patch.object(user_profile_service, 'update_profile') as mock_update_profile, \
         patch('flask_login.utils._get_user') as mock_current_user:

        # Simulando el objeto current_user
        mock_user = MagicMock()
        mock_user.id = 1  # Estableciendo el ID de current_user
        mock_current_user.return_value = mock_user  # Reemplazamos current_user por el mock

        # Simulando los datos
        user_profile_mock = MagicMock()
        user_profile_mock.id = 1
        mock_update_profile.return_value = user_profile_mock, None  # Simulamos dos valores: el perfil y None

        form_mock = MagicMock()
        form_mock.validate.return_value = True  # Formulario válido

        # Llamando al método que estamos probando
        result, message = user_profile_service.update_profile(1, form_mock)

        # Verificaciones
        mock_update_profile.assert_called_once()
        assert result == user_profile_mock  # Usamos `==` para comparar objetos
        assert message is None  # `None` porque el formulario es válido