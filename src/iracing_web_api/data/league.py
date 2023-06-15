"""
A collection of classes related to iRacing League data.
Refer to https://members-ng.iracing.com/data/doc for more information.

  "league": {
    "cust_league_sessions": {
      "link": "https://members-ng.iracing.com/data/league/cust_league_sessions",
      "parameters": {
        "mine": {
          "type": "boolean",
          "note": "If true, return only sessions created by this user."
        },
        "package_id": {
          "type": "number",
          "note": "If set, return only sessions using this car or track package ID."
        }
      },
      "expirationSeconds": 900
    },
    "directory": {
      "link": "https://members-ng.iracing.com/data/league/directory",
      "parameters": {
        "search": {
          "type": "string",
          "note": "Will search against league name, description, owner, and league ID."
        },
        "tag": {
          "type": "string",
          "note": "One or more tags, comma-separated."
        },
        "restrict_to_member": {
          "type": "boolean",
          "note": "If true include only leagues for which customer is a member."
        },
        "restrict_to_recruiting": {
          "type": "boolean",
          "note": "If true include only leagues which are recruiting."
        },
        "restrict_to_friends": {
          "type": "boolean",
          "note": "If true include only leagues owned by a friend."
        },
        "restrict_to_watched": {
          "type": "boolean",
          "note": "If true include only leagues owned by a watched member."
        },
        "minimum_roster_count": {
          "type": "number",
          "note": "If set include leagues with at least this number of members."
        },
        "maximum_roster_count": {
          "type": "number",
          "note": "If set include leagues with no more than this number of members."
        },
        "lowerbound": {
          "type": "number",
          "note": "First row of results to return.  Defaults to 1."
        },
        "upperbound": {
          "type": "number",
          "note": "Last row of results to return. Defaults to lowerbound + 39."
        },
        "sort": {
          "type": "string",
          "note": "One of relevance, leaguename, displayname, rostercount. displayname is owners's name. Defaults to relevance."
        },
        "order": {
          "type": "string",
          "note": "One of asc or desc.  Defaults to asc."
        }
      },
      "expirationSeconds": 900
    },
    "get": {
      "link": "https://members-ng.iracing.com/data/league/get",
      "parameters": {
        "league_id": {
          "type": "number",
          "required": true
        },
        "include_licenses": {
          "type": "boolean",
          "note": "For faster responses, only request when necessary."
        }
      },
      "expirationSeconds": 900
    },
    "get_points_systems": {
      "link": "https://members-ng.iracing.com/data/league/get_points_systems",
      "parameters": {
        "league_id": {
          "type": "number",
          "required": true
        },
        "season_id": {
          "type": "number",
          "note": "If included and the season is using custom points (points_system_id:2) then the custom points option is included in the returned list. Otherwise the custom points option is not returned."
        }
      },
      "expirationSeconds": 900
    },
    "membership": {
      "link": "https://members-ng.iracing.com/data/league/membership",
      "parameters": {
        "cust_id": {
          "type": "number",
          "note": "If different from the authenticated member, the following resrictions apply: - Caller cannot be on requested customer's block list or an empty list will result; - Requested customer cannot have their online activity prefrence set to hidden or an empty list will result; - Only leagues for which the requested customer is an admin and the league roster is not private are returned."
        },
        "include_league": {
          "type": "boolean"
        }
      },
      "expirationSeconds": 900
    },
    "seasons": {
      "link": "https://members-ng.iracing.com/data/league/seasons",
      "parameters": {
        "league_id": {
          "type": "number",
          "required": true
        },
        "retired": {
          "type": "boolean",
          "note": "If true include seasons which are no longer active."
        }
      },
      "expirationSeconds": 900
    },
    "season_standings": {
      "link": "https://members-ng.iracing.com/data/league/season_standings",
      "parameters": {
        "league_id": {
          "type": "number",
          "required": true
        },
        "season_id": {
          "type": "number",
          "required": true
        },
        "car_class_id": {
          "type": "number"
        },
        "car_id": {
          "type": "number",
          "note": "If car_class_id is included then the standings are for the car in that car class, otherwise they are for the car across car classes."
        }
      },
      "expirationSeconds": 900
    },
    "season_sessions": {
      "link": "https://members-ng.iracing.com/data/league/season_sessions",
      "parameters": {
        "league_id": {
          "type": "number",
          "required": true
        },
        "season_id": {
          "type": "number",
          "required": true
        },
        "results_only": {
          "type": "boolean",
          "note": "If true include only sessions for which results are available."
        }
      },
      "expirationSeconds": 900
    }

"""
from abc import  abstractmethod
from enum import Enum
import requests
import iracing_web_api.data.common as common
from iracing_web_api.data.common import iRacingDataObject, iRacingRequestException

CUST_LEAGUE_SESSIONS_URL = common.BASE_URL + "league/cust_league_sessions"
DIRECTORY_URL = common.BASE_URL + "league/directory"
LEAGUE_URL = common.BASE_URL + "league/get"
GET_POINTS_SYSTEMS_URL = common.BASE_URL + "league/get_points_systems"
MEMBERSHIP_URL = common.BASE_URL + "league/membership"
SEASONS_URL = common.BASE_URL + "league/seasons"
SEASON_STANDINGS_URL = common.BASE_URL + "league/season_standings"
SEASON_SESSIONS_URL = common.BASE_URL + "league/season_sessions"

class LeagueSort(Enum):
    RELEVANCE = 'relevance'
    LEAGUENAME = 'leaguename'
    DISPLAYNAME = 'displayname'
    ROSTERCOUNT = 'rostercount'

