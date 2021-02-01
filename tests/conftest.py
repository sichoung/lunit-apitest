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



###### COMMON ######
def pytest_addoption(parser):
    parser.addoption("--gw_url", action="store", default="http://10.120.0.11:91", help="Gateway test URL. By default: http://10.120.0.11:91")
    parser.addoption("--be_url", action="store", default="http://10.120.0.11:8001", help="Insight Backend test URL. By default: http://10.120.0.11:91")
    parser.addoption("--is_url", action="store", default="http://10.220.150.115:7711", help="Inference Server test URL. By default: http://10.120.0.11:91")
    parser.addoption("--lv_url", action="store", default="not_yet_defined", help="LogViewer server test URL. By default: not_yet_defined")
    parser.addoption('--integration', action='store_true', help='run include integration tests')

def pytest_runtest_setup(item):
  if 'integration' in item.keywords and not item.config.getoption('--integration'):
    pytest.skip('need --integration option to run')


@pytest.fixture(scope='module')
def get_dirpath():
    dirname = os.path.dirname(os.path.abspath(__file__))
    return dirname

###### BE ######
@pytest.fixture(scope='session')
def get_be_baseurl(pytestconfig):
    return pytestconfig.getoption("--be_url")

@pytest.fixture(scope='package')
def get_apikey():
    # TODO: test mode & diff api key
    # return 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJiYWI4NzVkYS03ZWUxLTRmYzYtOTNiOC1mZWIxZDIwY2E5NzUiLCJpc3MiOiJMdW5pdCIsImlhdCI6MTYwNjExMjc4MCwiZXhwIjoxNjEzODg4NzgwLCJuYmYiOjE2MDYxMTI3ODAsImF1ZCI6Imh0dHBzOi8vaW5zaWdodC5sdW5pdC5pbyIsImRhdGEiOnsiY291bnRyeV9pZCI6MSwiY291bnRyeV9uYW1lIjoiQWZnaGFuaXN0YW4ifX0.XEmOg5ZBZiHyzhcZJRuu12J-_VxyGfbvVPWygee23qc'
    return 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5NjFhN2NlMS1lNTY2LTQ4YmQtYWFjZS01MTg4MmQ0OGE3ODMiLCJpc3MiOiJMdW5pdCIsImlhdCI6MTYwMzY4MzMzOCwiZXhwIjoxNjE0MDUxMzM4LCJuYmYiOjE2MDM2ODMzMzgsImF1ZCI6Imh0dHBzOi8vaW5zaWdodC5sdW5pdC5pbyIsImRhdGEiOnsiY291bnRyeV9pZCI6ODIsImNvdW50cnlfbmFtZSI6IkdhbWJpYSJ9fQ.mrzdYEfT26KXl3cwaalqufJw20gZGe3UzbsI2vBZ5Bw'


###### GW for GCM ######
@pytest.fixture(scope='session')
def get_gcm_mmg_baseurl(get_cmd_opt):
    return 'http://10.120.0.11'

@pytest.fixture(scope='session')
def get_gcm_cxr3_baseurl(get_cmd_opt):
    return 'http://10.120.0.11:91'

###### IS ######




###### LogViewer ######
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





