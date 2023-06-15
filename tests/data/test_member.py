"""Test Member Module."""
import pytest
from iracing_web_api.data.member import Member
from iracing_web_api.data.constants import Category, ChartType


@pytest.fixture(scope="module")
def member_instance(http_session):
    """Return a Member object."""
    return Member(http_session)


def test_get_member(member_instance):
    """Test get_member function."""
    member_data = member_instance.get_member(cust_id=530595)
    assert member_data
    assert isinstance(member_data, dict)
    assert member_data['success'] == True
    assert member_data['members'][0]['cust_id'] == 530595


def test_get_members(member_instance):
    """Test get_members function."""
    member_data = member_instance.get_members(cust_ids=[530595, 516632])
    assert member_data
    assert isinstance(member_data, dict)
    assert member_data['success'] == True
    assert member_data['members'][0]['cust_id'] == 530595
    assert member_data['members'][1]['cust_id'] == 516632


def test_get_awards(member_instance):
    """Test get_awards function."""
    awards_data = member_instance.get_awards(530595)
    assert awards_data
    assert isinstance(awards_data, list)
    assert awards_data[0]['cust_id'] == 530595


def test_get_chart_data_default_cust_id(member_instance):
   """Test get_chart_data function."""
   chart_data = member_instance.get_chart_data(
       category=Category.ROAD,
       chart_type=ChartType.IRATING)
   assert chart_data
   assert isinstance(chart_data, dict)
   assert chart_data['success'] == True


def test_get_chart_data_by_custid(member_instance):
   """Test get_chart_data_by_category function."""
   chart_data = member_instance.get_chart_data(
       category=Category.ROAD,
       chart_type=ChartType.IRATING,
       cust_id=530595)
   assert chart_data
   assert isinstance(chart_data, dict)
   assert chart_data['success'] == True
   assert chart_data['cust_id'] == 530595


def test_my_info(member_instance):
    """Test my_info function."""
    my_info = member_instance.my_info
    assert my_info
    assert isinstance(my_info, dict)
    assert my_info['cust_id'] == 530595


def test_my_participation_credits(member_instance):
    """Test my_participation_credits function."""
    my_participation_credits = member_instance.my_participation_credits
    assert isinstance(my_participation_credits, list)


def test_get_profile_default_cust_id(member_instance):
    """Test get_profile function."""
    profile = member_instance.get_profile()
    assert profile
    assert isinstance(profile, dict)
    assert profile['success'] == True


def test_get_profile_by_custid(member_instance):
    """Test get_profile function."""
    profile = member_instance.get_profile(cust_id=530595)
    assert profile
    assert isinstance(profile, dict)
    assert profile['success'] == True
    assert profile['cust_id'] == 530595