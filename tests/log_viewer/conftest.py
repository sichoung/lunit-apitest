#-*- coding: utf-8 -*-
import os,sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
import json
import requests
from common import api_test_util as api_util
from common.exceptions import APITestException
from common.api_constants import LogViewerConstants as lv_constants

@pytest.fixture(scope='session')
def get_lv_token(get_lv_baseurl):
    def _data(test_email, test_pw):
        headers = {"Content-Type": "application/json"}
        payload = {
            "email": test_email,
            "password": test_pw
        }
        response = requests.post(get_lv_baseurl + lv_constants.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
        if response.status_code == 200: 
            response_body = response.json()
            return response_body.get("accessToken")
        else:
            raise APITestException("Failed to login - status_code: {}, {}".format(response.status_code, response.text))    
    return _data

@pytest.fixture(scope='session')
def prepare_testuser_gettoken(get_lv_baseurl, get_lv_token):
    """1) 요청받은 사용자 정보로 등록 시도. 
    1-1) 등록 성공하면 비번 변경 2회 하여 초기 로그인 사용자 제약 해제. 
    1-2) 이미 존재하는 사용자면 로그인 시도 """
    def _data(test_email, test_pw):
        temp_pw_to_change = "1q2w3e4r%t_chg"
        headers = {"Content-Type": "application/json"}
        payload = {
            "email": test_email,
            "password": test_pw,
            "username": "api test user"
        }
        response = requests.post(get_lv_baseurl + lv_constants.signup_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
        if response.status_code == 200:
            # 신규 추가 등록 -> 비번변경 
            response_body = response.json()
            access_token = response_body.get("accessToken")
            headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(access_token)}
            payload = {
                "currentPassword": test_pw,
                "newPassword": temp_pw_to_change,
                "email": test_email
            }
            response = requests.put(get_lv_baseurl + lv_constants.chgpw_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
            if response.status_code != 200: 
                raise APITestException("Failed to change newly added user's password - status_code: {}, {}".format(response.status_code, response.text))
            payload = {
                "currentPassword": temp_pw_to_change,
                "newPassword": test_pw,
                "email": test_email
            }
            response = requests.put(get_lv_baseurl + lv_constants.chgpw_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
            if response.status_code != 200: 
                raise APITestException("Failed to change newly added user's password - status_code: {}, {}".format(response.status_code, response.text))
            return access_token
        else: 
            # 이미 있는 사용자인 경우로 보고 로그인 시도 - '{"code":"422.1000.001","message":"Email is already in use."}'
            headers = {"Content-Type": "application/json"}
            payload = {
                "email": test_email,
                "password": test_pw
            }
            response = requests.post(get_lv_baseurl + lv_constants.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
            if response.status_code == 200: 
                response_body = response.json()
                return response_body.get("accessToken")
            else:
                raise APITestException("Failed to login - status_code: {}, {}".format(response.status_code, response.text))
    return _data

