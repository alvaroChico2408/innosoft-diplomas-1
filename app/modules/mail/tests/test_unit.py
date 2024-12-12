import pytest
from unittest.mock import patch, MagicMock
from app.modules.mail.services import MailService


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