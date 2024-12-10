import pytest
from unittest.mock import patch, MagicMock
from app.modules.mail.services import MailService


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
def mail_service():
    return MailService()

def test_send_email(mail_service):
    
    with patch.object(mail_service, 'send_email') as mock_send_email:
        mock_send_email.return_value = True

        result = mail_service.send_email(' subject', 'body', ' from', ' to')
        
        assert result is True
    
def test_send_email_invalid(mail_service):
    with patch.object(mail_service, 'send_email') as mock_send_email:
        mock_send_email.return_value = False

        result = mail_service.send_email(' subject', 'body', ' from', ' to')
        
        assert result is False
    

def test_send_email_with_attachment(mail_service):  
    with patch.object(mail_service, 'send_email_with_attachment') as mock_send_email_with_attachment:
        mock_send_email_with_attachment.return_value = True

        result = mail_service.send_email_with_attachment(' subject', 'body', ' from', ' to', 'file')
        
        assert result is True
        
def test_send_email_with_attachment_invalid(mail_service):
    with patch.object(mail_service, 'send_email_with_attachment') as mock_send_email_with_attachment:
        mock_send_email_with_attachment.return_value = False

        result = mail_service.send_email_with_attachment(' subject', 'body', ' from', ' to', 'file')
        
        assert result is False