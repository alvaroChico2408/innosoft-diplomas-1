import pytest
from app import db
from app.modules.conftest import login, logout
from app.modules.auth.models import User
from flask_login import current_user

@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extiende el fixture test_client para agregar datos específicos para las pruebas del módulo.
    """
    with test_client.application.app_context():
        user_test = User(email='user@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

    yield test_client

def test_login(test_client):
    """
    Prueba el inicio de sesión de un usuario.
    """
    # Intentar iniciar sesión con credenciales válidas
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "El inicio de sesión no fue exitoso."
    assert current_user.is_authenticated, "El usuario no está autenticado después del inicio de sesión."

    logout(test_client)

def test_logout(test_client):
    """
    Prueba el cierre de sesión de un usuario.
    """
    # Iniciar sesión primero
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "El inicio de sesión no fue exitoso."

    # Cerrar sesión
    logout_response = logout(test_client)
    assert logout_response.status_code == 200, "El cierre de sesión no fue exitoso."
    assert not current_user.is_authenticated, "El usuario todavía está autenticado después del cierre de sesión."


def test_login_invalid_credentials(test_client):
    """
    Prueba el inicio de sesión con credenciales inválidas.
    """
    # Intentar iniciar sesión con credenciales inválidas
    login_response = login(test_client, "user@example", "test1234")
    assert login_response.status_code == 200, "El inicio de sesión no fue exitoso."
    
    


