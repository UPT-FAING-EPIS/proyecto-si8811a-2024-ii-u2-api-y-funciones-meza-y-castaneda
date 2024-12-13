import jwt
import datetime

class JWTUtils:
    def __init__(self, secret_key="default_secret_key"):
        self.secret_key = secret_key

    def create_jwt(self, email, name, roles):
        payload = {
            'sub': email,
            'name': name,
            'roles': roles,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
