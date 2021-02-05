#-*- coding: utf-8 -*-
import os,sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
import json
import requests
from common import api_test_util as api_util
from common.exceptions import APITestException
from common.api_constants import LogViewerConstants as APIInfo

@pytest.fixture(scope='session')
def get_lv_token(get_lv_baseurl):
    def _data(test_id, test_pw):
        headers = {"Content-Type": "application/json"}
        payload = {
            "password": test_id,
            "username": test_pw
        }
        response = requests.post(get_lv_baseurl + APIInfo.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
        if response.status_code == 200: 
            response_body = response.json()
            return response_body.get("accessToken")
        else:
            raise APITestException("Failed to login - status_code: {}, {}".format(response.status_code, response.text))    
    return _data

@pytest.fixture(scope='session')
def get_lv_logobjkey(get_lv_baseurl):
    return "2021/02/05/GATEWAY/10.120.0.11:91.qe_test.GATEWAY.daily05022021_185522.log"

