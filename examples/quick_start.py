import iracing_client.auth as auth
from iracing_client.data.constants import Constants
from iracing_client.data.member import Member
from iracing_client.data.league import League

# Authenticate with iRacing
iracing_username = os.environ.ge("IRACING_USERNAME")
iracing_password = os.environ.ge("IRACING_PASSWORD")

http_session = auth.login(iracing_username, iracing_password)


# iRacing Constants
constants = Constants(http_session)
print(constants.categories)
print(constants.divisions)
print(constants.event_types)


# My iRacing Member Info
member = Member(http_session)
print(member.get_profile())


# My iRacing League Directory
league = League(http_session)
print(league_instance.get_directory())
