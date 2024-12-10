import jwt
import datetime
from config import Config

def create_jwt(email, name, roles):
    # Verificar que los parámetros requeridos no sean None
    if not email or not name or not roles:
        raise ValueError("Email, name, and roles are required to create JWT")

    # Payload del JWT
    payload = {
        'sub': email,
        'name': name,
        'roles': roles,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")
    return token
    
