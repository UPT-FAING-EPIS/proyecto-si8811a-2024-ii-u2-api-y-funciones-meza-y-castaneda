import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
from unittest.mock import patch, Mock
from auth.google import google_login, google_authorized
    
# Mocks
mock_config = Mock()
mock_config.CLIENT_ID = 'test_client_id'
mock_config.CLIENT_SECRET = 'test_client_secret'
mock_config.AUTHORITY = 'https://test_authority.com'
mock_config.SCOPE = ["User.Read"]

@patch('app.auth.google.ConfidentialClientApplication')
def test_google_login(mock_app):
    with app.app_context():
        # Configurar mock de la aplicación de cliente confidencial para la URL de autorización
        mock_app.return_value.get_authorization_request_url.return_value = "https://test_auth_url.com"
        
        # Ejecutar la función de login de Google
        result = google_login()
        
        # Asegurarse de que la URL de autorización sea la esperada
        assert "https://test_auth_url.com" in result.location

@patch('app.auth.google.ConfidentialClientApplication')
def test_google_authorized(mock_app):
    with app.app_context():
        # Configuración de las credenciales y el scope
        mock_app_instance = mock_app.return_value
        mock_app_instance.acquire_token_by_authorization_code.return_value = {
            "access_token": "test_access_token",
            "id_token_claims": {
                "preferred_username": "test@example.com",
                "name": "Test User",
                "roles": ["user"]
            }
        }
        
        # Mock de la creación de JWT
        with patch('app.auth.google.create_jwt') as mock_create_jwt:
            mock_create_jwt.return_value = "test_jwt_token"
            
            # Ejecutar la función de autorización de Google
            result = google_authorized()
            
            # Validaciones para el usuario autenticado
            assert "Hola, Test User!" in result.data.decode()
            assert "Roles: user" in result.data.decode()

        # Caso donde no hay roles asignados
        mock_app_instance.acquire_token_by_authorization_code.return_value["id_token_claims"]["roles"] = []
        
        # Ejecutar la función de autorización de Google nuevamente con roles vacíos
        result = google_authorized()
        
        # Validar que se maneja adecuadamente la falta de roles
        assert "Roles: user" in result.data.decode()

        # Caso donde la respuesta es incorrecta (usuario no autorizado)
        mock_app_instance.acquire_token_by_authorization_code.return_value = None
        
        # Ejecutar la función de autorización de Google con respuesta None
        result = google_authorized()
        
        # Validar manejo de error
        assert "Error en la autorización" in result.data.decode()
