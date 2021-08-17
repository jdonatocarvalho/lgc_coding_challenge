import pytest
import requests
from config.config import COUNTRY
import pytest
from config import endpoints
from utils.basic_logger import Logger


def pytest_sessionstart(session):
    # Hook to verify API availability before starting tests execution...
    try:
        Logger.debug('Validating LGC API availability...')
        response = requests.post(endpoints.session_token('v1'))
        response.raise_for_status()
        Logger.warning('LGC Shop API is online, starting pytests execution...')
    except requests.exceptions.HTTPError as err:
        Logger.error('There is a problem with the LGC API or it is reachable')
        pytest.exit('Exiting pytest execution')


def pytest_runtest_setup(item):
    Logger.info("Starting {} execution...".format(item.name))


@pytest.fixture
def country():
    return COUNTRY