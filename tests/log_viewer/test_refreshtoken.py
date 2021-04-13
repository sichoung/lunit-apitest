#-*- coding: utf-8 -*-
import os,sys
import pytest

import os, sys, io
import requests
import json, time
from common import api_test_util as util
from common.exceptions import APITestException
from common.api_constants import LogViewerConstants as url_manager


test_email = url_manager.test_email
test_pw = url_manager.test_pw

def test_refreshtoken_basic(get_lv_baseurl):
    # 1)로그인
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": test_email,
        "password": test_pw
    }
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert response.status_code == 200, response.text
    response_body = response.json()
    first_access_token = response_body.get("accessToken")
    first_refresh_token = response_body.get("refreshToken")

    time.sleep(5)
    # 2)두번째 로그인한 후 처음 access_token 값과 비교. 
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": test_email,
        "password": test_pw
    }
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert response.status_code == 200, response.text
    response_body = response.json()
    second_access_token = response_body.get("accessToken")
    second_refresh_token = response_body.get("refreshToken")
    # assert first_access_token != second_access_token
    print(f"first_access_token= {first_access_token} and \nsecond_access_token= {second_access_token}")

    time.sleep(5)
    # 3) 리프레시 
    # headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(access_token)}
    headers = {"Content-Type": "application/json"}
    payload = {
        "token": second_refresh_token
    }
    response = requests.post(get_lv_baseurl + url_manager.refreshtkn_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    new_access_token = response_body.get("accessToken")
    new_refresh_token = response_body.get("refreshToken")
    assert new_access_token != None
    assert new_refresh_token != None
    assert first_access_token != new_access_token, "리프레시 된 access_token이 기존 처음 로그인시 access_token 값과 동일합니다!"
    assert second_access_token != new_access_token, "리프레시 된 access_token이 기존 두번째 로그인시 access_token 값과 동일합니다!"

    # 3) 이전 accessToken verify
    old_token_verify = verify_token(get_lv_baseurl + url_manager.verifytkn_api_path, first_access_token)
    new_token_verify = verify_token(get_lv_baseurl + url_manager.verifytkn_api_path, new_access_token)
    # 2021.03.23 요건 추가 확인. 
    assert old_token_verify == True, "old token should be invalid, but was verify returned 'True'"
    assert new_token_verify == True
    time.sleep(80)
    assert old_token_verify == False, "old token should be invalid, but was verify returned 'True'"


def test_refreshtoken_invalidrefreshtoken(get_lv_baseurl):
    # 2) 리프레시 
    headers = {"Content-Type": "application/json"}
    payload = {
        "token": "invalid____token____313890123iopk123lm123asdfjkl"
    }
    response = requests.post(get_lv_baseurl + url_manager.refreshtkn_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 500 == response.status_code
    response_body = response.json()
    assert response_body.get("code") == "500.1000.004"
    assert response_body.get("message") == "Refresh Token expired or invalid."


def verify_token(url_and_path, token_to_check):
    headers = {"Content-Type": "application/json"}
    payload = {
        "token": token_to_check
    }
    response = requests.post(url_and_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    if 200 == response.status_code:
        response_body = response.json()
        return response_body.get("isVerify")
    else:
        raise APITestException("Failed to check token - status_code : {}, {}".format(response.status_code, response.text))
        

