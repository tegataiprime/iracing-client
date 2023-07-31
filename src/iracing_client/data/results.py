"""
    A wrapper around the iRacing Results Entity.
    
    Refer to https://members-ng.iracing.com/data/doc for more information.

    Functions:
    - get
    - event_log
    - lap_chart_data
    - lap_data
    - search_hosted
    - search_official
    - season_results

    "results": {
    "get": {
      "link": "https://members-ng.iracing.com/data/results/get",
      "note": "Get the results of a subsession, if authorized to view them. series_logo image paths are relative to https://images-static.iracing.com/img/logos/series/",
      "parameters": {
        "subsession_id": {
          "type": "number",
          "required": true
        },
        "include_licenses": {
          "type": "boolean"
        }
      },
      "expirationSeconds": 900
    },
    "event_log": {
      "link": "https://members-ng.iracing.com/data/results/event_log",
      "parameters": {
        "subsession_id": {
          "type": "number",
          "required": true
        },
        "simsession_number": {
          "type": "number",
          "required": true,
          "note": "The main event is 0; the preceding event is -1, and so on."
        }
      },
      "expirationSeconds": 900
    },
    "lap_chart_data": {
      "link": "https://members-ng.iracing.com/data/results/lap_chart_data",
      "parameters": {
        "subsession_id": {
          "type": "number",
          "required": true
        },
        "simsession_number": {
          "type": "number",
          "required": true,
          "note": "The main event is 0; the preceding event is -1, and so on."
        }
      },
      "expirationSeconds": 900
    },
    "lap_data": {
      "link": "https://members-ng.iracing.com/data/results/lap_data",
      "parameters": {
        "subsession_id": {
          "type": "number",
          "required": true
        },
        "simsession_number": {
          "type": "number",
          "required": true,
          "note": "The main event is 0; the preceding event is -1, and so on."
        },
        "cust_id": {
          "type": "number",
          "note": "Required if the subsession was a single-driver event. Optional for team events. If omitted for a team event then the laps driven by all the team's drivers will be included."
        },
        "team_id": {
          "type": "number",
          "note": "Required if the subsession was a team event."
        }
      },
      "expirationSeconds": 900
    },
    "search_hosted": {
      "link": "https://members-ng.iracing.com/data/results/search_hosted",
      "note": "Hosted and league sessions.  Maximum time frame of 90 days. Results split into one or more files with chunks of results. For scraping results the most effective approach is to keep track of the maximum end_time found during a search then make the subsequent call using that date/time as the finish_range_begin and skip any subsessions that are duplicated.  Results are ordered by subsessionid which is a proxy for start time. Requires one of: start_range_begin, finish_range_begin. Requires one of: cust_id, team_id, host_cust_id, session_name.",
      "parameters": {
        "start_range_begin": {
          "type": "string",
          "note": "Session start times. ISO-8601 UTC time zero offset: \"2022-04-01T15:45Z\"."
        },
        "start_range_end": {
          "type": "string",
          "note": "ISO-8601 UTC time zero offset: \"2022-04-01T15:45Z\". Exclusive. May be omitted if start_range_begin is less than 90 days in the past."
        },
        "finish_range_begin": {
          "type": "string",
          "note": "Session finish times. ISO-8601 UTC time zero offset: \"2022-04-01T15:45Z\"."
        },
        "finish_range_end": {
          "type": "string",
          "note": "ISO-8601 UTC time zero offset: \"2022-04-01T15:45Z\". Exclusive. May be omitted if finish_range_begin is less than 90 days in the past."
        },
        "cust_id": {
          "type": "number",
          "note": "The participant's customer ID. Ignored if team_id is supplied."
        },
        "team_id": {
          "type": "number",
          "note": "The team ID to search for. Takes priority over cust_id if both are supplied."
        },
        "host_cust_id": {
          "type": "number",
          "note": "The host's customer ID."
        },
        "session_name": {
          "type": "string",
          "note": "Part or all of the session's name."
        },
        "league_id": {
          "type": "number",
          "note": "Include only results for the league with this ID."
        },
        "league_season_id": {
          "type": "number",
          "note": "Include only results for the league season with this ID."
        },
        "car_id": {
          "type": "number",
          "note": "One of the cars used by the session."
        },
        "track_id": {
          "type": "number",
          "note": "The ID of the track used by the session."
        },
        "category_ids": {
          "type": "numbers",
          "note": "Track categories to include in the search.  Defaults to all. ?category_ids=1,2,3,4"
        }
      },
      "expirationSeconds": 900
    },
    "search_series": {
      "link": "https://members-ng.iracing.com/data/results/search_series",
      "note": "Official series.  Maximum time frame of 90 days. Results split into one or more files with chunks of results. For scraping results the most effective approach is to keep track of the maximum end_time found during a search then make the subsequent call using that date/time as the finish_range_begin and skip any subsessions that are duplicated.  Results are ordered by subsessionid which is a proxy for start time but groups together multiple splits of a series when multiple series launch sessions at the same time. Requires at least one of: season_year and season_quarter, start_range_begin, finish_range_begin.",
      "parameters": {
        "season_year": {
          "type": "number",
          "note": "Required when using season_quarter."
        },
        "season_quarter": {
          "type": "number",
          "note": "Required when using season_year."
        },
        "start_range_begin": {
          "type": "string",
          "note": "Session start times. ISO-8601 UTC time zero offset: \"2022-04-01T15:45Z\"."
        },
        "start_range_end": {
          "type": "string",
          "note": "ISO-8601 UTC time zero offset: \"2022-04-01T15:45Z\". Exclusive. May be omitted if start_range_begin is less than 90 days in the past."
        },
        "finish_range_begin": {
          "type": "string",
          "note": "Session finish times. ISO-8601 UTC time zero offset: \"2022-04-01T15:45Z\"."
        },
        "finish_range_end": {
          "type": "string",
          "note": "ISO-8601 UTC time zero offset: \"2022-04-01T15:45Z\". Exclusive. May be omitted if finish_range_begin is less than 90 days in the past."
        },
        "cust_id": {
          "type": "number",
          "note": "Include only sessions in which this customer participated. Ignored if team_id is supplied."
        },
        "team_id": {
          "type": "number",
          "note": "Include only sessions in which this team participated. Takes priority over cust_id if both are supplied."
        },
        "series_id": {
          "type": "number",
          "note": "Include only sessions for series with this ID."
        },
        "race_week_num": {
          "type": "number",
          "note": "Include only sessions with this race week number."
        },
        "official_only": {
          "type": "boolean",
          "note": "If true, include only sessions earning championship points. Defaults to all."
        },
        "event_types": {
          "type": "numbers",
          "note": "Types of events to include in the search. Defaults to all. ?event_types=2,3,4,5"
        },
        "category_ids": {
          "type": "numbers",
          "note": "License categories to include in the search.  Defaults to all. ?category_ids=1,2,3,4"
        }
      },
      "expirationSeconds": 900
    },
    "season_results": {
      "link": "https://members-ng.iracing.com/data/results/season_results",
      "parameters": {
        "season_id": {
          "type": "number",
          "required": true
        },
        "event_type": {
          "type": "number",
          "note": "Restrict to one event type: 2 - Practice; 3 - Qualify; 4 - Time Trial; 5 - Race"
        },
        "race_week_num": {
          "type": "number",
          "note": "The first race week of a season is 0."
        }
      },
      "expirationSeconds": 900
    }
  }
"""  # pylint: disable=line-too-long
import requests
from iracing_client.data import common
from iracing_client.data.common import IRacingDataObject

