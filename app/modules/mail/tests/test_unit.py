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

def test_init_app(mail_service):
    app = MagicMock()
    app.config = {}
    mail_service.init_app(app)
    
    assert mail_service.mail is not None
    assert mail_service.sender is not None
    assert app.config['MAIL_SERVER'] == 'smtp.gmail.com'
    assert app.config['MAIL_PORT'] == 587
    assert app.config['MAIL_USE_TLS'] == True
    assert app.config['MAIL_USE_SSL'] == False
    assert app.config['MAIL_USERNAME'] == 'diplomasinnosoft2024@gmail.com'
    assert app.config['MAIL_PASSWORD'] == 'slav jfes qacm knls'
    assert app.config['MAIL_DEFAULT_SENDER'] == 'diplomasinnosoft2024@gmail.com'
    
