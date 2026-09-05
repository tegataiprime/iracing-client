"""Unit tests for the auth module."""
from unittest.mock import MagicMock, patch
import pytest
import requests
import iracing_client.auth as auth


def test_encode_pw_basic():
    """Test encode_pw produces the expected hash."""
    assert auth.encode_pw("fred", "password") == "V1jLWG2/dbeTBtZzCrsMTyX0jDhiz8HPgblo5DQEi/4="


def test_encode_pw_case_insensitive():
    """encode_pw lowercases the username before hashing."""
    assert auth.encode_pw("FRED", "password") == auth.encode_pw("fred", "password")


def test_login_success():
    """login() attaches a ****** to session headers on success."""
    token = "test-token-123"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"access_token": token}

    with patch("requests.Session.post", return_value=mock_response):
        session = auth.login("user@example.com", "password", "client_id", "client_secret")

    assert isinstance(session, requests.Session)
    auth_header = session.headers.get("Authorization", "")
    assert auth_header.startswith("Bearer ")
    assert token in auth_header


def test_login_no_access_token_raises():
    """login() raises AuthenticationException when response has no access_token."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}

    with patch("requests.Session.post", return_value=mock_response):
        with pytest.raises(auth.AuthenticationException):
            auth.login("user@example.com", "password", "client_id", "client_secret")


def test_login_bad_status_raises():
    """login() raises AuthenticationException on non-200 response."""
    mock_response = MagicMock()
    mock_response.status_code = 401

    with patch("requests.Session.post", return_value=mock_response):
        with pytest.raises(auth.AuthenticationException) as exc_info:
            auth.login("user@example.com", "password", "client_id", "client_secret")

    assert "401" in str(exc_info.value)


def test_login_timeout_raises():
    """login() raises AuthenticationException on timeout."""
    with patch("requests.Session.post", side_effect=requests.Timeout):
        with pytest.raises(auth.AuthenticationException, match="timed out"):
            auth.login("user@example.com", "password", "client_id", "client_secret")


def test_login_connection_error_raises():
    """login() raises AuthenticationException on connection error."""
    with patch("requests.Session.post", side_effect=requests.ConnectionError):
        with pytest.raises(auth.AuthenticationException, match="connection error"):
            auth.login("user@example.com", "password", "client_id", "client_secret")


def test_login_payload_uses_oauth_grant_type():
    """login() sends the password_limited grant_type to the OAuth URL."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"access_token": "tok"}

    with patch("requests.Session.post", return_value=mock_response) as mock_post:
        auth.login("user@example.com", "password", "client_id", "client_secret")

    call_kwargs = mock_post.call_args
    sent_data = call_kwargs[1].get("data", {})
    assert sent_data.get("grant_type") == "password_limited"
    assert sent_data.get("scope") == "iracing.auth"
    assert sent_data.get("username") == "user@example.com"


def test_login_posts_to_oauth_url():
    """login() posts to the configured OAUTH_URL."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"access_token": "tok"}

    with patch("requests.Session.post", return_value=mock_response) as mock_post:
        auth.login("user@example.com", "password", "client_id", "client_secret")

    called_url = mock_post.call_args[0][0]
    assert called_url == auth.OAUTH_URL
