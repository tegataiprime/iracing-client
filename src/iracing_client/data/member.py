""" 
A wrapper around the iRacing Member Entity.

Perform a lookup for a member by cust_id or get a list of members by
provding a list of cust_ids.  Note:  cust_ids must be integers.

Properties for the current authenticated user are lazily fetched and cached the
first time a property is accessed.  To refresh the data, call the clear_cache() function
and then access the property again.

Refer to https://members-ng.iracing.com/data/doc for more information.
""" # pylint: disable=line-too-long
import requests
from iracing_client.data.constants import Category, ChartType
from iracing_client.data import common
from iracing_client.data.common import IRacingDataObject

MEMBER_URL = common.BASE_URL + "member/get"
AWARDS_URL = common.BASE_URL + "member/awards"
CHART_DATA_URL = common.BASE_URL + "member/chart_data"
MY_INFO_URL = common.BASE_URL + "member/info"
MY_PARTICIPATION_CREDITS_URL = common.BASE_URL + "member/participation_credits"
PROFILE_URL = common.BASE_URL + "member/profile"


class Member(IRacingDataObject):
    """iRacing Member Data Classes."""

    def __init__(self, http_session: requests.Session):
        super().__init__("member", http_session)
        self._my_info = None
        self._my_participation_credits = None

    def clear_cache(self):
        """Clear the cached data."""
        self._my_info = None
        self._my_participation_credits = None

    def get_member(self, cust_id: int) -> dict:
        """Fetch member data for the cust_id specified.

        Args:
            cust_id (int): iRacing Member Id

        Returns:
            dict: iRacing Member Data, deserialized from JSON.
        """
        request = requests.Request("GET", MEMBER_URL, params={"cust_ids": cust_id})
        return self.send(request).json()

    def get_members(self, cust_ids: list) -> dict:
        """Fetch member data for the cust_ids specified.

        Args:
            cust_ids (list): A list of cust_ids, as integers.

        Raises:
            TypeError: If cust_ids contains anything other than integers.

        Returns:
            dict: iRacing Member Data, deserialized from JSON.
        """
        if not all(isinstance(cust_id, int) for cust_id in cust_ids):
            raise TypeError("cust_ids must contain only integers.")
        # Convert cust_ids to a comma-separated string.
        str_cust_ids = ",".join(str(cust_id) for cust_id in cust_ids)
        request = requests.Request("GET", MEMBER_URL, params={"cust_ids": str_cust_ids})
        return self.send(request).json()

    def get_awards(self, cust_id: int = None) -> list:
        """iRacing Member Awards.

        Args:
            cust_id (int, optional): iRacing Member Id. Defaults to authenticated user.

        Returns:
            list: iRacing Member Awards, deserialized from JSON.
        """
        params = {}
        if cust_id:
            params["cust_id"] = cust_id
        request = requests.Request("GET", AWARDS_URL, params=params)
        return self.send(request).json()

    def get_chart_data(
        self, category: Category, chart_type: ChartType, cust_id: int = None
    ) -> dict:
        """iRacing Member Chart Data.

        Args:
            category (Category): An enumeration of Oval, Road, DirtOval, or DirtRoad
            chart_type (ChartType): An enumeration of iRating, Time Trial Rating, or Safety Rating
            cust_id (int, optional): iRacing Member Id. Defaults to authenticaed user.

        Returns:
            dict: iRacing Member Chart Data, deserialized from JSON.
        """
        params = {"category_id": category.value, "chart_type": chart_type.value}
        if cust_id:
            params["cust_id"] = cust_id
        request = requests.Request("GET", CHART_DATA_URL, params=params)
        return self.send(request).json()

    @property
    def my_info(self) -> dict:
        """iRacing Member Info for the authenticated user.
        Data is cached the first time this property is accessed.
        Use clear_cache() to refresh the data.

        Returns:
            dict: iRacing Member Info, deserialized from JSON.
        """
        if self._my_info is None:
            request = requests.Request("GET", MY_INFO_URL)
            self._my_info = self.send(request).json()
        return self._my_info

    @property
    def my_participation_credits(self) -> list:
        """iRacing Member Participation Credits for the authenticated user.
        Note: May be empty if the user has no participation credits.
        Data is cached the first time this property is accessed.
        Use clear_cache() to refresh the data.

        Returns:
            list: iRacing Member Participation Credits, deserialized from JSON.
        """
        if self._my_participation_credits is None:
            request = requests.Request("GET", MY_PARTICIPATION_CREDITS_URL)
            self._my_participation_credits = self.send(request).json()
        return self._my_participation_credits

    def get_profile(self, cust_id: int = None) -> dict:
        """iRacing Member Profile.

        Args:
            cust_id (int, optional): iRacing Member Id. Defaults to authenticated user.

        Returns:
            dict: iRacing Member Profile, deserialized from JSON.
        """
        params = {}
        if cust_id:
            params["cust_id"] = cust_id
        request = requests.Request("GET", PROFILE_URL, params=params)
        return self.send(request).json()
