#-*- coding: utf-8 -*-
import os, sys, io
import os.path
import requests
import pytest

api_path_get_logs = '/logs'
# api_path_add_log = '/logs'
# api_path_get_log = '/logs/{id}'

user_token = None
base_url = None
# https://log-collector-server-dev.lunit.io/

@pytest.fixture
def lv_tokener():
    if user_token ==None:
        yield user_token
    else:
        print('TODO: get user token')
        yield user_token 

def test_get_logs_200(lv_api_url, lv_tokener, get_dirpath):
    response = requests.get(lv_api_url + api_path_get_logs, verify = False) # = get_dirpath+'/base64_lunit_cert.cer')
    assert response.status_code == 200
    response_body = response.json()
    assert "" == response_body["message"]

# 현재 조회시도하면 500 에러나서 추가진행 불가


def test_add_log_200(lv_api_url, lv_tokener, get_dirpath):
    # headers = {'Content-Type': 'application/json'}
    headers = {'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryY4ruG5YEGEX3yU47'}

    # Body
    with open(get_dirpath+'/sample_log.log', 'rb') as f:
        sample = bytearray(f.read())
        f.close()
    
    payload = {
        "containerId ": "pytest_automation",
        # "file" : (io.BytesIO(b"abcdef"), 'test.dcm'),
        "file" : (sample, 'test.dcm'),
        "host" : "http://10.220.150.115"
    }

    response = requests.post(lv_api_url + api_path_get_logs, data=payload, headers = headers, verify = False) # =get_dirpath+'/base64_lunit_cert.cer')
    # data=json.dumps(payload, indent=4)
    print(response.text)
    assert response.status_code == 200
    response_body = response.json()
    assert "" == response_body["message"]


def test_get_log_200(lv_api_url, lv_tokener):
    temp_id = "temp_id"
    response = requests.get(lv_api_url + api_path_get_logs+"/"+temp_id, verify = False)
    assert response.status_code == 200
    response_body = response.json()
    assert "" == response_body["message"]