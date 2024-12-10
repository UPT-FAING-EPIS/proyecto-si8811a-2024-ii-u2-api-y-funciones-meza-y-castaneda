# app/config.py
from dotenv import load_dotenv
load_dotenv()  # Esto carga las variables de entorno desde el archivo .env
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    AUTHORITY = os.getenv("AUTHORITY")
    REDIRECT_PATH = os.getenv("REDIRECT_PATH", "/getAToken")  # Asegúrate de que no sea None
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_DISCOVERY_URL = os.getenv("GOOGLE_DISCOVERY_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SCOPE = ["User.Read"]

