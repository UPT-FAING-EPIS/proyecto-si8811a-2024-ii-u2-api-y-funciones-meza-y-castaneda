import pytest
import sys
import os
from unittest.mock import Mock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
import jwt
from utils.jwt_utils import create_jwt

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
        'exp': 0
    }, mock_config.JWT_SECRET_KEY, algorithm="HS256")
    
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(expired_token, mock_config.JWT_SECRET_KEY, algorithms=["HS256"])
