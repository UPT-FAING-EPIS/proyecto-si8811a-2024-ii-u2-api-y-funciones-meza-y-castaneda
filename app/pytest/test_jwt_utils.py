import pytest
from app.utils.jwt_utils import create_jwt
import jwt

# Mocks
mock_config = Mock()
mock_config.JWT_SECRET_KEY = 'test_secret_key'

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
