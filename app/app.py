from flask import Flask, redirect, request, url_for, session
from auth.microsoft import microsoft_login, microsoft_authorized
from auth.google import google_login, google_authorized
from utils.jwt_utils import create_jwt
from utils.device_utils import is_mobile
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    return '''
        <h1>Bienvenido</h1>
        <p>Inicia sesión con:</p>
        <a href="/login">Microsoft</a><br>
        <a href="/google/login">Google</a>
    '''

@app.route('/login')
def login():
    return microsoft_login()

@app.route(Config.REDIRECT_PATH)
def microsoft_authorized_route():
    return microsoft_authorized()

@app.route('/google/login')
def google_login_route():
    return google_login()

@app.route('/google/authorized')
def google_authorized_route():
    return google_authorized()

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
