
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


###### BE ######
@pytest.fixture(scope='session')
def get_be_baseurl(pytestconfig):
    return pytestconfig.getoption("--be_url")

@pytest.fixture(scope='package')
def get_apikey():
    # scope:package 는 패키지별로 1회 수행 후 재사용된다
    # return 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJiYWI4NzVkYS03ZWUxLTRmYzYtOTNiOC1mZWIxZDIwY2E5NzUiLCJpc3MiOiJMdW5pdCIsImlhdCI6MTYwNjExMjc4MCwiZXhwIjoxNjEzODg4NzgwLCJuYmYiOjE2MDYxMTI3ODAsImF1ZCI6Imh0dHBzOi8vaW5zaWdodC5sdW5pdC5pbyIsImRhdGEiOnsiY291bnRyeV9pZCI6MSwiY291bnRyeV9uYW1lIjoiQWZnaGFuaXN0YW4ifX0.XEmOg5ZBZiHyzhcZJRuu12J-_VxyGfbvVPWygee23qc'
    # return 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5NjFhN2NlMS1lNTY2LTQ4YmQtYWFjZS01MTg4MmQ0OGE3ODMiLCJpc3MiOiJMdW5pdCIsImlhdCI6MTYwMzY4MzMzOCwiZXhwIjoxNjE0MDUxMzM4LCJuYmYiOjE2MDM2ODMzMzgsImF1ZCI6Imh0dHBzOi8vaW5zaWdodC5sdW5pdC5pbyIsImRhdGEiOnsiY291bnRyeV9pZCI6ODIsImNvdW50cnlfbmFtZSI6IkdhbWJpYSJ9fQ.mrzdYEfT26KXl3cwaalqufJw20gZGe3UzbsI2vBZ5Bw'
    return 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxNDUxZjlkMC0xYmY5LTQyNDYtOTM0YS01ODI0NTIxZGM5ZTEiLCJpc3MiOiJMdW5pdCIsImlhdCI6MTYxMjc3MTMxNywiZXhwIjoxNjQ0MzA3MzE3LCJuYmYiOjE2MTI3NzEzMTcsImF1ZCI6Imh0dHBzOi8vaW5zaWdodC5sdW5pdC5pbyIsImRhdGEiOnsiY291bnRyeV9pZCI6MTE5LCJjb3VudHJ5X25hbWUiOiJLb3JlYSAoU291dGgpIn19.2Ob7UFBW_LpVomizK5bq7UR6W0r6zg-FUJJnE2Oh3ok'

@pytest.fixture(scope="module")
def get_dicom_uuid(get_be_baseurl, get_apikey, get_dirpath):
    # scope:module 는 module 파일별로 1회 수행 후 재사용된다
    upload_api_path = '/cxr-v3/dcm/'
    headers = {"Authorization": "Bearer "+get_apikey}
    values = {
        "file": ("normal.dcm", open(get_dirpath+"/be/normal.dcm", "rb"))
    }
    response = requests.post(get_be_baseurl + upload_api_path, files=values, headers=headers)
    if 201 != response.status_code:
        raise APITestException("Failed to upload dicom file and get uuid - {}".format(response.text))
    else:
        yield response.json()["uuid"]

@pytest.fixture(scope="module")
def get_case_uuid(get_be_baseurl, get_apikey, get_dicom_uuid):
    predict_api_path = '/cxr-v3/models/latest/predict/'
    dicom_uuid = get_dicom_uuid
    test_threshold_value = 0.25
    headers = {"Content-Type": "application/json", "Authorization": "Bearer "+get_apikey}
    payload = {
        "case": [
            {
                "dicom": dicom_uuid,
                "view_name": "frontal"
            }
        ],
        "threshold": test_threshold_value,
        "filtering": False
    }
    response = requests.post(get_be_baseurl + predict_api_path, data=json.dumps(payload,indent=4), headers=headers)
    if response.status_code != 200:
        raise APITestException("Failed to predict with {}, response{}".format(dicom_uuid,response.text))
    else:
        response_body = response.json()
        if "uuid" in response_body:
            yield response_body.get("uuid")
        else:
            raise APITestException("Failed to predict with {}, response{}".format(dicom_uuid,response.text))
        

###### GW for GCM ######
@pytest.fixture(scope='session')
def get_gcm_mmg_baseurl(get_cmd_opt):
    return 'http://10.120.0.11'

@pytest.fixture(scope='session')
def get_gcm_cxr3_baseurl(get_cmd_opt):
    return 'http://10.120.0.11:91'

###### IS ######




###### LogViewer ######





