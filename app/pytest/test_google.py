import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
from unittest.mock import patch, Mock
from auth.google import google_login, google_authorized

# Mocks
mock_config = Mock()
mock_config.GOOGLE_CLIENT_ID = 'test_client_id'
mock_config.GOOGLE_CLIENT_SECRET = 'test_client_secret'
mock_config.GOOGLE_DISCOVERY_URL = 'https://test_url.com/.well-known/openid-configuration'

@patch('app.auth.google.requests.get')
def test_google_login(mock_get):
    mock_get.return_value.json.return_value = {
        "authorization_endpoint": "https://test_authorization.com"
    }
    
    result = google_login()
    
    assert mock_get.called
    assert result.location == "https://test_authorization.com"

@patch('app.auth.google.requests.get')
@patch('app.auth.google.requests.post')
def test_google_authorized(mock_post, mock_get):
    # Simula los datos de respuesta para las peticiones GET y POST
    mock_get.return_value.json.return_value = {
        "token_endpoint": "https://test_token.com",
        "userinfo_endpoint": "https://test_userinfo.com"
    }
    mock_post.return_value.json.return_value = {
        "access_token": "test_token",
        "id_token_claims": {
            "email_verified": True,
            "email": "test@example.com",
            "name": "Test User"
        }
    }
    
    with patch('app.auth.google.create_jwt') as mock_create_jwt:
        mock_create_jwt.return_value = "test_jwt_token"
        
        result = google_authorized()
        
        assert "Hola, Test User!" in result.data.decode()
        assert "Roles: user" in result.data.decode()

    # Caso donde el correo no está verificado
    mock_post.return_value.json.return_value["id_token_claims"]["email_verified"] = False
    result = google_authorized()
    assert "Error: No se pudo verificar el correo electrónico de Google." in result.data.decode()
