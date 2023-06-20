"""
A wrapper around the iRacing League Entity.

Refer to https://members-ng.iracing.com/data/doc for more information.
"""
from enum import Enum
import requests
from iracing_client.data import common
from iracing_client.data.common import IRacingDataObject

CUST_LEAGUE_SESSIONS_URL = common.BASE_URL + "league/cust_league_sessions"
DIRECTORY_URL = common.BASE_URL + "league/directory"
LEAGUE_URL = common.BASE_URL + "league/get"
GET_POINTS_SYSTEMS_URL = common.BASE_URL + "league/get_points_systems"
MEMBERSHIP_URL = common.BASE_URL + "league/membership"
SEASONS_URL = common.BASE_URL + "league/seasons"
SEASON_STANDINGS_URL = common.BASE_URL + "league/season_standings"
SEASON_SESSIONS_URL = common.BASE_URL + "league/season_sessions"


class LeagueSort(Enum):
    """An enumerated class representing iRacing League Sort Types."""

    RELEVANCE = "relevance"
    LEAGUENAME = "leaguename"
    DISPLAYNAME = "displayname"
    ROSTERCOUNT = "rostercount"


class LeagueOrder(Enum):
    """An enumerated class representing iRacing League Order Types."""

    ASC = "asc"
    DESC = "desc"


