import pytest
import sys
import os
from unittest.mock import patch, Mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
import jwt
from utils.jwt_utils import create_jwt

# Importa la instancia de la aplicación Flask
from app import app
from auth.google import google_login, google_authorized
from auth.microsoft import microsoft_login, microsoft_authorized

# Mocks
mock_config = Mock()
mock_config.JWT_SECRET_KEY = 'a9f52e4c6b8f3a90e8b21d63f0c26d79'

def test_create_jwt():
    email = "test@example.com"
    name = "Test User"
    roles = ["user"]

    token = create_jwt(email, name, roles)
    
    # Decode the token
    decoded_token = jwt.decode(token, mock_config.JWT_SECRET_KEY, algorithms=["HS256"])
    assert decoded_token['sub'] == email
    assert decoded_token['name'] == name
    assert decoded_token['roles'] == roles
    assert 'exp' in decoded_token

    # Expired token scenario
    expired_token = jwt.encode({
        'sub': email,
        'name': name,
        'roles': roles,
        'exp': 0  # Set to epoch time (0) to simulate an expired token
    }, mock_config.JWT_SECRET_KEY, algorithm="HS256")
    
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(expired_token, mock_config.JWT_SECRET_KEY, algorithms=["HS256"])

# Tests for Google authentication
@patch('auth.google.ConfidentialClientApplication')
def test_google_login(mock_app):
    with app.app_context():
        # Setup mock for ConfidentialClientApplication to return a test authorization URL
        mock_app.return_value.get_authorization_request_url.return_value = "https://test_auth_url.com"
        
        # Ejecuta la función de login de Google
        result = google_login()
        
        # Asegúrate de que la URL de autorización sea la esperada
        assert "https://test_auth_url.com" in result.location

@patch('auth.google.ConfidentialClientApplication')
def test_google_authorized(mock_app):
    with app.app_context():
        # Setup mock credentials and scope
        mock_app_instance = mock_app.return_value
        mock_app_instance.acquire_token_by_authorization_code.return_value = {
            "access_token": "test_access_token",
            "id_token_claims": {
                "preferred_username": "test@example.com",
                "name": "Test User",
                "roles": ["user"]
            }
        }
        
        # Mock JWT creation
        with patch('auth.google.create_jwt') as mock_create_jwt:
            mock_create_jwt.return_value = "test_jwt_token"
            
            # Ejecuta la función de Google authorized
            result = google_authorized()
            
            # Validaciones para el usuario autenticado
            assert "Hola, Test User!" in result.data.decode()
            assert "Roles: user" in result.data.decode()

        # Caso en que no se asignan roles
        mock_app_instance.acquire_token_by_authorization_code.return_value["id_token_claims"]["roles"] = []
        
        # Ejecuta la función de Google authorized de nuevo con sin roles
        result = google_authorized()
        
        # Validar que la falta de roles sea manejada adecuadamente
        assert "Roles: user" in result.data.decode()

# Tests for Microsoft authentication
@patch('auth.microsoft.ConfidentialClientApplication')
def test_microsoft_login(mock_app):
    with app.app_context():
        # Setup mock for ConfidentialClientApplication to return a test authorization URL
        mock_app.return_value.get_authorization_request_url.return_value = "https://test_auth_url.com"
        
        # Ejecuta la función de login de Microsoft
        result = microsoft_login()
        
        # Asegúrate de que la URL de autorización sea la esperada
        assert "https://test_auth_url.com" in result.location

@patch('auth.microsoft.ConfidentialClientApplication')
def test_microsoft_authorized(mock_app):
    with app.app_context():
        # Setup mock credentials and scope
        mock_app_instance = mock_app.return_value
        mock_app_instance.acquire_token_by_authorization_code.return_value = {
            "access_token": "test_access_token",
            "id_token_claims": {
                "preferred_username": "test@example.com",
                "name": "Test User",
                "roles": ["user"]
            }
        }
        
        # Mock JWT creation
        with patch('auth.microsoft.create_jwt') as mock_create_jwt:
            mock_create_jwt.return_value = "test_jwt_token"
            
            # Ejecuta la función de Microsoft authorized
            result = microsoft_authorized()
            
            # Validaciones para el usuario autenticado
            assert "Hola, Test User!" in result.data.decode()
            assert "Roles: user" in result.data.decode()

        # Caso en que no se asignan roles
        mock_app_instance.acquire_token_by_authorization_code.return_value["id_token_claims"]["roles"] = []
        
        # Ejecuta la función de Microsoft authorized de nuevo con sin roles
        result = microsoft_authorized()
        
        # Validar que la falta de roles sea manejada adecuadamente
        assert "Roles: user" in result.data.decode()
