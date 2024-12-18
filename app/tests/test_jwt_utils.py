import pytest
from unittest.mock import patch, MagicMock
import jwt
from utils.jwt_utils import create_jwt

# Importa la instancia de la aplicación Flask
from app import app
from auth.google import google_login
from auth.microsoft import microsoft_login
from config import Config

@patch.object(Config, 'JWT_SECRET_KEY', 'a9f52e4c6b8f3a90e8b21d63f0c26d79')
def test_create_jwt():
    email = "test@example.com"
    name = "Test User"
    roles = ["user"]

    token = create_jwt(email, name, roles)

    # Decode the token
    decoded_token = jwt.decode(token, "a9f52e4c6b8f3a90e8b21d63f0c26d79", algorithms=["HS256"])
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
    }, "a9f52e4c6b8f3a90e8b21d63f0c26d79", algorithm="HS256")

    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(expired_token, "a9f52e4c6b8f3a90e8b21d63f0c26d79", algorithms=["HS256"])

# Tests for Google authentication
@patch('auth.google.ConfidentialClientApplication')
def test_google_login_basic(mock_app):
    # Setup mock for ConfidentialClientApplication
    mock_instance = MagicMock()
    mock_instance.get_authorization_request_url.return_value = "https://test_auth_url.com"
    mock_app.return_value = mock_instance

    with app.app_context():
        # Ejecuta la función de login de Google
        result = google_login()

        # Asegúrate de que la URL de autorización sea la esperada
        assert "https://test_auth_url.com" in result.location

# Tests for Microsoft authentication
@patch('auth.microsoft.ConfidentialClientApplication')
def test_microsoft_login_basic(mock_app):
    # Setup mock for ConfidentialClientApplication
    mock_instance = MagicMock()
    mock_instance.get_authorization_request_url.return_value = "https://test_auth_url.com"
    mock_app.return_value = mock_instance

    with app.app_context():
        # Ejecuta la función de login de Microsoft
        result = microsoft_login()

        # Asegúrate de que la URL de autorización sea la esperada
        assert "https://test_auth_url.com" in result.location