"""Base classes for iRacing data objects."""
from abc import ABC, abstractmethod
import requests

BASE_URL = "https://members-ng.iracing.com/data/"

REQUEST_TIMEOUT = 10.0


class IRacingRequestException(Exception):
    """Raised when an iRacing request fails."""


class IRacingDataObject(ABC):
    """An abstract base class for iRacing data objects."""

    def __init__(self, name: str, http_session: requests.Session):
        self.name = name
        self.http_session = http_session
        self.clear_cache()

    @abstractmethod
    def clear_cache(self):
        """Clear the cached data."""

    def get_http_session(self) -> requests.Session:
        """Return the iRacing session."""
        return self.http_session

    def prepare_request(self, request: requests.Request) -> requests.PreparedRequest:
        """Prepare a request."""
        return self.http_session.prepare_request(request)

    def send(self, request: requests.Request) -> requests.Response:
        """Prepare & Execute a request using the current http session."""
        try:
            prepared_request = self.prepare_request(request)
            response = self.http_session.send(prepared_request, timeout=REQUEST_TIMEOUT)
        except requests.Timeout as timeout:
            raise IRacingRequestException(f"{self.name} timed out") from timeout
        except requests.ConnectionError as conection_error:
            raise IRacingRequestException(
                f"{self.name} failed due to connection error"
            ) from conection_error

        if (
            response.status_code == requests.codes.ok  # pylint: disable=no-member
            and response.cookies["authtoken_members"]
        ):
            data = response.json()
            if isinstance(data, dict) and data["link"]:
                link_request = requests.Request("GET", data["link"])
                return self.follow_link(link_request)
            return response

        raise IRacingRequestException(
            f"{self.name} failed with status code {response.status_code}"
        )

    def follow_link(self, link_request: requests.Request) -> requests.Response:
        """Follow the link to the data that we requested."""
        try:
            prepared_request = self.prepare_request(link_request)
            response = self.http_session.send(prepared_request, timeout=REQUEST_TIMEOUT)
        except requests.Timeout as timeout:
            raise IRacingRequestException(f"{self.name} timed out") from timeout
        except requests.ConnectionError as conection_error:
            raise IRacingRequestException(
                f"{self.name} failed due to connection error"
            ) from conection_error

        if response.status_code == requests.codes.ok:  # pylint: disable=no-member
            return response

        raise IRacingRequestException(
            f"{self.name} failed with status code {response.status_code}"
        )
