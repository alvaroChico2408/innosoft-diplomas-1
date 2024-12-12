import pytest
from unittest.mock import patch
from app.modules.diplomas.services import DiplomasService
from app.modules.diplomas.models import Diploma
from app import create_app
from unittest.mock import patch


@pytest.fixture 
def diploma_service():
    return DiplomasService()

@pytest.fixture 
def diplomas_models():
    return Diploma()

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_validate_and_save_excel(diploma_service):
    
    with patch('app.modules.diplomas.services.DiplomasService.validate_and_save_excel') as mock_validate_and_save_excel:
        mock_validate_and_save_excel.return_value = True
        
        result = diploma_service.validate_and_save_excel('file')
    assert result is True

def test_validate_and_save_excel_with_invalid_file(diploma_service):
    
    with patch('app.modules.diplomas.services.DiplomasService.validate_and_save_excel') as mock_validate_and_save_excel:
        mock_validate_and_save_excel.return_value = False
        
        result = diploma_service.validate_and_save_excel('file')
    assert result is False

    
def test_generate_all_pdfs(diploma_service):
    
    with patch('app.modules.diplomas.services.DiplomasService.generate_all_pdfs') as mock_generate_all_pdfs:
        mock_generate_all_pdfs.return_value = True
        
        result = diploma_service.generate_all_pdfs()
    assert result is True
    
def test_generate_all_pdfs_with_no_data(diploma_service):
        
    with patch('app.modules.diplomas.services.DiplomasService.generate_all_pdfs') as mock_generate_all_pdfs:
        mock_generate_all_pdfs.return_value = False
            
        result = diploma_service.generate_all_pdfs()
    assert result is False
    
def test_generate_pdf(diploma_service):
    
    with patch('app.modules.diplomas.services.DiplomasService.generate_pdf') as mock_generate_pdf:
        mock_generate_pdf.return_value = True
        
        result = diploma_service.generate_pdf('file')
    assert result is True

def test_generate_pdf_with_invalid_file(diploma_service):
    
    with patch('app.modules.diplomas.services.DiplomasService.generate_pdf') as mock_generate_pdf:
        mock_generate_pdf.return_value = False
        
        result = diploma_service.generate_pdf('file')
    assert result is False


def test_text_pdf_format(diploma_service):
    
    with patch('app.modules.diplomas.services.DiplomasService.text_pdf_format') as mock_text_pdf_format:
        mock_text_pdf_format.return_value = True
        
        result = diploma_service.text_pdf_format('file')
    assert result is True

def test_text_pdf_format_with_invalid_file(diploma_service):
    
    with patch('app.modules.diplomas.services.DiplomasService.text_pdf_format') as mock_text_pdf_format:
        mock_text_pdf_format.return_value = False
        
        result = diploma_service.text_pdf_format('file')
    assert result is False

def test_generate_preview_with_text(diploma_service):
    
    with patch('app.modules.diplomas.services.DiplomasService.generate_preview_with_text') as mock_generate_preview_with_text:
        mock_generate_preview_with_text.return_value = True
        
        result = diploma_service.generate_preview_with_text('file')
    assert result is True

def test_generate_preview_with_text_with_invalid_file(diploma_service):
    
    with patch('app.modules.diplomas.services.DiplomasService.generate_preview_with_text') as mock_generate_preview_with_text:
        mock_generate_preview_with_text.return_value = False
        
        result = diploma_service.generate_preview_with_text('file')
    assert result is False
    
def test_generate_custom_text(diploma_service):
    
    with patch('app.modules.diplomas.services.DiplomasService.generate_custom_text') as mock_generate_custom_text:
        mock_generate_custom_text.return_value = True
        
        result = diploma_service.generate_custom_text('file')
    assert result is True
    
def test_generate_custom_text_with_invalid_file(diploma_service):
    
    with patch('app.modules.diplomas.services.DiplomasService.generate_custom_text') as mock_generate_custom_text:
        mock_generate_custom_text.return_value = False
        
        result = diploma_service.generate_custom_text('file')
    assert result is False
    
def test_validate_and_save_excel_empty_file(diploma_service):
    
    with patch('app.modules.diplomas.services.DiplomasService.validate_and_save_excel') as mock_validate_and_save_excel:
        mock_validate_and_save_excel.return_value = False
        
        result = diploma_service.validate_and_save_excel('')
    assert result is False
    
def test_generate_pdf_empty_file(diploma_service):
    
    with patch('app.modules.diplomas.services.DiplomasService.generate_pdf') as mock_generate_pdf:
        mock_generate_pdf.return_value = False
        
        result = diploma_service.generate_pdf('')
    assert result is False

def test_generate_all_pdfs_no_data(diploma_service):
    
    with patch('app.modules.diplomas.services.DiplomasService.generate_all_pdfs') as mock_generate_all_pdfs:
        mock_generate_all_pdfs.return_value = False
        
        result = diploma_service.generate_all_pdfs()
    assert result is False
    

#MODELS
# Test de validación del correo válido
def test_validate_correo_valido(diplomas_models):
    correo_valido = 'user1@example.com'
    
    with patch('app.modules.diplomas.models.Diploma.validate_correo') as mock_validate_correo:
        mock_validate_correo.return_value = correo_valido

        result = diplomas_models.validate_correo('correo', correo_valido)
        assert result == correo_valido
    
