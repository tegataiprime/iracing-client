[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=tegataiprime_iracing-client&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=tegataiprime_iracing-client)

[![CodeQL](https://github.com/tegataiprime/iracing-client/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/tegataiprime/iracing-client/actions/workflows/github-code-scanning/codeql)

[![Test Suite](https://github.com/tegataiprime/iracing-client/actions/workflows/test-suite.yaml/badge.svg)](https://github.com/tegataiprime/iracing-client/actions/workflows/test-suite.yaml)

[![Release](https://github.com/tegataiprime/iracing-client/actions/workflows/release.yaml/badge.svg)](https://github.com/tegataiprime/iracing-client/actions/workflows/release.yaml)

# iracing-client
A Python Client Library for working with iRacing Data API.

This library provides communiction & error handling with the iRacing Data API.


## Quick Start

JSON formatted data returned by iRacing is deserialized as either a `list` or `dict` using [`json.loads`](https://docs.python.org/3/library/json.html)

```python
import iracing_client.auth as auth
from iracing_client.data.constants import Constants
from iracing_client.data.member import Member
from iracing_client.data.league import League

# Authenticate with iRacing
iracing_username = os.environ.ge('IRACING_USERNAME')
iracing_password = os.environ.ge('IRACING_PASSWORD')

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
```




## Useful Information

[iRacing Data API Documentation](https://members-ng.iracing.com/data/doc)

[iRacing Forums Data API Discussion](https://forums.iracing.com/discussion/15068/general-availability-of-data-api/p1)

[iRacing Auth Portal](https://members-ng.iracing.com/auth/)

## Colaborating

Feel free to fork this repo and commit back via a Pull Request.

We have provided a VSCode devcontainer to make getting started as simple as possible.  Use your own local machine or a GitHub CodeSpace.

The python dependancies and packaging is managed using [Poetry](https://python-poetry.org/).

Tests are managed and executed using [pytest](https://docs.pytest.org/).

Code formatting is performed by [black](https://pypi.org/project/black/).

Linting is performed by [pylint](https://pypi.org/project/pylint/).

### Unit Tests

Unit Tests mock interactions with the iRacing Data API and can be executed offline.  Create unit tests to exercise logic and error handling.

Running pytest from the VSCode Terminal:
```bash
poetry run pytest tests/unit/
```

### Integration Tests

Integration Tests will connect to the iRacing Service and perform a shake down of the base data classes using live data.

When testing locally, provide the following values in a `.env` file in the root of the project.

```bash
IRACING_USERNAME=<your email address>
IRACING_PASSWORD=<your iRacing password>
IRACING_MEMBER_ID=<your iRacing Member Id>
```


Running pytest from the command line (integration tests only):
```bash
poetry run pytest tests/integration
```

