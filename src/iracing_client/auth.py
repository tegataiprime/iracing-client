"""
iRacing Web API Authentication
------------------------------

Authentication uses the iRacing OAuth 2.0 service.

To obtain OAuth credentials (client_id and client_secret), register an application
through the iRacing developer portal.

Credential Encoding
-------------------
Both the account password and the OAuth client secret are encoded before submission
using the same method:

    - Convert the "username" (email or client_id) to lowercase
    - Concatenate the lowercase username to the end of the credential (password or client_secret)
    - Create a SHA256 hash of the combined string
    - Base64-encode the digest

Example:

    import hashlib
    import base64

    def encode_pw(username, password):
        initial_hash = hashlib.sha256(
            (password + username.lower()).encode('utf-8')
        ).digest()
        return base64.b64encode(initial_hash).decode('utf-8')

The same function is used to encode the client_secret, substituting client_id
for username.

OAuth 2.0 Token Request
-----------------------
POST https://oauth.iracing.com/oauth2/token

    Content-Type: application/x-www-form-urlencoded

    Form fields: username, password (encoded), grant_type=password_limited,
    client_id, client_secret (encoded), scope=iracing.auth

A successful response contains an ``access_token`` which is attached to the
``requests.Session`` as an ``Authorization: Bearer`` header for all subsequent
API calls.
""" # pylint: disable=line-too-long
import hashlib
import base64
import requests


class AuthenticationException(Exception):
    """Raised when login fails."""


OAUTH_URL = "https://oauth.iracing.com/oauth2/token"


def login(
    username: str, password: str, client_id: str, client_secret: str
) -> requests.Session:
    """Login to iRacing via OAuth 2.0 and return an authenticated requests.Session.

    Args:
        username (str): iRacing account email address.
        password (str): iRacing account password (plain text; encoded internally).
        client_id (str): OAuth application client ID issued by iRacing.
        client_secret (str): OAuth application client secret (plain text; encoded internally).

    Returns:
        requests.Session: A session with the ****** set in its Authorization header.

    Raises:
        AuthenticationException: If login fails for any reason.
    """
    credential_hash = encode_pw(username, password)
    client_secret_hash = encode_pw(client_id, client_secret)

    payload = {
        "username": username,
        "password": credential_hash,
        "grant_type": "password_limited",
        "client_id": client_id,
        "client_secret": client_secret_hash,
        "scope": "iracing.auth",
    }

    http_session = requests.Session()

    try:
        response = http_session.post(OAUTH_URL, data=payload, timeout=10.0)
    except requests.Timeout as timeout:
        raise AuthenticationException("Login timed out") from timeout
    except requests.ConnectionError as connection_error:
        raise AuthenticationException(
            "Login failed due to connection error"
        ) from connection_error

    if response.status_code == requests.codes.ok:  # pylint: disable=no-member
        token_data = response.json()
        access_token = token_data.get("access_token")
        if access_token:
            http_session.headers.update({"Authorization": f"Bearer {access_token}"})
            return http_session

    raise AuthenticationException(
        f"Login failed with status code {response.status_code}"
    )


def encode_pw(username: str, password: str) -> str:
    """Encode a credential to iRacing's specification.

    Used for both the account password (with email as username) and the OAuth
    client secret (with client_id as username).
    """
    initial_hash = hashlib.sha256((password + username.lower()).encode("utf-8")).digest()
    hash_in_base64 = base64.b64encode(initial_hash).decode("utf-8")
    return hash_in_base64
