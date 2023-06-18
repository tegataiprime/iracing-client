"""
Taken from iRacing Web API Documentation: 
https://forums.iracing.com/discussion/15068/general-availability-of-data-api/p1

iRacing Web API Authentication
------------------------------

In order to access the API, you will need to authenticate. This can be 
accomplished by making a single POST request to https://members-ng.iracing.com/auth 
with the email (username) and password fields in the body. 

The value for the PW field is derived using the method described below.

    Submitting Login Credentials
    ----------------------------
    With the Season 3 release, currently planned for the week of June 6th,
    we will be changing how the various /Login and https://members-ng.iracing.com/auth 
    endpoints expect user credentials to be submitted. 
    This will affect any 3rd party applications which authenticate with the website, including /data. 
    The current login endpoints submit the password in plain text over HTTPS (encrypted in transit).

    With the Season 3 release, these endpoints will begin sending the password as a Base64 encoded string 
    (still transmitted via HTTPS) using the following steps.

    - Convert the username (email) to lowercase
    - Concatenate the output from step 1 to the end of the password
    - Create a SHA256 hash of the output from step 2
    - Encode the output from step 3 in Base64
    - Submit the output from step 4 in the password field of the login form
    
    Additional Details:
    This change is a requirement for the new OAuth 2.0 service that is in the works. 
    While this new method does not improve the security of the password (since it is already 
    encrypted in transit) this does ensure that the plain text version of the password is 
    never transmitted off of the device which is authenticating.

    Finally, for the avoidance of doubt, the hashed value that is submitted in the password
    poetyfield is not the value stored in the database for the password.

    Example Python Code
    -------------------
    import hashlib
    import base64

    username = 'CLunky@iracing.Com'
    password = 'MyPassWord'

    def encode_pw(username, password):
        initialHash = hashlib.sha256((password + username.lower()).encode('utf-8')).digest()
        hashInBase64 = base64.b64encode(initialHash).decode('utf-8')
        return hashInBase64

    pwValueToSubmit = encode_pw(username, password)
    print(f'{username}\n{pwValueToSubmit}')


A sample curl script is shown below.

    EMAIL="john.smith@iracing.com"
    PASSWORD="SuperSecure123"

    EMAILLOWER=$(echo -n "$EMAIL" | tr [:upper:] [:lower:])
    ENCODEDPW=$(echo -n $PASSWORD$EMAILLOWER | openssl dgst -binary -sha256 | openssl base64)

    BODY="{\"email\": \"$EMAIL\", \"password\": \"$ENCODEDPW\"}"

    /usr/bin/curl -c cookie-jar.txt -X POST -H 'Content-Type: application/json' --data "$BODY" https://members-ng.iracing.com/auth

The cookie-jar.txt stores the cookies, including the authtoken set during login. You may continue to use the cookie-jar.txt on each 
subsequent request without needing to re-auth and the authtoken will be automatically refreshed as needed. 
Please do not re-auth with each request. We see that on a number of the current scrapers hitting the membersite.
""" # pylint: disable=line-too-long
import hashlib
import base64
import requests


class AuthenticationException(Exception):
    """Raised when login fails."""


AUTH_URL = "https://members-ng.iracing.com/auth"


def login(username: str, password: str) -> requests.Session:
    """Login to iRacing and return a requests.Session object."""
    credential_hash = encode_pw(username, password)
    payload = {"email": username, "password": credential_hash}
    http_session = requests.Session()
    try:
        response = http_session.post(AUTH_URL, json=payload, timeout=10.0)
    except requests.Timeout as timeout:
        raise AuthenticationException("Login timed out") from timeout
    except requests.ConnectionError as connection_error:
        raise AuthenticationException("Login failed due to connection error") from connection_error

    if response.status_code == requests.codes.ok: # pylint: disable=no-member
        return http_session

    raise AuthenticationException(
        f"Login failed with status code {response.status_code}"
    )


def encode_pw(username: str, password: str) -> str:
    """Encode the password to iRacing's specification."""
    initial_hash = hashlib.sha256((password + username.lower()).encode("utf-8")).digest()
    hash_in_base64 = base64.b64encode(initial_hash).decode("utf-8")
    return hash_in_base64