# Test de validación del correo inválido
def test_validate_correo_invalido(diplomas_models):
    correo_invalido = 'user1example'  # Un correo incorrecto
    with pytest.raises(ValueError, match="Correo no tiene un formato válido."):
        diplomas_models.validate_correo('correo', correo_invalido)
        
         
# Test válido
def test_validate_perfil_valido(diplomas_models):
    perfil_valido = 'Estudiante'

    with patch('app.modules.diplomas.models.Diploma.validate_perfil') as mock_validate_perfil:
        mock_validate_perfil.return_value = perfil_valido

        result = diplomas_models.validate_perfil('perfil1', perfil_valido)
        assert result == perfil_valido

# Test inválido con ajuste del mensaje de error real
def test_validate_perfil_invalido(diplomas_models):
    perfil_invalido = 'Profesor'  # Un perfil incorrecto
    with pytest.raises(ValueError, match="Perfil debe comenzar con https://www.evidentia.cloud/2024/profiles/view/ seguido de un número."):
        diplomas_models.validate_perfil('perfil', perfil_invalido)


def test_validate_participacion_valida(diplomas_models):
    participacion_valida = 'ORGANIZATION'

    with patch('app.modules.diplomas.models.Diploma.validate_participacion') as mock_validate_participacion:
        mock_validate_participacion.return_value = participacion_valida

        result = diplomas_models.validate_participacion('participacion', participacion_valida)
        assert result == participacion_valida
        
def test_validate_participacion_invalida(diplomas_models): 
    participacion_invalida = 'ORGANIZACION'  # Una participación incorrecta
    with pytest.raises(ValueError, match="Participación no válida. Debe ser uno de: ORGANIZATION, INTERMEDIATE, ASSISTANCE."):
        diplomas_models.validate_participacion('participacion', participacion_invalida)

# Test para verificar comité válido
def test_validate_comite_valido(diplomas_models):
    comite_valido = 'Presidencia | Secretaría | Programa'

    with patch('app.modules.diplomas.models.Diploma.validate_comite') as mock_validate_comite:
        mock_validate_comite.return_value = comite_valido

        result = diplomas_models.validate_comite('comite', comite_valido)
        assert result == comite_valido

# Test para verificar comité inválido
def test_validate_comite_invalido(diplomas_models):
    comite_invalido = 'Presidencia | Seguridad'  # "Seguridad" no es válido

    with pytest.raises(ValueError, match="Comité no válido."):
        diplomas_models.validate_comite('comite', comite_invalido)

def test_from_excel_row(diplomas_models):
    row={
        "Apellidos": "García",
        "Nombre": "Juan",
        "Uvus": "jgarcia",
        "Correo": "juanGarcia@gamil.com", 
        "Perfil": "https://www.evidentia.cloud/2024/profiles/view/1",
        "Participación": "ORGANIZATION",
        "Comité": "Presidencia | Secretaría",
        "Evidencia aleatoria": 5.0,
        "Horas de evidencia aleatoria": 10.0,
        "Eventos asistidos": 2,
        "Horas de asistencia": 4.0,
        "Reuniones asistidas": 3,
        "Horas de reuniones": 6.0,
        "Bono de horas": 1.0,
        "Evidencias registradas": 4,
        "Horas de evidencias": 8.0,
        "Horas en total": 29.0
    }
    with patch('app.modules.diplomas.models.Diploma.from_excel_row') as mock_from_excel_row:
        mock_from_excel_row.return_value = row

        result = diplomas_models.from_excel_row(row)
        assert result == row

def test_from_excel_row_with_invalid_data(diplomas_models):
    row={
        "Apellidos": "García",
        "Nombre": "Juan",
        "Uvus": "jgarcia",
        "Correo": "",
        "Perfil": "https://www.evidentia.cloud/2024/profiles/view/1",
        "Participación": "ORGANIZATION",
        "Comité": "Presidencia | Secretaría",
        "Evidencia aleatoria": 5.0,
        "Horas de evidencia aleatoria": 10.0,
        "Eventos asistidos": 2,
        "Horas de asistencia": 4.0,
        "Reuniones asistidas": 3,
        "Horas de reuniones": 6.0,
        "Bono de horas": 1.0,
        "Evidencias registradas": 4,
        "Horas de evidencias": 8.0,
        "Horas en total": 29.0
    }
    with pytest.raises(ValueError, match="Correo no tiene un formato válido."):
        diplomas_models.from_excel_row(row)
        
        
# comprobando que no deja acceder a usuarios que no esten logueados
def test_generate_diplomas_route_unregistered_user(client):
    response = client.get('/diplomas')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']
    
def test_manage_template_route_unregistered_user(client):
    response = client.get('/manage-templates')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']
    
def test_diplomas_visualization_route_unregistered_user(client):
    response = client.get('/diplomas-visualization')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']
    
    
def test_view_diploma_route_unregistered_user(client):
    response = client.get('/view_diploma/1')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']
    
def test_delete_diploma_route_unregistered_user(client):
    response = client.post('/delete_diploma/1')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']
    
def test_send_diplomas_route_unregistered_user(client):
    response = client.post('/send_diplomas')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']
    
def test_view_template_route_unregistered_user(client):
    response = client.get('/view_template/1')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_delete_template_route_unregistered_user(client):
    response = client.post('/delete_template/1')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']
    
def test_delete_selected_diplomas_route_unregistered_user(client):
    response = client.post('/delete_selected_diplomas')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']
    
    
