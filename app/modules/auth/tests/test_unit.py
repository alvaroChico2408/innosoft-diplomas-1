import pytest
from unittest.mock import patch, MagicMock
from app.modules.auth.services import AuthenticationService
from app.modules.profile.services import UserProfileService
from app import create_app
from selenium import webdriver


@pytest.fixture
def authentication_service():
    """Fixture para inicializar AuthenticationService."""
    return AuthenticationService()

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # Asegúrate de tener instalado el WebDriver adecuado.
    yield driver
    driver.quit()
            
@pytest.fixture
def user_profile_service():
    """Fixture para inicializar UserProfileService."""
    return UserProfileService()

def test_is_email_available(authentication_service):
    """Verifica que el email esté disponible."""
    with patch.object(authentication_service, 'is_email_available') as mock_is_email_available:
        mock_is_email_available.return_value = True  # Simulando email disponible
        
        result = authentication_service.is_email_available(' ')
        
        # Verificaciones
        
        assert result is True



def test_login_invalid_credentials_wrong_password(authentication_service):
    """Verifica que el login falle con credenciales inválidas."""
    with patch.object(authentication_service, 'login') as mock_login:
        mock_login.return_value = False  # Simulando un login fallido

        result = authentication_service.login('user@example.com', 'wrongpassword')

        # Verificaciones
        assert result is False
     
        
def test_login_invalid_credentials_wrong_email(authentication_service):
    """Verifica que el login falle con credenciales inválidas."""
    with patch.object(authentication_service, 'login') as mock_login:
        mock_login.return_value = False  # Simulando un login fallido

        result = authentication_service.login('wrongemail@example.com', 'correctpassword')

        # Verificaciones
        assert result is False
        
def test_login_invalid_credentials_empty_email(authentication_service):
    """Verifica que el login falle con credenciales inválidas."""
    with patch.object(authentication_service, 'login') as mock_login:
        mock_login.return_value = False  # Simulando un login fallido

        result = authentication_service.login('', 'correctpassword')

        # Verificaciones
        assert result is False
        
def test_login_invalid_credentials_empty_password(authentication_service):
    """Verifica que el login falle con credenciales inválidas."""
    with patch.object(authentication_service, 'login') as mock_login:
        mock_login.return_value = False  # Simulando un login fallido

        result = authentication_service.login('correctemail@example.com', '')

        # Verificaciones
        assert result is False
        
def test_login_valid_credentials(authentication_service):
    """Verifica que el login sea exitoso con credenciales válidas."""
    with patch.object(authentication_service, 'login') as mock_login:
        mock_login.return_value = True  # Simulando un login exitoso

        result = authentication_service.login('user@example.com', 'correctpassword')

        # Verificaciones
        assert result is True

def test_change_password(authentication_service):
    """Verifica que se cambie la contraseña correctamente."""
    with patch.object(authentication_service, 'change_password') as mock_change_password:

        # Simulando el cambio de contraseña
        mock_user = MagicMock()
        mock_user.id = 1
        mock_change_password.return_value = (mock_user, None)

        result, error = authentication_service.change_password(1, 'newpassword')

        # Verificaciones
        mock_change_password.assert_called_once_with(1, 'newpassword')
        assert result is mock_user
        assert error is None

def test_create_user_with_profile(authentication_service):
    """Verifica que un usuario se cree junto con su perfil."""
    with patch.object(authentication_service, 'create_with_profile') as mock_create_with_profile:

        # Simulando la creación de un usuario con perfil
        mock_user = MagicMock()
        mock_user.id = 1
        mock_create_with_profile.return_value = (mock_user, None)

        result, error = authentication_service.create_with_profile(
            email='newuser@example.com',
            password='password123',
            name='John',
            surname='Doe'
        )

        # Verificaciones
        mock_create_with_profile.assert_called_once_with(
            email='newuser@example.com',
            password='password123',
            name='John',
            surname='Doe'
        )
        assert result is mock_user
        assert error is None
        
def test_get_authenticated_user(authentication_service):
    """Verifica que se obtenga el usuario autenticado correctamente."""
    with patch('flask_login.utils._get_user') as mock_current_user:

        # Simulando el usuario autenticado
        mock_user = MagicMock()
        mock_user.id = 1
        mock_current_user.return_value = mock_user

        result = authentication_service.get_authenticated_user()

        # Verificaciones
        assert result == mock_user 
 

def test_get_authenticated_user_profile(authentication_service):
    """Verifica que se obtenga el perfil del usuario autenticado correctamente."""
    with patch('flask_login.utils._get_user') as mock_current_user:

        # Simulando el usuario autenticado
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.profile = MagicMock()
        mock_current_user.return_value = mock_user

        result = authentication_service.get_authenticated_user_profile()

        # Verificaciones
        assert result == mock_user.profile

        
def test_temp_folder_by_user(authentication_service): 
    """Verifica que se obtenga la carpeta temporal del usuario correctamente."""
    with patch('app.modules.auth.services.uploads_folder_name') as mock_uploads_folder_name:

        # Simulando la carpeta temporal del usuario
        mock_user = MagicMock()
        mock_user.id = 1
        mock_uploads_folder_name.return_value = '/uploads'

        result = authentication_service.temp_folder_by_user(mock_user)

        # Verificaciones
        assert result == '/uploads/temp/1'


def test_get_by_email(authentication_service):
    """Verifica que se obtenga un usuario por email correctamente."""
    with patch.object(authentication_service, 'get_by_email') as mock_get_by_email:

        # Simulando la obtención de un usuario por email
        mock_user = MagicMock()
        mock_user.id = 1
        mock_get_by_email.return_value = mock_user


        result= authentication_service.get_by_email(' ')
        
        # Verificaciones
        mock_get_by_email.assert_called_once_with(' ')
        assert result == mock_user
        

def test_update_profile_user_not_found(authentication_service):
    """Prueba de actualización de perfil con usuario inexistente."""
    with patch.object(authentication_service.repository, 'get_by_id', return_value=None):
        user, error = authentication_service.update_profile(999, email="new@example.com")
        assert user is None
        assert error == "User not found."

def test_login_route(client):
    response = client.post('/login', data={'username': 'user', 'password': 'pass'})
    assert response.status_code == 200

def test_logout_route(client):
    # Simula un usuario registrado que inicia sesión
    login_response = client.post('/login', data={'username': 'user', 'password': 'pass'})
    
    # Verifica que el inicio de sesión sea exitoso
    assert login_response.status_code == 200

    # Simula que el usuario se desloguea
    logout_response = client.get('/logout', follow_redirects=True)

    # Verifica que el deslogueo sea exitoso
    assert logout_response.status_code == 200



#def test_auth_seeder():
#    app = create_app('testing')
#    with app.app_context():
#        seeder = AuthSeeder()
#        seeder.run()
#        assert db.session.query(User).count() > 0

def test_create_with_profile_duplicate_email(authentication_service):
    """Verifica que no se permita crear un usuario con un email duplicado."""
    with patch.object(authentication_service, 'is_email_available', return_value=False):
        result, error = authentication_service.create_with_profile(
            email='duplicate@example.com',
            password='password123',
            name='Jane',
            surname='Doe'
        )
        assert result is None
        assert error == "The email address is already registered."


