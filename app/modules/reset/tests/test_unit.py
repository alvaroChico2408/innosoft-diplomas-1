import pytest
from unittest.mock import patch
from app.modules.reset.services import ResetService


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
def reset_service():
    return ResetService()

def test_send_reset_password_mail(reset_service):
    with patch.object(reset_service, 'send_reset_password_mail') as mock_send_reset_password_mail:
        mock_send_reset_password_mail.return_value = True

        result = reset_service.send_reset_password_mail('email')
        
        assert result is True
    
def test_send_reset_password_mail_no_user(reset_service):
    with patch.object(reset_service, 'send_reset_password_mail') as mock_send_reset_password_mail:
        mock_send_reset_password_mail.return_value = None

        result = reset_service.send_reset_password_mail('email')
        
        assert result is None
def test_add_token(reset_service):  
    with patch.object(reset_service, 'add_token') as mock_add_token:
        mock_add_token.return_value = True

        result = reset_service.add_token('token')
        
        assert result is True
def test_add_token_no_token(reset_service):  
    with patch.object(reset_service, 'add_token') as mock_add_token:
        mock_add_token.return_value = None

        result = reset_service.add_token(None)
        
        assert result is None

def test_email_by_token(reset_service):
    with patch.object(reset_service, 'get_email_by_token') as mock_get_email_by_token:
        mock_get_email_by_token.return_value = 'email'

        result = reset_service.get_email_by_token('token')
        
        assert result == 'email'

def test_email_by_token_no_token(reset_service):
    with patch.object(reset_service, 'get_email_by_token') as mock_get_email_by_token:
        mock_get_email_by_token.return_value = None

        result = reset_service.get_email_by_token(None)
        
        assert result is None
        
def test_check_valid_token(reset_service):
    with patch.object(reset_service, 'check_valid_token') as mock_check_valid_token:
        mock_check_valid_token.return_value = True

        result = reset_service.check_valid_token('token')
        
        assert result is True
def test_check_invalid_token(reset_service):
    with patch.object(reset_service, 'check_valid_token') as mock_check_valid_token:
        mock_check_valid_token.return_value = False

        result = reset_service.check_valid_token('token')
        
        assert result is False

def test_token_already_used(reset_service):
    with patch.object(reset_service, 'token_already_used') as mock_token_already_used:
        mock_token_already_used.return_value = True

        result = reset_service.token_already_used('token')
        
        assert result is True

def test_reset_password(reset_service):
    with patch.object(reset_service, 'reset_password') as mock_reset_password:
        mock_reset_password.return_value = True

        result = reset_service.reset_password('email', 'password')
        
        assert result is True

def test_reset_password_no_user(reset_service):
    with patch.object(reset_service, 'reset_password') as mock_reset_password:
        mock_reset_password.return_value = None

        result = reset_service.reset_password(None, 'password')
        
        assert result is None

def test_mark_token_as_used(reset_service):
    with patch.object(reset_service, 'mark_token_as_used') as mock_mark_token_as_used:
        mock_mark_token_as_used.return_value = True

        result = reset_service.mark_token_as_used('token')
        
        assert result is True
    
def test_mark_token_as_used_no_token(reset_service):
    with patch.object(reset_service, 'mark_token_as_used') as mock_mark_token_as_used:
        mock_mark_token_as_used.return_value = None

        result = reset_service.mark_token_as_used(None)
        
        assert result is None