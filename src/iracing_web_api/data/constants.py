"""
iRacing Constants:
    categories:           a list of iRacing categories
    divisions:            a list of iRacing divisions
    event_types:          a list of iRacing event types

Refer to https://members-ng.iracing.com/data/doc for more information.
"""
import requests
from enum import Enum
import iracing_web_api.data.common as common
from iracing_web_api.data.common import iRacingDataObject

# URLs for iRacing Constants.
CATEGORIES_URL = common.BASE_URL + 'constants/categories'
DIVISIONS_URL = common.BASE_URL + 'constants/divisions'
EVENT_TYPES_URL = common.BASE_URL + 'constants/event_types'


class Category(Enum):
    """An enumerated class representing iRacing Categories."""
    OVAL = 1
    ROAD = 2
    DIRT_OVAL = 3
    DIRT_ROAD = 4


class ChartType(Enum):
    """An enumerated class representing iRacing Chart Types."""
    IRATING = 1
    TT_RACING = 2
    LICENSE_SR = 3


class Constants(iRacingDataObject):
    """A class representing iRacing Constants."""


    #Prepare requests for iRacing Constants.
    _categories_request = requests.Request('GET', CATEGORIES_URL)
    _divisions_request = requests.Request('GET', DIVISIONS_URL)
    _event_types_request = requests.Request('GET', EVENT_TYPES_URL)


    def __init__(self, http_session: requests.Session):
        """Initialize the Constants class."""
        super().__init__('constants', http_session) 


    def clear_cache(self):
        """Clear the cached data."""
        self._categories = None
        self._divisions = None
        self._event_types = None

    @property
    def categories(self) -> list:
        """
        Return a list of iRacing categories.
        Categories will be fetched and cached as an instance attribute.
        """
        if self._categories is None:
            self._categories = self.send(self._categories_request).json()
        return self._categories

    @property
    def divisions(self) -> list:
        """
        Return a list of iRacing divisions.
        Divisions will be fetched and cached as an instance attribute.
        """
        if self._divisions is None:
            self._divisions = self.send(self._divisions_request).json()
        return self._divisions

    @property
    def event_types(self) -> list:
        """
        Return a list of iRacing event types.
        Event types will be fetched and cached as an instance attribute.
        """
        if self._event_types is None:
            self._event_types = self.send(self._event_types_request).json()
        return self._event_types