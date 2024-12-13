import pytest
from unittest.mock import patch, MagicMock
from app.modules.profile.services import UserProfileService


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

def test_set_password_hashing():
    from app.modules.profile.models import UserProfile
    user_profile = UserProfile()
    plain_password = "my_secure_password"
    user_profile.set_password(plain_password)

    # Asegurarse de que la contraseña se almacena en formato encriptado
    assert user_profile.password != plain_password
    assert len(user_profile.password) == 64  # Longitud esperada de un hash SHA-256

def test_get_by_user_id():
    from app.modules.profile.repositories import UserProfileRepository
    with patch('app.modules.profile.models.UserProfile.query') as mock_query:
        mock_instance = MagicMock()
        mock_query.filter_by.return_value.first.return_value = mock_instance

        repository = UserProfileRepository()
        result = repository.get_by_user_id(1)

        # Verificar que el método de consulta fue llamado con los argumentos correctos
        mock_query.filter_by.assert_called_once_with(user_id=1)
        assert result == mock_instance

def test_user_profile_form_validation():
    from app.modules.profile.forms import UserProfileForm

    form = UserProfileForm(
        name="John",
        surname="Doe",
        email="john.doe@example.com"
    )

    # Verificar que el formulario es válido
    assert form.validate()

def test_get_by_user_id_returns_none():
    from app.modules.profile.repositories import UserProfileRepository
    with patch('app.modules.profile.models.UserProfile.query') as mock_query:
        mock_query.filter_by.return_value.first.return_value = None

        repository = UserProfileRepository()
        result = repository.get_by_user_id(999)  # ID inexistente

        # Verificar que se devuelve None
        mock_query.filter_by.assert_called_once_with(user_id=999)
        assert result is None

def test_user_profile_form_invalid_email():
    from app.modules.profile.forms import UserProfileForm

    form = UserProfileForm(
        name="Jane",
        surname="Doe",
        email="invalid-email"
    )

    # Verificar que el formulario no es válido debido al email incorrecto
    assert not form.validate()
    assert 'email' in form.errors
