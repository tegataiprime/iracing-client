"""Test auth module."""
import iracing_client.auth as auth
from requests import Session


def test_encode_pw():
    """Test encode_pw function."""
    assert auth.encode_pw('fred', 'password') == 'V1jLWG2/dbeTBtZzCrsMTyX0jDhiz8HPgblo5DQEi/4='


def test_login(iracing_username, iracing_password, iracing_client_id, iracing_client_secret):
    """Test login function."""
    http_session = auth.login(iracing_username, iracing_password, iracing_client_id, iracing_client_secret)
    assert http_session
    assert isinstance(http_session, Session)
    assert 'Authorization' in http_session.headers
    assert http_session.headers['Authorization'].startswith('Bearer ')
