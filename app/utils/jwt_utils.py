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

    # Convertir JWT_SECRET_KEY a string si no lo es ya
    secret_key = str(Config.JWT_SECRET_KEY)
    
    # Codificar el JWT
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token
