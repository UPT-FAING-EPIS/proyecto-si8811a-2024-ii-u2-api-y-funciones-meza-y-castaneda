from unittest.mock import patch
from app.auth.google import google_login, google_authorized

@patch("app.auth.google.requests.get")
@patch("app.auth.google.requests.post")
def test_google_login(mock_post, mock_get):
    # Mockear respuestas de las solicitudes HTTP
    mock_get.return_value.json.return_value = {
        "authorization_endpoint": "https://accounts.google.com/o/oauth2/auth"
    }

    response = google_login()

    assert response.status_code == 302  # Redirección
    assert "https://accounts.google.com/o/oauth2/auth" in response.location

@patch("app.auth.google.requests.get")
@patch("app.auth.google.requests.post")
def test_google_authorized(mock_post, mock_get):
    # Mockear respuestas de las solicitudes HTTP
    mock_get.return_value.json.side_effect = [
        {
            "token_endpoint": "https://oauth2.googleapis.com/token",
            "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo",
        },
        {"email_verified": True, "email": "test@example.com", "name": "Test User"},
    ]
    mock_post.return_value.text = '{"access_token": "mock_access_token"}'

    # Simular la solicitud Flask
    with app.test_request_context("/callback?code=mock_code"):
        response = google_authorized()

    assert response.status_code == 302  # Redirección
    assert "token=" in response.location
