import pytest
import os
from flask import Flask
from flask_mail import Mail, Message
from app.modules.mail.services import MailService
from app import db
from flask_login import current_user

# Configuración del entorno de prueba
@pytest.fixture(scope="module")
def create_app():
    """
    Configuración inicial del entorno Flask para pruebas.
    """
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['MAIL_SERVER'] = 'smtp.office365.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'user1@example.com'
    app.config['MAIL_PASSWORD'] = 'password'
    app.config['MAIL_DEFAULT_SENDER'] = 'test@example.com'

    with app.app_context():
        yield app

# Fixture para el MailService
@pytest.fixture(scope="module")
def mail_service(create_app):
    service = MailService()
    service.init_app(create_app)
    return service

# Test envío con archivo PDF adjunto
def test_send_email_with_attachment(mail_service):
    """
    Prueba para verificar el envío de correos con archivos PDF adjuntos.
    """
    subject = "Correo con adjunto PDF"
    recipients = ["destinatario@ejemplo.com"]
    body = "Este correo contiene un archivo PDF adjunto."

    test_pdf_path = 'test_files/sample.pdf'
    os.makedirs('test_files', exist_ok=True)

    # Crear archivo PDF de prueba
    with open(test_pdf_path, 'wb') as f:
        f.write(b'Sample PDF content for testing.')

    try:
        mail_service.send_email_with_attachment(subject, recipients, body, test_pdf_path)
        assert os.path.exists(test_pdf_path)
    except Exception as e:
        pytest.fail(f"Envío del correo con adjunto PDF falló: {e}")

    finally:
        # Limpiar archivo después de la prueba
        os.remove(test_pdf_path)

# # Prueba de la ruta `/mail`
# def test_flask_mail_endpoint(create_app):
#     client = create_app.test_client()
#
#     # Realizar la solicitud GET
#     response = client.get('/mail')
#
#     # Verificar si la respuesta devuelve el código 200
#     assert response.status_code == 200, f"La ruta `/mail` devolvió {response.status_code}"