RESULTS_URL = common.BASE_URL + "/results/get"
EVENT_LOG_URL = common.BASE_URL + "/results/event_log"
LAP_CHART_DATA_URL = common.BASE_URL + "/results/lap_chart_data"
LAP_DATA_URL = common.BASE_URL + "/results/lap_data"
SEARCH_HOSTED_URL = common.BASE_URL + "/results/search_hosted"
SEARCH_SERIES_URL = common.BASE_URL + "/results/search_series"
SEASON_RESULTS_URL = common.BASE_URL + "/results/season_results"


class Results(IRacingDataObject):
    """iRacing Results Data Class"""

    def __init__(self, http_session: requests.Session):
        super().__init__("member", http_session)

    def get_result(self, subsession_id: int, include_licenses: bool = False):
        """
        Get the results of a subsession, if authorized to view them.
        series_logo image paths are relative to https://images-static.iracing.com/img/logos/series/

        Args:
            subsession_id (int): iRacing subsession
            include_licenses (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: dict
        """  # pylint: disable=line-too-long
        params = {"subsession_id": subsession_id, "include_licenses": include_licenses}
        request = requests.Request("GET", RESULTS_URL, params=params)
        return self.send(request).json()

    def get_event_log(self, subsession_id: int, simsession_number: int):
        """
        iRacing Event Log for a given subsession & simsession

        Args:
            subsession_id (int): iRacing subsession
            simsession_number (int): The main event is 0; the preceding event is -1, and so on.

        Returns:
            _type_: dict
        """  # pylint: disable=line-too-long
        params = {
            "subsession_id": subsession_id,
            "simsession_number": simsession_number,
        }
        request = requests.Request("GET", EVENT_LOG_URL, params=params)
        return self.send(request).json()

    def get_lap_chart_data(
        self,
        subsession_id: int,
        simsession_number: int,
        cust_id: int = None,
        team_id: int = None,
    ):
        """
        iRacing Lap Chart Data for a given subsession & simsession

        Args:
            subsession_id (int): iRacing subsession
            simsession_number (int): The main event is 0; the preceding event is -1, and so on.
            cust_id (int, optional): Required if the subsession was a single-driver event. Optional for team events. If omitted for a team event then the laps driven by all the team's drivers will be included. Defaults to None.
            team_id (int, optional): Required if the subsession was a team event. Defaults to None.

        Returns:
            _type_: dict
        """  # pylint: disable=line-too-long
        params = {
            "subsession_id": subsession_id,
            "simsession_number": simsession_number,
        }
        if cust_id:
            params["cust_id"] = cust_id
        if team_id:
            params["team_id"] = team_id
        request = requests.Request("GET", LAP_CHART_DATA_URL, params=params)
        return self.send(request).json()

    def search_hosted(
        self,
        start_range_begin: str = None,
        start_range_end: str = None,
        finish_range_begin: str = None,
        finish_range_end: str = None,
        cust_id: int = None,
        team_id: int = None,
        host_cust_id: int = None,
        session_name: str = None,
        league_id: int = None,
        league_season_id: int = None,
        car_id: int = None,
        track_id: int = None,
        category_ids: list = None,
    ):
        """
        Hosted and league sessions.
        Maximum time frame of 90 days.
        Results split into one or more files with chunks of results.
        For scraping results the most effective approach is to keep track of the maximum end_time found during a search then make the subsequent call using that date/time as the finish_range_begin and skip any subsessions that are duplicated.
        Results are ordered by subsessionid which is a proxy for start time.
        Requires one of: start_range_begin, finish_range_begin.
        Requires one of: cust_id, team_id, host_cust_id, session_name.

        Args:
            start_range_begin (str, optional): Session start times. ISO-8601 UTC time zero offset. Defaults to None.
            start_range_end (str, optional): ISO-8601 UTC time zero offset: \"2022-04-01T15:45Z\". Exclusive. May be omitted if start_range_begin is less than 90 days in the past. Defaults to None.
            finish_range_begin (str, optional): Session finish times. ISO-8601 UTC time zero offset: \"2022-04-01T15:45Z\". Defaults to None.
            finish_range_end (str, optional): ISO-8601 UTC time zero offset: \"2022-04-01T15:45Z\". Exclusive. May be omitted if finish_range_begin is less than 90 days in the past. Defaults to None.
            cust_id (int, optional): The participant's customer ID. Ignored if team_id is supplied. Defaults to None.
            team_id (int, optional): The team ID to search for. Takes priority over cust_id if both are supplied. Defaults to None.
            host_cust_id (int, optional): The host's customer ID. Defaults to None.
            session_name (str, optional): Part or all of the session's name. Defaults to None.
            league_id (int, optional): Include only results for the league with this ID. Defaults to None.
            league_season_id (int, optional): Include only results for the league season with this ID. Defaults to None.
            car_id (int, optional): One of the cars used by the session. Defaults to None.
            track_id (int, optional): The ID of the track used by the session. Defaults to None.
            category_ids (list, optional): Track categories to include in the search.  Defaults to all. ?category_ids=1,2,3,4. Defaults to None.
        """  # pylint: disable=line-too-long
        params = {}
        if start_range_begin:
            params["start_range_begin"] = start_range_begin
        if start_range_end:
            params["start_range_end"] = start_range_end
        if finish_range_begin:
            params["finish_range_begin"] = finish_range_begin
        if finish_range_end:
            params["finish_range_end"] = finish_range_end
        if cust_id:
            params["cust_id"] = cust_id
        if team_id:
            params["team_id"] = team_id
        if host_cust_id:
            params["host_cust_id"] = host_cust_id
        if session_name:
            params["session_name"] = session_name
        if league_id:
            params["league_id"] = league_id
        if league_season_id:
            params["league_season_id"] = league_season_id
        if car_id:
            params["car_id"] = car_id
        if track_id:
            params["track_id"] = track_id
        if category_ids:
            # Convert category_ids to a comma-separated string.
            str_category_ids = ",".join(
                str(category_id) for category_id in category_ids
            )
            params["category_ids"] = str_category_ids
        request = requests.Request("GET", SEARCH_HOSTED_URL, params=params)
        return self.send(request).json()

    def search_series(
        self,
        season_year: int = None,
        season_quarter: int = None,
        start_range_begin: str = None,
        start_range_end: str = None,
        finish_range_begin: str = None,
        finish_range_end: str = None,
        cust_id: int = None,
        team_id: int = None,
        series_id: int = None,
        race_week_num: int = None,
        official_only: bool = None,
        event_types: list = None,
        category_ids: list = None,
    ):
        """
        Official series.
        Maximum time frame of 90 days.
        Results split into one or more files with chunks of results.
        For scraping results the most effective approach is to keep track of the maximum end_time found during a search then make the subsequent call using that date/time as the finish_range_begin and skip any subsessions that are duplicated.
        Results are ordered by subsessionid which is a proxy for start time but groups together multiple splits of a series when multiple series launch sessions at the same time. Requires at least one of: season_year and season_quarter, start_range_begin, finish_range_begin.

        Args:
            season_year (int, optional): Required when using season_quarter. Defaults to None.
            season_quarter (int, optional): Required when using season_year. Defaults to None.
            start_range_begin (str, optional): Session start times. ISO-8601 UTC time zero offset: \"2022-04-01T15:45Z\". Defaults to None.
            start_range_end (str, optional): ISO-8601 UTC time zero offset: \"2022-04-01T15:45Z\". Exclusive. May be omitted if start_range_begin is less than 90 days in the past. Defaults to None.
            finish_range_begin (str, optional): Session finish times. ISO-8601 UTC time zero offset: \"2022-04-01T15:45Z\". Defaults to None.
            finish_range_end (str, optional): _description_. Defaults to None.
            cust_id (int, optional): ISO-8601 UTC time zero offset: \"2022-04-01T15:45Z\". Exclusive. May be omitted if finish_range_begin is less than 90 days in the past. Defaults to None.
            team_id (int, optional): Include only sessions in which this customer participated. Ignored if team_id is supplied. Defaults to None.
            series_id (int, optional): Include only sessions in which this team participated. Takes priority over cust_id if both are supplied. Defaults to None.
            race_week_num (int, optional): Include only sessions for series with this ID. Defaults to None.
            official_only (bool, optional): Include only sessions with this race week number. Defaults to None.
            event_types (list, optional): If true, include only sessions earning championship points. Defaults to all. Defaults to None.
            category_ids (list, optional): Types of events to include in the search. Defaults to all. ?event_types=2,3,4,5. Defaults to None.
        """
        params = {}
        if season_year:
            params["season_year"] = season_year
        if season_quarter:
            params["season_quarter"] = season_quarter
        if start_range_begin:
            params["start_range_begin"] = start_range_begin
        if start_range_end:
            params["start_range_end"] = start_range_end
        if finish_range_begin:
            params["finish_range_begin"] = finish_range_begin
        if finish_range_end:
            params["finish_range_end"] = finish_range_end
        if cust_id:
            params["cust_id"] = cust_id
        if team_id:
            params["team_id"] = team_id
        if series_id:
            params["series_id"] = series_id
        if race_week_num:
            params["race_week_num"] = race_week_num
        if official_only:
            params["official_only"] = official_only
        if event_types:
            # Convert event_types to a comma-separated string.
            str_event_types = ",".join(str(event_type) for event_type in event_types)
            params["event_types"] = str_event_types
        if category_ids:
            # Convert category_ids to a comma-separated string.
            str_category_ids = ",".join(
                str(category_id) for category_id in category_ids
            )
            params["category_ids"] = str_category_ids
        request = requests.Request("GET", SEARCH_SERIES_URL, params=params)
        return self.send(request).json()

    def get_season_results(
        self, season_id: int, event_type: int = None, race_week_num: int = None
    ):
        """Fetch Results for a Season

        Args:
            season_id (int): iRacing Season ID
            event_type (int, optional): Restrict to one event type: 2 - Practice; 3 - Qualify; 4 - Time Trial; 5 - Race. Defaults to None.
            race_week_num (int, optional): The first race week of a season is 0. Defaults to None.
        """
        params = {"season_id": season_id}
        if event_type:
            params["event_type"] = event_type
        if race_week_num:
            params["race_week_num"] = race_week_num
        request = requests.Request("GET", SEASON_RESULTS_URL, params=params)
        return self.send(request).json()
