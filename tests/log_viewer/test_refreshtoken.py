#-*- coding: utf-8 -*-
import os,sys
import pytest

import os, sys, io
import requests
import json, time
from common import api_test_util as util
from common.exceptions import APITestException
from common.api_constants import LogViewerConstants as url_manager


test_email = "test@lunit.io"
test_pw = "test"

def test_refreshtoken_basic(get_lv_baseurl):
    # 1)로그인
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": test_email,
        "password": test_pw
    }
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert response.status_code == 200
    response_body = response.json()
    access_token = response_body.get("accessToken")
    refresh_token = response_body.get("refreshToken")
    # 2) 리프레시 
    # headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(access_token)}
    headers = {"Content-Type": "application/json"}
    payload = {
        "token": refresh_token
    }
    response = requests.post(get_lv_baseurl + url_manager.refreshtkn_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    new_access_token = response_body.get("accessToken")
    new_refresh_token = response_body.get("refreshToken")
    assert new_access_token != None
    assert new_refresh_token != None

    # 3) 이전 accessToken verify
    old_token_verify = verify_token(get_lv_baseurl + url_manager.verifytkn_api_path, access_token)
    assert old_token_verify == False


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
        

