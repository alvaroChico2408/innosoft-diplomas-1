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

'''
@pytest.fixture
def app():
    """Fixture para crear la aplicación Flask para las pruebas."""
    app = create_app()  # Asumiendo que tienes una función 'create_app' que crea tu app Flask
    with app.app_context():
        yield app

def test_update_profile_successful(user_profile_service, app):
    """Verifica que el perfil se actualice correctamente cuando el formulario es válido."""
    with app.app_context(), \
         patch.object(user_profile_service, 'update') as mock_update, \
         patch.object(user_profile_service, 'get_by_id') as mock_get_by_id, \
         patch.object(user_profile_service.auth_service, 'update_profile') as mock_update_profile, \
         patch('flask_login.utils._get_user') as mock_current_user:

        # Simulando el objeto current_user
        mock_user = MagicMock()
        mock_user.id = 1  # Estableciendo el ID de current_user
        mock_current_user.return_value = mock_user  # Reemplazamos current_user por el mock

        # Simulando los datos de un perfil de usuario
        user_profile_mock = MagicMock()
        user_profile_mock.id = 1

        # Simulando el _sa_instance_state, __name__, y otros atributos necesarios
        user_profile_mock._sa_instance_state = MagicMock()
        user_profile_mock.__name__ = "UserProfile"  # Para evitar el error de atributo __name__
        user_profile_mock.__mapper__ = MagicMock()  # Simulando el mapper de SQLAlchemy

        mock_get_by_id.return_value = user_profile_mock

        # Simulando el formulario
        form_mock = MagicMock()
        form_mock.validate.return_value = True  # El formulario es válido
        form_mock.data = MultiDict([('name', 'New Name'), ('surname', 'New Surname'), ('email', 'newemail@example.com')])
        form_mock.email.data = 'newemail@example.com'  # Estableciendo el campo email

        # Simulando las respuestas de los mocks
        mock_update.return_value = user_profile_mock
        mock_update_profile.return_value = None  # Sin errores

        # IDs de usuario
        user_profile_id = 1

        # Llamando al método que estamos probando
        result, message = user_profile_service.update_profile(user_profile_id, form_mock)

        # Verificaciones
        mock_update.assert_called_once_with(user_profile_id, name='New Name', surname='New Surname')
        mock_update_profile.assert_called_once_with(mock_user.id, 'newemail@example.com')

        # Verificando los resultados esperados
        assert result == user_profile_mock
        assert message is None  # Asegurándose de que no haya mensaje de error
'''

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
