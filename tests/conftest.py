
#-*- coding: utf-8 -*-
import os,sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
import json
import requests
from common import api_test_util as api_util
from common.exceptions import APITestException

###### COMMON ######
# TODO 각 폴더별로 conftest.py를 여러개 만들어 분리
def pytest_addoption(parser):
    parser.addoption("--gw_url", action="store", default="http://10.120.0.11:91", help="Gateway test URL. By default: http://10.120.0.11:91")
    parser.addoption("--be_url", action="store", default="http://10.120.0.11:8001", help="Insight Backend test URL. By default: http://10.120.0.11:91")
    parser.addoption("--is_url", action="store", default="http://10.220.150.115:7711", help="Inference Server test URL. By default: http://10.120.0.11:91")
    parser.addoption("--lv_url", action="store", default="https://log-collector-server-dev.lunit.io", help="LogViewer server test URL. By default: not_yet_defined")
    parser.addoption('--integration', action='store_true', help='run include integration tests')

def pytest_runtest_setup(item):
  if 'integration' in item.keywords and not item.config.getoption('--integration'):
    pytest.skip('need --integration option to run')


@pytest.fixture(scope='module')
def get_dirpath():
    dirname = os.path.dirname(os.path.abspath(__file__))
    return dirname

@pytest.fixture(scope='session')
def get_lv_baseurl(pytestconfig):
    return pytestconfig.getoption("--lv_url")



        

###### GW for GCM ######
@pytest.fixture(scope='session')
def get_gcm_mmg_baseurl(get_cmd_opt):
    return 'http://10.120.0.11'

@pytest.fixture(scope='session')
def get_gcm_cxr3_baseurl(get_cmd_opt):
    return 'http://10.120.0.11:91'

###### IS ######




###### LogViewer ######





