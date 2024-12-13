from msal import ConfidentialClientApplication

class MicrosoftAuth:
    def __init__(self, client_id, client_secret, authority, redirect_path, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.authority = authority
        self.redirect_path = redirect_path
        self.scope = scope
        self.app = ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )

    def get_auth_url(self, redirect_uri):
        return self.app.get_authorization_request_url(self.scope, redirect_uri=redirect_uri)

    def acquire_token(self, code, redirect_uri):
        return self.app.acquire_token_by_authorization_code(
            code, scopes=self.scope, redirect_uri=redirect_uri
        )
