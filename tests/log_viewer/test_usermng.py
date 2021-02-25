#-*- coding: utf-8 -*-
import os,sys
import pytest

import os, sys, io
import requests
import json, time
from common import api_test_util as util
from common.api_constants import LogViewerConstants as url_manager

new_test_id = "lunit_qe_id"
new_test_pw = "lunit_qe_pw"
new_test_pw_chg = "lunit_qe_pw_chg"

# new_test_pw = "lunit_qe_pw_chg"
# new_test_pw_chg = "lunit_qe_pw"

def test_useraccount_flow001(get_lv_baseurl):
    """ Flow Test Scenario - 001
    1) 신규가입 
    2) 신규 가입 정보로 로그인
    3) 비번변경
    4) 바뀐 비번으로 로그인 
    5) 다시 원래대로 변경
    6) 토큰 밸리드 확인
    7) 리프레시 토큰
    8) 새로 받은 토큰 밸리드
    """
    headers = {"Content-Type": "application/json"}
    # 신규가입
    # payload = {
    #     "email": new_test_id + "@lunit.io",
    #     "password": new_test_pw,
    #     "username": new_test_id
    # }
    # response = requests.post(get_lv_baseurl + signup_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    # assert 200 == response.status_code
    # # '{"id":"601ba9d406cf29107efb573a","username":"lunit_qe_id","accessToken":"eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJsdW5pdF9xZV9pZCIsImF1dGgiOltdLCJpYXQiOjE2MTI0MjU2ODQsImV4cCI6MTYxMjQyOTI4NH0.qUY8aHKh36xn-TnMEQswEVB_4ZfhK79F4uO6R3_-GmkDbC-pI97_g-q4vFM6RNX4Bfu4tCx74HSyq1E_wAvXdA","refreshToken":"a5bbf99b4040430baac32e3f19db20e2"}'
    # response_body = response.json()
    # assert "id" in response_body
    # assert "accessToken" in response_body
    # assert "refreshToken" in response_body
    # assert new_test_id ==  response_body.get("username")
    
    # print(response.status_code)
    # print(response.text)
    # 로그인
    payload = {
        "password": new_test_pw,
        "username": new_test_id,
        "email": new_test_id+"@lunit.io"
    }
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    access_token = response_body.get("accessToken")
    refresh_token = response_body.get("refreshToken")

    # 비번변경
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(access_token)}
    payload = {
        "currentPassword": new_test_pw,
        "newPassword": new_test_pw_chg,
        "username": new_test_id
    }
    response = requests.put(get_lv_baseurl + url_manager.chgpw_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    assert True == response_body.get("isChanged")

    # 바뀐 비번으로 로그인
    payload = {
        "password": new_test_pw_chg,
        "username": new_test_id
    }
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    access_token = response_body.get("accessToken")
    refresh_token = response_body.get("refreshToken")

    # 다시원래대로변경
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(access_token)}
    payload = {
        "currentPassword": new_test_pw_chg,
        "newPassword": new_test_pw,
        "username": new_test_id
    }
    response = requests.put(get_lv_baseurl + url_manager.chgpw_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    assert True == response_body.get("isChanged")

    # 토큰 밸리드
    headers = {"Content-Type": "application/json"}
    payload = {
        "token": access_token
    }
    response = requests.post(get_lv_baseurl + url_manager.verifytkn_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    assert True == response_body.get("isVerify")

    # invalid 토큰 확인
    headers = {"Content-Type": "application/json"}
    payload = {
        "token": "faskjfqjroiqwefnasdfaosf;ij49-09123o12ofasjlskafasdfasdfa"
    }
    response = requests.post(get_lv_baseurl + url_manager.verifytkn_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json() 
    assert False == response_body.get("isVerify")

    # 리프레시 잘못된 값 , 리프레스 토큰
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(access_token)}
    payload = {
        "token": access_token
    }
    response = requests.post(get_lv_baseurl + url_manager.refreshtkn_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    # assert 200 == response.status_code
    response_body = response.json() # '{"code":"500.1000.004","message":"Refresh Token expired or invalid."}'
    # new_access_token = response_body.get("accessToken")
    # new_refresh_token = response_body.get("refreshToken")

    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(access_token)}
    payload = {
        "token": refresh_token
    }
    response = requests.post(get_lv_baseurl + url_manager.refreshtkn_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json() # '{"id":"601ba9d406cf29107efb573a","username":"lunit_qe_id","accessToken":"eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJsdW5pdF9xZV9pZCIsImF1dGgiOltdLCJpYXQiOjE2MTI0Mjk3ODYsImV4cCI6MTYxMjQzMzM4Nn0.KbXq2rmwdJO7dAMXE_bRRT0l_jpEkkBlL3_Rf8wiwvpe7qoH9vK_sAm8p-vqzVlWBu1rtxfe5bWEYFQsK_ZOMA","refreshToken":"7872341ea4cc446d94d2c0d92306db2b"}'
    new_access_token = response_body.get("accessToken")
    new_refresh_token = response_body.get("refreshToken")

    # 토큰 밸리드 기존, 신규
    # headers = {"Content-Type": "application/json"}
    # payload = {
    #     "token": access_token
    # }
    # response = requests.post(get_lv_baseurl + verifytkn_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    # assert 200 == response.status_code
    # response_body = response.json()
    # assert False == response_body.get("isVerify")

    headers = {"Content-Type": "application/json"}
    payload = {
        "token": new_access_token
    }
    response = requests.post(get_lv_baseurl + url_manager.verifytkn_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    assert True == response_body.get("isVerify")
    
















    