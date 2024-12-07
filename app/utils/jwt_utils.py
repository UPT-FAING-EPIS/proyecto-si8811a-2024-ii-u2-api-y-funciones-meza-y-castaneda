import jwt
import datetime
from config import Config

def create_jwt(email, name, roles):
    payload = {
        'sub': email,
        'name': name,
        'roles': roles,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")
    return token