class LeagueOrder(Enum):
    ASC = 'asc'
    DESC = 'desc'

class League(iRacingDataObject):
    """Functions for working with iRacing League Data. """
    def __init__(self, http_session: requests.Session):
        super().__init__('league', http_session)


    def clear_cache(self):
        """We have no cached data for this object. """
        pass


    def get_cust_league_sessions(
            self,
            mine: bool = False,
            package_id: int = None):
        """
        Customer League Sessions

        Parameters:
            mine:       If true, return only sessions created by this user.
            package_id: If set, return only sessions using this car or track package ID.
        """
        params = {}
        if mine:
            params['mine'] = mine
        if package_id:
            params['package_id'] = package_id
        request = requests.Request('GET', CUST_LEAGUE_SESSIONS_URL, params=params)
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
            sort: str = LeagueSort.RELEVANCE,
            order: str = LeagueOrder.ASC):
        """
        League Directory

        Parameters:
            search:                 Search string.
            tag:                    Tag string.
            restrict_to_member:     If true, return only leagues of which the authenticated user is a member.
            restrict_to_recruiting: If true, return only leagues which are recruiting.
            restrict_to_friends:    If true, return only leagues of which the authenticated user is a friend.
            restrict_to_watched:    If true, return only leagues which the authenticated user is watching.
            minimum_roster_count:   Minimum number of members in the league.
            maximum_roster_count:   Maximum number of members in the league.
            lowerbound:             First row of results to return. Defaults to 0.
            upperbound:             Last row of results to return. Defaults to lowerbound + 39.
            sort:                   One of relevance, leaguename, displayname, rostercount. displayname is owners's name. Defaults to relevance.
            order:                  One of asc or desc.  Defaults to asc.
        """
        params = {}
        if search:
            params['search'] = search
        if tag:
            params['tag'] = tag
        if restrict_to_member:
            params['restrict_to_member'] = restrict_to_member
        if restrict_to_recruiting:
            params['restrict_to_recruiting'] = restrict_to_recruiting
        if restrict_to_friends:
            params['restrict_to_friends'] = restrict_to_friends
        if restrict_to_watched:
            params['restrict_to_watched'] = restrict_to_watched
        if minimum_roster_count:
            params['minimum_roster_count'] = minimum_roster_count
        if maximum_roster_count:
            params['maximum_roster_count'] = maximum_roster_count
        if lowerbound:
            params['lowerbound'] = lowerbound
        if upperbound:
            params['upperbound'] = upperbound
        if sort:
            params['sort'] = sort
        if order:
            params['order'] = order
        request = requests.Request('GET', DIRECTORY_URL, params=params)
        return self.send(request).json()


    def get_league(self,
                   league_id: int,
                   include_licenses: bool = False):
        """
        Get League Data

        Parameters:
            league_id:          League ID.
            include_licenses:   If true, include licenses for each member.  For faster response, only request when necessary.
        """
        params = {'league_id': league_id}
        if include_licenses:
            params['include_licenses'] = include_licenses
        request = requests.Request('GET', LEAGUE_URL, params=params)
        return self.send(request).json()
    

    def get_points_systems(
            self,
            league_id: int,
            season_id: int = None):
        """
        Get Points Systems

        Parameters:
            league_id:  League ID.
            season_id:  Season ID. If included and the season is using custom points 
            (points_system_id:2) then the custom points option is included in the 
            returned list. Otherwise the custom points option is not returned. 
        """
        params = {'league_id': league_id}
        if season_id:
            params['season_id'] = season_id
        request = requests.Request('GET', GET_POINTS_SYSTEMS_URL, params=params)
        return self.send(request).json()

    def get_membership(
            self,
            cust_id: int = None,
            include_league: bool = False):
        """
        Get League Membership

        Parameters:
            cust_id:            Customer ID. Defaults to authenticated user.
            include_league:     If true, include league data.
        """ 
        params = {}
        if cust_id:
            params['custid'] = cust_id
        if include_league:
            params['include_league'] = include_league
        request = requests.Request('GET', MEMBERSHIP_URL, params=params)
        return self.send(request).json()
    

    def get_seasons(
            self,
            league_id: int,
            retired: bool = False):
        """
        Get League Sessions

        Parameters:
            league_id:  League ID.
            retired:    If true include seasons which are no longer active.
        """
        params = {'league_id': league_id}
        if retired:
            params['retired'] = retired
        request = requests.Request('GET', SEASONS_URL, params=params)
        return self.send(request).json()
    

    def get_season_standings(
            self,
            league_id: int,
            season_id: int,
            car_class_id: int = None,
            car_id: int = None):
        """
        Get Season Standings

        Parameters:
            league_id:      League ID.
            season_id:      Season ID.
            car_class_id:   Car Class ID. If included, return only standings for this car class.
            car_id:         Car ID. If included, return only standings for this car.
        """
        params = {
            'league_id': league_id,
            'season_id': season_id
        }
        if car_class_id:
            params['car_class_id'] = car_class_id
        if car_id:
            params['car_id'] = car_id
        request = requests.Request('GET', SEASON_STANDINGS_URL, params=params)
        return self.send(request).json()
    

    def get_season_sessions(
            self,
            league_id: int,
            season_id: int,
            results_only: bool = False):
        """
        Get Season Sessions

        Parameters:
            league_id:      League ID.
            season_id:      Season ID.
            results_only:   If true include only sessions for which results are available.
        """
        params = {
            'league_id': league_id,
            'season_id': season_id
        }
        if results_only:
            params['results_only'] = results_only
        request = requests.Request('GET', SEASON_SESSIONS_URL, params=params)
        return self.send(request).json()
    