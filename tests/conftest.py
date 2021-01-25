import os,sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
import requests


# @pytest.fixture(autouse=True, scope='session')
# def cmd_param(pytestconfig):
#     api_version = pytestconfig.getoption("--mobile_api_ver").lower()
#     global api_url
#     if api_version in ['v24', 'v25', 'v26', 'v27']:
#         api_url = 'http://www.foobar.com/' + api_version
#     else:
#         raise ValueError('Unknown api version: ' + api_version)

# def pytest_addoption(parser):
#     parser.addoption("--api_version", action="store", default="v25", help="By default: v25")

@pytest.fixture(scope='session')
def get_gcm_mmg_baseurl():
    return 'http://10.120.0.11'

@pytest.fixture(scope='session')
def get_gcm_cxr3_baseurl():
    return 'http://10.120.0.11:91'

@pytest.fixture(scope='session')
def lv_gettoken(access_token, email_id, passwd):
    if(access_token != None):
        return access_token
    else:
        return None

@pytest.fixture(scope='session')
def lv_api_url(pytestconfig):
    return 'https://log-collector-server-dev.lunit.io'
    # api_version = pytestconfig.getoption("--api_version").lower()
    # if api_version in ['v24', 'v25', 'v26', 'v27']:
    #     return 'https://log-collector-server-dev.lunit.io' + api_version
    # else:
    #     raise ValueError('Unknown api version: ' + api_version)

@pytest.fixture(scope='module')
def get_dirpath():
    dirname = os.path.dirname(os.path.abspath(__file__))
    # base_path = dirname + '/responses'
    return dirname

