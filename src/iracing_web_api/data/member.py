""" 
A wrapper around the iRacing Member Entity API.

Perform a lookup for a member by cust_id or get a list of members by
provding a list of cust_ids.  Note:  cust_ids must be integers.

Properties for the current authenticated user are lazily fetched and cached the
first time a property is accessed.  To refresh the data, call the clear_cache() function
and then access the property again.

Refer to https://members-ng.iracing.com/data/doc for more information.
"""
import requests
from iracing_web_api.data.constants import Category, ChartType
import iracing_web_api.data.common as common
from iracing_web_api.data.common import iRacingDataObject

MEMBER_URL = common.BASE_URL + 'member/get'
AWARDS_URL = common.BASE_URL + 'member/awards'
CHART_DATA_URL = common.BASE_URL + 'member/chart_data'
MY_INFO_URL = common.BASE_URL + 'member/info'
MY_PARTICIPATION_CREDITS_URL = common.BASE_URL + 'member/participation_credits'
PROFILE_URL = common.BASE_URL + 'member/profile'

class Member(iRacingDataObject):
    """iRacing Member Data Classes."""

    def __init__(self, http_session: requests.Session):
        super().__init__('member', http_session)


    def clear_cache(self):
        """Clear the cached data."""
        self._my_info = None
        self._my_participation_credits = None



    def get_member(self, cust_id: int) -> dict:
        """Return a dict of member data."""
        request = requests.Request('GET', MEMBER_URL, params={'cust_ids': cust_id})
        return self.send(request).json()
    

    def get_members(self, cust_ids: list) -> dict:
        """Return a dict of member data for multiple members."""
        if not all(isinstance(cust_id, int) for cust_id in cust_ids):
            raise TypeError('cust_ids must contain only integers.')
        # Convert cust_ids to a comma-separated string.
        str_cust_ids = ','.join(str(cust_id) for cust_id in cust_ids)
        request = requests.Request('GET', MEMBER_URL, params={'cust_ids': str_cust_ids})
        return self.send(request).json()


    def get_awards(self, cust_id: int = 0) -> list:
        """Return a list of awards for the cust_id specified, 
        or default to the current authenticated user."""
        
        params = {}
        if cust_id != 0:
            params['cust_id'] = cust_id

        request = requests.Request('GET', AWARDS_URL, params=params)
        return self.send(request).json()
        

    def get_chart_data(
            self, 
            category: Category,
            chart_type: ChartType,
            cust_id: int = 0
            ) -> dict:
        """Return a dict of chart data for the current user.
        category_id is mandatory and must be a valid Category enum.
        chart_type is mandatory and must be a valid ChartType enum.
        cust_id is optional and must be an integer.
        """
    
        params = {'category_id': category.value, 'chart_type': chart_type.value}
        if cust_id != 0:
            params['cust_id'] = cust_id

        request = requests.Request('GET', CHART_DATA_URL, params=params)
        return self.send(request).json()
        
    
    @property
    def my_info(self) -> dict:
        """Return a dict of info for the current user."""
        if self._my_info is None:
            request = requests.Request('GET', MY_INFO_URL)
            self._my_info = self.send(request).json()
        return self._my_info
    
    @property
    def my_participation_credits(self) -> list:
        """Return a dict of participation credits for the current user."""
        if self._my_participation_credits is None:
            request = requests.Request('GET', MY_PARTICIPATION_CREDITS_URL)
            self._my_participation_credits = self.send(request).json()
        return self._my_participation_credits
    

    def get_profile(self, cust_id: int = 0) -> dict:
        """Return a dict of profile data for the specifued cust_id 
        or the authenticated user."""
    
        params = {}
        if cust_id != 0:
            params['cust_id'] = cust_id

        request = requests.Request('GET', PROFILE_URL, params=params)
        return self.send(request).json()
