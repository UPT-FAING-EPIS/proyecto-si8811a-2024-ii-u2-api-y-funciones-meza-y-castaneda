import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
from app.auth.microsoft import microsoft_login, microsoft_authorized
from unittest.mock import patch, Mock

# Mocks
mock_config = Mock()
mock_config.CLIENT_ID = 'test_client_id'
mock_config.CLIENT_SECRET = 'test_client_secret'
mock_config.AUTHORITY = 'https://test_authority.com'
mock_config.SCOPE = ["User.Read"]

@patch('app.auth.microsoft.ConfidentialClientApplication')
def test_microsoft_login(mock_app):
    mock_app.return_value.get_authorization_request_url.return_value = "https://test_auth_url.com"
    result = microsoft_login()
    assert "https://test_auth_url.com" in result.location

@patch('app.auth.microsoft.ConfidentialClientApplication.acquire_token_by_authorization_code')
@patch('app.auth.microsoft.Config')
def test_microsoft_authorized(mock_config):
    mock_config.return_value.SCOPE = ["User.Read"]
    mock_app = Mock()
    mock_app.acquire_token_by_authorization_code.return_value = {
        "access_token": "test_access_token",
        "id_token_claims": {
            "preferred_username": "test@example.com",
            "name": "Test User",
            "roles": ["user"]
        }
    }
    with patch('app.auth.microsoft.create_jwt') as mock_create_jwt:
        mock_create_jwt.return_value = "test_jwt_token"
        result = microsoft_authorized()
        assert "Hola, Test User!" in result.data.decode()
        assert "Roles: user" in result.data.decode()

    # Case with no roles
    mock_app.acquire_token_by_authorization_code.return_value["id_token_claims"]["roles"] = []
    result = microsoft_authorized()
    assert "Roles: user" in result.data.decode()
