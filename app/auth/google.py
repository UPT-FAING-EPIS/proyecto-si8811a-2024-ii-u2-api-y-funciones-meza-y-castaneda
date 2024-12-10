import requests
from oauthlib.oauth2 import WebApplicationClient
from flask import redirect, request, url_for
from config import Config
from utils.jwt_utils import create_jwt
from utils.device_utils import is_mobile

google_client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)

def google_login():
    google_provider_cfg = requests.get(Config.GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = google_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=url_for("google_authorized_route", _external=True),
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

def google_authorized():
    code = request.args.get("code")
    google_provider_cfg = requests.get(Config.GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = google_client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=url_for("google_authorized_route", _external=True),
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(Config.GOOGLE_CLIENT_ID, Config.GOOGLE_CLIENT_SECRET),
    )

    google_client.parse_request_body_response(token_response.text)

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = google_client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        email = userinfo_response.json()["email"]
        name = userinfo_response.json()["name"]
        roles = ["user"]

        token = create_jwt(email, name, roles)

        if is_mobile(request.headers.get('User-Agent', '')):
            return f"Hola, {name}! Roles: {', '.join(roles)}"

        redirect_url = f"http://161.132.50.153/?token={token}"
        return redirect(redirect_url)

    return "Error: No se pudo verificar el correo electrónico de Google.", 400
