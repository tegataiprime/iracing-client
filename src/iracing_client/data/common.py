"""Base classes for iRacing data objects."""
from abc import ABC, abstractmethod
import requests
from typing import List

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

    def collect_chunks(self, chunk_response: requests.Response) -> list:
        """Fetch each chunk of data and return the combined data.  Assumes a json response."""
        data = []
        response = chunk_response.json()
        if response["success"] and response["chunk_info"]["num_chunks"] > 0:
            base_download_url = response["chunk_info"]["base_download_url"]
            chunk_file_names = response["chunk_info"]["chunk_file_names"]
            for chunk_file_name in chunk_file_names:
                chunk_request = requests.Request(
                    "GET", f"{base_download_url}{chunk_file_name}"
                )
                response = self.follow_link(chunk_request)
                data.extend(response.json())
        return data