class League(IRacingDataObject):
    """Functions for working with iRacing League Data."""

    def __init__(self, http_session: requests.Session):
        super().__init__("league", http_session)

    def clear_cache(self):
        """We have no cached data for this object."""

    def get_cust_league_sessions(self, mine: bool = False, package_id: int = None):
        """League Sessions available to the authenticated user.

        Args:
            mine (bool, optional): If true, return only sessions created by this user. Defaults to False.
            package_id (int, optional): If set, return only sessions using this car or track package ID. Defaults to None.

        Returns:
            _type_: _description_
        """  # pylint: disable=line-too-long
        params = {}
        if mine:
            params["mine"] = mine
        if package_id:
            params["package_id"] = package_id
        request = requests.Request("GET", CUST_LEAGUE_SESSIONS_URL, params=params)
        return self.send(request).json()

    def get_directory(
        self,
        search: str = None,
        tag: str = None,
        restrict_to_member: bool = False,
        restrict_to_recruiting: bool = False,
        restrict_to_friends: bool = False,
        restrict_to_watched: bool = False,
        minimum_roster_count: int = None,
        maximum_roster_count: int = None,
        lowerbound: int = None,
        upperbound: int = None,
        sort: LeagueSort = LeagueSort.RELEVANCE,
        order: LeagueOrder = LeagueOrder.ASC,
    ): # pylint: disable=too-many-arguments
        """Lookup the directory of leagues.

        Args:
            search (str, optional): League Name Search String. Defaults to None.
            tag (str, optional): League Tags to include. Defaults to None.
            restrict_to_member (bool, optional): If true, return only leagues of which the authenticated user is a member. Defaults to False.
            restrict_to_recruiting (bool, optional): If true, return only leagues which are recruiting. Defaults to False.
            restrict_to_friends (bool, optional): If true, return only leagues of which the authenticated user is a friend. Defaults to False.
            restrict_to_watched (bool, optional): If true, return only leagues which the authenticated user is watching. Defaults to False.
            minimum_roster_count (int, optional): Minimum number of members in the league.
            maximum_roster_count (int, optional): Maximum number of members in the league.
            lowerbound (int, optional): First row of results to return. Defaults to 0.
            upperbound (int, optional): Last row of results to return. Defaults to lowerbound + 39.
            sort (LeagueSort, optional): _description_. One of relevance, leaguename, displayname, rostercount. displayname is owners's name. Defaults to relevance.
            order (LeagueOrder, optional): _description_. One of asc or desc.  Defaults to asc.

        Returns:
            _type_: iRacing Legue Directory Data, deserialized from JSON.
        """  # pylint: disable=line-too-long
        params = {}
        if search:
            params["search"] = search
        if tag:
            params["tag"] = tag
        if restrict_to_member:
            params["restrict_to_member"] = restrict_to_member
        if restrict_to_recruiting:
            params["restrict_to_recruiting"] = restrict_to_recruiting
        if restrict_to_friends:
            params["restrict_to_friends"] = restrict_to_friends
        if restrict_to_watched:
            params["restrict_to_watched"] = restrict_to_watched
        if minimum_roster_count:
            params["minimum_roster_count"] = minimum_roster_count
        if maximum_roster_count:
            params["maximum_roster_count"] = maximum_roster_count
        if lowerbound:
            params["lowerbound"] = lowerbound
        if upperbound:
            params["upperbound"] = upperbound
        if sort:
            params["sort"] = sort.value
        if order:
            params["order"] = order.value
        request = requests.Request("GET", DIRECTORY_URL, params=params)
        return self.send(request).json()

    def get_league(self, league_id: int, include_licenses: bool = False):
        """Fetches data for a specific league.

        Args:
            league_id (int): iRacing League ID.
            include_licenses (bool, optional): If true, include licenses for each member.  For faster response, only request when necessary. Defaults to False.

        Returns:
            _type_: iRacing League Data, deserialized from JSON.
        """  # pylint: disable=line-too-long
        params = {"league_id": league_id}
        if include_licenses:
            params["include_licenses"] = include_licenses
        request = requests.Request("GET", LEAGUE_URL, params=params)
        return self.send(request).json()

    def get_points_systems(self, league_id: int, season_id: int = None):
        """Return the points systems for a league.

        Args:
            league_id (int): iRacing League ID.
            season_id (int, optional): If included and the season is using custom points
            (points_system_id:2) then the custom points option is included in the
            returned list. Otherwise the custom points option is not returned. Defaults to None.

        Returns:
            _type_: iRacing League Points Systems Data, deserialized from JSON.
        """  # pylint: disable=line-too-long
        params = {"league_id": league_id}
        if season_id:
            params["season_id"] = season_id
        request = requests.Request("GET", GET_POINTS_SYSTEMS_URL, params=params)
        return self.send(request).json()

    def get_membership(self, cust_id: int = None, include_league: bool = False):
        """Fetch iRacing League Membership for a specific customer id.

        Args:
            cust_id (int, optional): iRacing Member ID. Defaults to authenticated user.
            include_league (bool, optional): If true, include league data. Defaults to False.

        Returns:
            _type_: _description_
        """  # pylint: disable=line-too-long
        params = {}
        if cust_id:
            params["custid"] = cust_id
        if include_league:
            params["include_league"] = include_league
        request = requests.Request("GET", MEMBERSHIP_URL, params=params)
        return self.send(request).json()

    def get_seasons(self, league_id: int, retired: bool = False):
        """Fetch Seasons for a specific league.

        Args:
            league_id (int): iRacing League ID.
            retired (bool, optional): If true include seasons which are no longer active. Defaults to False.

        Returns:
            _type_: _description_
        """  # pylint: disable=line-too-long
        params = {"league_id": league_id}
        if retired:
            params["retired"] = retired
        request = requests.Request("GET", SEASONS_URL, params=params)
        return self.send(request).json()

    def get_season_standings(
        self,
        league_id: int,
        season_id: int,
        car_class_id: int = None,
        car_id: int = None,
    ):
        """Get Season Standings for a specific league and season.

        Args:
            league_id (int): iRacing League Id
            season_id (int): Season Id within the league.
            car_class_id (int, optional): Car Class ID. If included, return only standings for this car class. Defaults to None.
            car_id (int, optional): Car ID. If included, return only standings for this car. Defaults to None.

        Returns:
            _type_: _description_
        """  # pylint: disable=line-too-long
        params = {"league_id": league_id, "season_id": season_id}
        if car_class_id:
            params["car_class_id"] = car_class_id
        if car_id:
            params["car_id"] = car_id
        request = requests.Request("GET", SEASON_STANDINGS_URL, params=params)
        return self.send(request).json()

    def get_season_sessions(
        self, league_id: int, season_id: int, results_only: bool = False
    ):
        """Get Season Sessions for a specific league and season.

        Args:
            league_id (int): iRacing League Id
            season_id (int): Season Id within the league.
            results_only (bool, optional): If true include only sessions for which results are available. Defaults to False.

        Returns:
            _type_: _description_
        """  # pylint: disable=line-too-long
        params = {"league_id": league_id, "season_id": season_id}
        if results_only:
            params["results_only"] = results_only
        request = requests.Request("GET", SEASON_SESSIONS_URL, params=params)
        return self.send(request).json()
