"""Test auth module."""
from requests import Session
import iracing_client.auth as auth


def test_login(iracing_username, iracing_password):
    """Test login function."""
    http_session = auth.login(iracing_username, iracing_password)
    assert http_session
    assert isinstance(http_session, Session)
    assert http_session.cookies
    assert http_session.cookies.get('authtoken_members')

def test_encode_pw():
    """Test encode_pw function."""
    assert auth.encode_pw('fred','password') == 'V1jLWG2/dbeTBtZzCrsMTyX0jDhiz8HPgblo5DQEi/4='
