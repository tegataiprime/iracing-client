"""Pytest configuration for integration tests."""
import pytest
import os
import iracing_web_api.auth as auth



@pytest.fixture(scope="session")
def iracing_username():
    """Return a username from an environment variable."""
    return os.environ.get('IRACING_USERNAME')

@pytest.fixture(scope="session")
def iracing_password():
    """Return a password from an environment variable."""
    return os.environ.get('IRACING_PASSWORD')

@pytest.fixture(scope="session")
def iracing_member_id():
    """Return a member id from an environment variable."""
    return os.environ.get('IRACING_MEMBER_ID')

@pytest.fixture(scope="session")
def http_session(iracing_username, iracing_password):
    """Return a cookiejar."""
    http_session = auth.login(iracing_username, iracing_password)
    return http_session