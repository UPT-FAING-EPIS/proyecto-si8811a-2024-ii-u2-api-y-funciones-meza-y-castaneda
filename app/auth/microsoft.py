import requests
from msal import ConfidentialClientApplication
from flask import redirect, request, url_for
from config import Config
from utils.jwt_utils import create_jwt
from utils.device_utils import is_mobile

app_msal = ConfidentialClientApplication(
    Config.CLIENT_ID,
    authority=Config.AUTHORITY,
    client_credential=Config.CLIENT_SECRET,
)

def microsoft_login():
    auth_url = app_msal.get_authorization_request_url(
        Config.SCOPE,
        redirect_uri=url_for("microsoft_authorized_route", _external=True)
    )
    return redirect(auth_url)

def microsoft_authorized():
    code = request.args.get('code')
    if not code:
        return "Error al obtener el código de autorización", 400

    result = app_msal.acquire_token_by_authorization_code(
        code,
        scopes=Config.SCOPE,
        redirect_uri=url_for("microsoft_authorized_route", _external=True)
    )

    if "access_token" in result:
        user_info = result.get('id_token_claims')
        email = user_info.get("preferred_username")
        name = user_info.get("name")
        roles = result.get('id_token_claims', {}).get('roles', [])

        if not roles:
            roles = ["user"]
        elif "admin" not in roles:
            roles.append("user")

        token = create_jwt(email, name, roles)

        if is_mobile(request.headers.get('User-Agent', '')):
            return f"Hola, {name}! Roles: {', '.join(roles)}"

        redirect_url = f"http://161.132.50.153/?token={token}"
        return redirect(redirect_url)

    return "Error al obtener el token de acceso", 400
