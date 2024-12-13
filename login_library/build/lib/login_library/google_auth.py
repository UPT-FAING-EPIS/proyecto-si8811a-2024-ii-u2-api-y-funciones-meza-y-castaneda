import requests
from oauthlib.oauth2 import WebApplicationClient

class GoogleAuth:
    def __init__(self, client_id, client_secret, discovery_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.discovery_url = discovery_url
        self.client = WebApplicationClient(client_id)

    def get_auth_url(self, redirect_uri, scope=["openid", "email", "profile"]):
        provider_cfg = requests.get(self.discovery_url).json()
        authorization_endpoint = provider_cfg["authorization_endpoint"]
        return self.client.prepare_request_uri(authorization_endpoint, redirect_uri=redirect_uri, scope=scope)

    def get_user_info(self, code, redirect_uri):
        provider_cfg = requests.get(self.discovery_url).json()
        token_endpoint = provider_cfg["token_endpoint"]

        token_url, headers, body = self.client.prepare_token_request(
            token_endpoint, authorization_response=redirect_uri, redirect_url=redirect_uri, code=code
        )
        token_response = requests.post(token_url, headers=headers, data=body, auth=(self.client_id, self.client_secret))
        self.client.parse_request_body_response(token_response.text)

        userinfo_endpoint = provider_cfg["userinfo_endpoint"]
        uri, headers, body = self.client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        if userinfo_response.json().get("email_verified"):
            return userinfo_response.json()
        return None
