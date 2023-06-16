"""Test League Module."""
import pytest
from iracing_web_api.data.league import League

@pytest.fixture(scope="module")
def league_instance(http_session):
    """Return a League object."""
    return League(http_session)

def test_get_cust_league_sessions(league_instance):
    """Test get_cust_league_sessions function."""
    league_data = league_instance.get_cust_league_sessions(mine=True)
    assert league_data
    assert isinstance(league_data, dict)
    assert league_data['success'] == True


def test_get_directory(league_instance):
    """Test get_directory function."""
    league_data = league_instance.get_directory()
    assert league_data
    assert isinstance(league_data, dict)
    assert league_data['success'] == True


def test_get_league(league_instance):
    """Test get_league function."""
    league_data = league_instance.get_league(league_id=3580)
    assert league_data
    assert isinstance(league_data, dict)
    assert league_data['league_id'] == 3580


def test_get_points_systems(league_instance):
    """Test get_points_systems function."""
    points_systems = league_instance.get_points_systems(league_id=3580)
    assert points_systems
    assert isinstance(points_systems, dict)
    assert points_systems['success'] == True
    assert points_systems['league_id'] == 3580


def test_get_membership(league_instance):
    """Test get_membership function."""
    membership = league_instance.get_membership(cust_id=530595, include_league=False)
    assert membership
    assert isinstance(membership, list)
    assert len(membership) > 0


def test_get_seasons(league_instance):
    """Test get_seasons function."""
    seasons = league_instance.get_seasons(league_id=3580)
    assert seasons
    assert isinstance(seasons, dict)
    assert seasons['success'] == True
    assert seasons['league_id'] == 3580

def test_get_season_standings(league_instance):
    """Test get_season_standings function."""
    standings = league_instance.get_season_standings(league_id=3580, season_id=93206)
    assert standings
    assert isinstance(standings, dict)
    assert standings['success'] == True
    assert standings['league_id'] == 3580
    assert standings['season_id'] == 93206


def test_get_season_sessions(league_instance):
    """Test get_season_sessions function."""
    sessions = league_instance.get_season_sessions(league_id=3580, season_id=93206)
    assert sessions
    assert isinstance(sessions, dict)
    assert sessions['success'] == True
    assert sessions['league_id'] == 3580
    assert sessions['season_id'] == 93206
    
