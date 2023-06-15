import pytest
import os
import iracing_web_api.auth as auth
import iracing_web_api.trace as trace


# Enable logging for the requests module
trace.httpclient_logging_patch()


@pytest.fixture(scope="session")
def iracing_username():
    """Return a username from an environment variable."""
    return os.environ.get('IRACING_USERNAME')

@pytest.fixture(scope="session")
def iracing_password():
    """Return a password from an environment variable."""
    return os.environ.get('IRACING_PASSWORD')

@pytest.fixture(scope="session")
def http_session(iracing_username, iracing_password):
    """Return a cookiejar."""
    http_session = auth.login(iracing_username, iracing_password)
    return http_session