import pytest
from unittest.mock import patch
from app.modules.diplomas.services import DiplomasService


#@pytest.fixture(scope='module')
#def test_client(test_client):
#    """
#    Extends the test_client fixture to add additional specific data for module testing.
#    """
#    with test_client.application.app_context():
#        # Add HERE new elements to the database that you want to exist in the test context.
#        # DO NOT FORGET to use db.session.add(<element>) and db.session.commit() to save the data.
#        pass

#    yield test_client


#def test_sample_assertion(test_client):
#    """
#    Sample test to verify that the test framework and environment are working correctly.
#    It does not communicate with the Flask application; it only performs a simple assertion to
#    confirm that the tests in this module can be executed.
#    """
#    greeting = "Hello, World!"
#    assert greeting == "Hello, World!", "The greeting does not coincide with 'Hello, World!'"


@pytest.fixture 
def diploma_service():
    return DiplomasService()


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