import pytest
import os
import shutil
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.environment.host import get_host_for_selenium_testing

from app import create_app, db
from app.modules.auth.models import User
from app.modules.diplomas.models import Diploma, DiplomaTemplate
from app.modules.diplomas.services import DiplomasService


@pytest.fixture(scope='session')
def test_app():
    """ Create and configure a new app instance for each test session. """
    test_app = create_app('testing')

    with test_app.app_context():
        # Imprimir los blueprints registrados
        print("TESTING SUITE (1): Blueprints registrados:", test_app.blueprints)
        yield test_app


@pytest.fixture(scope='module')
def test_client(test_app):

    with test_app.test_client() as testing_client:
        with test_app.app_context():
            print("TESTING SUITE (2): Blueprints registrados:", test_app.blueprints)

            db.drop_all()
            db.create_all()
            """
            The test suite always includes the following user in order to avoid repetition
            of its creation
            """
            user_test = User(email='test@example.com', password='test1234')
            db.session.add(user_test)
            db.session.commit()

            print("Rutas registradas:")
            for rule in test_app.url_map.iter_rules():
                print(rule)
            yield testing_client

            db.session.remove()
            db.drop_all()


@pytest.fixture(scope='function')
def clean_database():
    db.session.remove()
    db.drop_all()
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()
    db.create_all()


@pytest.fixture(scope="function")
def populate_diplomas_with_pdfs(test_app):
    """Puebla la base de datos con diplomas y genera los PDFs correspondientes."""
    with test_app.app_context():
        # Ruta de la carpeta de diplomas
        folder_path = os.path.join(test_app.root_path, "../docs/diplomas")
        backup_path = os.path.join(test_app.root_path, "../docs/diplomas_backup")

        # Crear una copia de seguridad de la carpeta de diplomas
        if os.path.exists(folder_path):
            if os.path.exists(backup_path):
                shutil.rmtree(backup_path)  # Eliminar una copia previa
            shutil.copytree(folder_path, backup_path)

        # Limpia los diplomas en la base de datos
        db.session.query(Diploma).delete()
        db.session.commit()

        # Obtiene la plantilla existente
        template = DiplomaTemplate.query.first()
        if not template:
            raise ValueError("No se encontró ninguna plantilla en la base de datos. Asegúrate de que exista una plantilla antes de ejecutar las pruebas.")

        # Crea diplomas de ejemplo
        diplomas = [
            Diploma(
                apellidos="Aragón Sánchez",
                nombre="Alejandro",
                uvus="alearasan",
                correo="alearasan@alum.us.es",
                perfil="https://www.evidentia.cloud/2024/profiles/view/1",
                participacion="ORGANIZATION",
                comite="Logística",
                evidencia_aleatoria=2.5,
                horas_de_evidencia_aleatoria=10.0,
                eventos_asistidos=5,
                horas_de_asistencia=15.0,
                reuniones_asistidas=2,
                horas_de_reuniones=3.0,
                bono_de_horas=5.0,
                evidencias_registradas=3,
                horas_de_evidencias=12.0,
                horas_en_total=45.0,
                file_path="docs/diplomas/alearasan_test.pdf"
            ),
            Diploma(
                apellidos="Fernández",
                nombre="Lucía",
                uvus="luciaf",
                correo="luciaf@us.es",
                perfil="https://www.evidentia.cloud/2024/profiles/view/2",
                participacion="ASSISTANCE",
                comite=None,
                evidencia_aleatoria=None,
                horas_de_evidencia_aleatoria=None,
                eventos_asistidos=3,
                horas_de_asistencia=9.0,
                reuniones_asistidas=None,
                horas_de_reuniones=None,
                bono_de_horas=1.0,
                evidencias_registradas=None,
                horas_de_evidencias=None,
                horas_en_total=10.0,
                file_path="docs/diplomas/luciaf_test.pdf"
            ),
        ]
        db.session.add_all(diplomas)
        db.session.commit()

        # Genera los PDFs usando DiplomasService
        service = DiplomasService()
        service.generate_all_pdfs(template)

        yield  # Fixture disponible para las pruebas

        # Limpia la base de datos
        db.session.query(Diploma).delete()
        db.session.commit()

        # Limpia la carpeta de diplomas
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

        # Restaura la carpeta original desde la copia de seguridad
        if os.path.exists(backup_path):
            shutil.copytree(backup_path, folder_path)
            shutil.rmtree(backup_path)  # Elimina la copia de seguridad


def login(test_client, email, password):
    """
    Authenticates the user with the credentials provided.

    Args:
        test_client: Flask test client.
        email (str): User's email address.
        password (str): User's password.

    Returns:
        response: POST login request response.
    """
    response = test_client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)
    return response


def logout(test_client):
    """
    Logs out the user.

    Args:
        test_client: Flask test client.

    Returns:
        response: Response to GET request to log out.
    """
    return test_client.get('/logout', follow_redirects=True)


def login_selenium(driver, email, password):
    """
    Realiza el login del usuario en Selenium.
    
    Args:
        driver: WebDriver de Selenium.
        email (str): Correo electrónico del usuario.
        password (str): Contraseña del usuario.
    """
    host = get_host_for_selenium_testing()
    driver.get(f'{host}/login')
    
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "submit").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".welcome-box h2.display-4.text-primary"))
    )