"""
A wrapper around the iRacing Constants Entity.

Refer to https://members-ng.iracing.com/data/doc for more information.
"""
from enum import Enum
import requests
from iracing_client.data import common
from iracing_client.data.common import IRacingDataObject

# URLs for iRacing Constants.
CATEGORIES_URL = common.BASE_URL + "constants/categories"
DIVISIONS_URL = common.BASE_URL + "constants/divisions"
EVENT_TYPES_URL = common.BASE_URL + "constants/event_types"


class Category(Enum):
    """An enumerated class representing iRacing Categories."""

    OVAL = 1
    ROAD = 2
    DIRT_OVAL = 3
    DIRT_ROAD = 4


class ChartType(Enum):
    """An enumerated class representing iRacing Chart Types."""

    IRATING = 1
    TT_RATING = 2
    LICENSE_SR = 3


class Constants(IRacingDataObject):
    """A class representing iRacing Constants."""

    # Prepare requests for iRacing Constants.
    _categories_request = requests.Request("GET", CATEGORIES_URL)
    _divisions_request = requests.Request("GET", DIVISIONS_URL)
    _event_types_request = requests.Request("GET", EVENT_TYPES_URL)

    def __init__(self, http_session: requests.Session):
        """Initialize the Constants class."""
        super().__init__("constants", http_session)
        self._categories = None
        self._divisions = None
        self._event_types = None

    def clear_cache(self):
        """Clear the cached data."""
        self._categories = None
        self._divisions = None
        self._event_types = None

    @property
    def categories(self) -> list:
        """iRacing Categories.
        Data is cached the first time this property is accessed.
        Use clear_cache() to refresh the data.

        Returns:
            list: iRacing Categories, deserialized from JSON.
        """
        if self._categories is None:
            self._categories = self.send(self._categories_request).json()
        return self._categories

    @property
    def divisions(self) -> list:
        """iRacing Divisions.
        Data is cached the first time this property is accessed.
        Use clear_cache() to refresh the data.

        Returns:
            list: iRacing Divisions, deserialized from JSON.
        """
        if self._divisions is None:
            self._divisions = self.send(self._divisions_request).json()
        return self._divisions

    @property
    def event_types(self) -> list:
        """iRacing Event Types.
        Data is cached the first time this property is accessed.
        Use clear_cache() to refresh the data.

        Returns:
            list: iRacing Event Types, deserialized from JSON.
        """
        if self._event_types is None:
            self._event_types = self.send(self._event_types_request).json()
        return self._event_types
