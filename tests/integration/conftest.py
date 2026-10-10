"""Pytest configuration for integration tests."""
import pytest
import os
import iracing_client.auth as auth


@pytest.fixture(scope="session")
def iracing_username():
    """Return a username from an environment variable."""
    return os.environ.get('IRACING_USERNAME')

@pytest.fixture(scope="session")
def iracing_password():
    """Return a password from an environment variable."""
    return os.environ.get('IRACING_PASSWORD')

@pytest.fixture(scope="session")
def iracing_client_id():
    """Return the OAuth client_id from an environment variable."""
    return os.environ.get('IRACING_CLIENT_ID')

@pytest.fixture(scope="session")
def iracing_client_secret():
    """Return the OAuth client_secret from an environment variable."""
    return os.environ.get('IRACING_CLIENT_SECRET')

@pytest.fixture(scope="session")
def iracing_member_id():
    """Return a member id from an environment variable."""
    iracing_member_id = os.environ.get('IRACING_MEMBER_ID')
    # Convert iracing_member_id to an int
    try:
        iracing_member_id = int(iracing_member_id)
    except ValueError:
        raise ValueError("IRACING_MEMBER_ID must be an integer.")
    else:
        return iracing_member_id

@pytest.fixture(scope="session")
def http_session(iracing_username, iracing_password, iracing_client_id, iracing_client_secret):
    """Return an authenticated requests.Session."""
    http_session = auth.login(iracing_username, iracing_password, iracing_client_id, iracing_client_secret)
    return http_session