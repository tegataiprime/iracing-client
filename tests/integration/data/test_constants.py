"""Test constants module."""
from iracing_client.data.constants import Constants

def test_get_categories(http_session):
    """Test get_categories function."""
    constants = Constants(http_session)
    categories = constants.categories
    assert categories
    assert isinstance(categories, list)
    assert (len(categories) == 4)

def test_get_divisions(http_session):
    """Test get_divisions function."""
    constants = Constants(http_session)
    divisions = constants.divisions
    assert divisions
    assert isinstance(divisions, list)
    assert (len(divisions) > 0)

def test_get_event_types(http_session):
    """Test get_event_types function."""
    constants = Constants(http_session)
    event_types = constants.event_types
    assert event_types
    assert isinstance(event_types, list)
    assert (len(event_types) > 0)