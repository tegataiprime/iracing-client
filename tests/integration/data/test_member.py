"""Test Member Module."""
import pytest
from iracing_client.data.member import Member
from iracing_client.data.constants import Category, ChartType


@pytest.fixture(scope="module")
def member_instance(http_session):
    """Return a Member object."""
    return Member(http_session)


def test_get_member(member_instance, iracing_member_id):
    """Test get_member function."""
    member_data = member_instance.get_member(cust_id=iracing_member_id)
    assert member_data
    assert isinstance(member_data, dict)
    assert member_data['success'] is True
    assert member_data['members'][0]['cust_id'] == iracing_member_id


def test_get_members(member_instance, iracing_member_id):
    """Test get_members function."""
    member_data = member_instance.get_members(cust_ids=[iracing_member_id])
    assert member_data
    assert isinstance(member_data, dict)
    assert member_data['success'] is True
    assert member_data['members'][0]['cust_id'] == iracing_member_id


def test_get_awards(member_instance, iracing_member_id):
    """Test get_awards function."""
    awards_data = member_instance.get_awards(iracing_member_id)
    assert awards_data
    assert isinstance(awards_data, list)
    assert awards_data[0]['cust_id'] == iracing_member_id


def test_get_chart_data_default_cust_id(member_instance):
   """Test get_chart_data function."""
   chart_data = member_instance.get_chart_data(
       category=Category.ROAD,
       chart_type=ChartType.IRATING)
   assert chart_data
   assert isinstance(chart_data, dict)
   assert chart_data['success'] is True


def test_get_chart_data_by_custid(member_instance, iracing_member_id):
   """Test get_chart_data_by_category function."""
   chart_data = member_instance.get_chart_data(
       category=Category.ROAD,
       chart_type=ChartType.IRATING,
       cust_id=530595)
   assert chart_data
   assert isinstance(chart_data, dict)
   assert chart_data['success'] is True
   assert chart_data['cust_id'] == iracing_member_id


def test_my_info(member_instance,iracing_member_id):
    """Test my_info function."""
    my_info = member_instance.my_info
    assert my_info
    assert isinstance(my_info, dict)
    assert my_info['cust_id'] == iracing_member_id


def test_my_participation_credits(member_instance):
    """Test my_participation_credits function."""
    my_participation_credits = member_instance.my_participation_credits
    assert isinstance(my_participation_credits, list)


def test_get_profile_default_cust_id(member_instance):
    """Test get_profile function."""
    profile = member_instance.get_profile()
    assert profile
    assert isinstance(profile, dict)
    assert profile['success'] is True


def test_get_profile_by_custid(member_instance, iracing_member_id):
    """Test get_profile function."""
    profile = member_instance.get_profile(cust_id=530595)
    assert profile
    assert isinstance(profile, dict)
    assert profile['success'] is True
    assert profile['cust_id'] == iracing_member_id