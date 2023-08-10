"""Test Results Module"""
import pytest
from iracing_client.data.results import Results

@pytest.fixture(scope="module")
def results_instance(http_session):
    """Return a Results object."""
    return Results(http_session)

@pytest.fixture(scope="module")
def subsession_id():
    """Return a subsession_id."""
    return 62223513

def test_get_result(results_instance, subsession_id):
    """Test get_result function."""
    result_data = results_instance.get_result(subsession_id=subsession_id)
    assert result_data
    assert isinstance(result_data, dict)
    assert result_data['subsession_id'] == subsession_id
    assert result_data['session_results'] is not None
    assert len(result_data['session_results']) > 0

def test_get_event_log(results_instance, subsession_id):
    """Test get_event_log"""
    result_data = results_instance.get_event_log(subsession_id=subsession_id, simsession_number=0)
    assert result_data
    assert len(result_data) > 0
