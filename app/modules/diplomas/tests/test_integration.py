import pytest
from app import db
from app.modules.diplomas.models import Diploma, DiplomaTemplate
from app.modules.diplomas.services import DiplomasService
import os
import json
from flask import url_for
import pandas as pd


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add specific data for integration testing.
    """
    test_client.application.config['SERVER_NAME'] = 'localhost'  # Required for URL generation

    # Create a template for testing
    template = DiplomaTemplate(
            filename="test_template.pdf",
            custom_text="Congratulations [nombre] [apellidos]!",
            file_path="docs/plantillas/test_template.pdf"
        )
    db.session.add(template)
    db.session.commit()

    yield test_client

    # Cleanup after tests
    db.session.query(DiplomaTemplate).delete()
    db.session.commit()

def create_mock_diploma():
    """
    Helper function to create a mock diploma in the database.
    """
    diploma = Diploma(
        apellidos="García",
        nombre="Juan",
        uvus="uvus123",
        correo="juan@alum.us.es",
        perfil="https://www.evidentia.cloud/2024/profiles/view/1",
        participacion="ORGANIZATION",
        comite="Igualdad",
        file_path="docs/plantillas/Plantilla diploma.pdf"
    )
    db.session.add(diploma)
    db.session.commit()
    return diploma

def test_generate_diplomas(test_client):
    """
    Test generating diplomas through the endpoint.
    """
    with test_client.application.app_context():
        # Create a mock Excel file
        mock_file_path = "mock_excel.xlsx"
        mock_data = {
            "Apellidos": ["García"],
            "Nombre": ["Juan"],
            "Uvus": ["uvus123"],
            "Correo": ["juan@alum.us.es"],
            "Perfil": ["https://www.evidentia.cloud/2024/profiles/view/1"],
            "Participación": ["ORGANIZATION"],
            "Comité": ["Igualdad"],
            "Evidencia aleatoria": ["Imagen"],
            "Horas de evidencia aleatoria": [2],
            "Eventos asistidos": [1],
            "Horas de asistencia": [3],
            "Reuniones asistidas": [1],
            "Horas de reuniones": [1],
            "Bono de horas": [0],
            "Evidencias registradas": [2],
            "Horas de evidencias": [5],
            "Horas en total": [10],
        }
        pd.DataFrame(mock_data).to_excel(mock_file_path, index=False)

        template = DiplomaTemplate.query.first()
        
        with open(mock_file_path, "rb") as mock_file:
            response = test_client.post(url_for('diplomas.generate_diplomas', _external=True), data={
                'hours_excel': mock_file,
                'template': template.id
            }, content_type='multipart/form-data', follow_redirects=True)

        assert response.status_code == 200

        os.remove(mock_file_path)
        
def login_user(test_client):
    test_client.post('/login', data={'username': 'testuser', 'password': 'password'})

def test_view_diploma(test_client):
    # Log in as an authenticated user
    login_user(test_client)

    diploma = create_mock_diploma()
    response = test_client.get(url_for('diplomas.view_diploma', diploma_id=diploma.id, _external=True))

    # Verify the response
    assert response.status_code == 302


#    def test_delete_diploma(test_client):
#        # Log in as an authenticated user
#        login_user(test_client)
#
#        diploma = create_mock_diploma()
#        response = test_client.post(url_for('diplomas.delete_diploma', diploma_id=diploma.id, _external=True))
#
#        # Verify the response
#        assert response.status_code == 302

#def test_send_diplomas(test_client):
#    """
#    Test sending diplomas via email.
#    """
#    with test_client.application.app_context():
#        diploma = create_mock_diploma()
#        response = test_client.post(url_for('diplomas.send_diplomas', _external=True),
#                                    data=json.dumps({'diploma_ids': [diploma.id]}),
#                                    content_type='application/json')##

#        assert response.status_code == 200
#        assert b"Successfully sent 1 diplomas." in response.data