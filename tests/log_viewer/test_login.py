#-*- coding: utf-8 -*-
import os,sys
import pytest

import os, sys, io
import requests
import json, time
from common import api_test_util as util
from common.api_constants import LogViewerConstants as APIInfo

test_id = "test"
test_pw = "test"

def test_login_basic(get_lv_baseurl):
    headers = {"Content-Type": "application/json"}
    payload = {
        "password": test_id,
        "username": test_pw
    }
    response = requests.post(get_lv_baseurl + APIInfo.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    assert "id" in response_body
    assert "username" in response_body
    assert "accessToken" in response_body
    assert "refreshToken" in response_body
    access_token = response_body["accessToken"]
    assert access_token != None
    # '{"id":"6019176c06cf29107efb5739","username":"test","accessToken":"eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZXN0IiwiYXV0aCI6W10sImlhdCI6MTYxMjQxMzA0NCwiZXhwIjoxNjEyNDE2NjQ0fQ.eNvfxtS7z5-KOQbfBIPpF45dkiSk-ds2Raoe1JNfb5d7-Rckptxb3xnqJFpAHfcPxOb4sroWMBG1F4TVL3tCKw","refreshToken":"eb2074744cc144ff81133029fbeee458"}'
    # assert "cxr-v3" == response_body["app"]
    # dicom_uuid = response_body["uuid"]

def test_login_twice(get_lv_baseurl):
    headers = {"Content-Type": "application/json"}
    payload = {
        "password": test_id,
        "username": test_pw
    }
    response = requests.post(get_lv_baseurl + APIInfo.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    first_access_token = response_body["accessToken"]
    
    response = requests.post(get_lv_baseurl + APIInfo.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    second_access_token = response_body["accessToken"]

    assert first_access_token == second_access_token


def test_login_notexistid(get_lv_baseurl):
    headers = {"Content-Type": "application/json"}
    payload = {
        "password": "not_exist_id",
        "username": test_pw
    }
    response = requests.post(get_lv_baseurl + APIInfo.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 500 == response.status_code
    # '{"code":"500.0001.0005","message":"Invalid Credentials"}'
    response_body = response.json()
    assert "500.0001.0005" == response_body.get("code")
    assert "Invalid Credentials" == response_body.get("message")

def test_login_wrongpw(get_lv_baseurl):
    headers = {"Content-Type": "application/json"}
    payload = {
        "password": test_id,
        "username": "wrong_pwwww"
    }
    response = requests.post(get_lv_baseurl + APIInfo.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 403 == response.status_code
    # '{"code":"403.1000.001","message":"User not found."}'
    response_body = response.json()
    assert "403.1000.001" == response_body.get("code")
    assert "User not found." == response_body.get("message")
    
def test_login_norequiredfield(get_lv_baseurl):
    headers = {"Content-Type": "application/json"}
    payload = {
        # "password": test_id,
        "username": test_pw
    }
    response = requests.post(get_lv_baseurl + APIInfo.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 400 == response.status_code
    # JSONDecodeError('Expecting value: line 1 column 1 (char 0)')
    
    assert ""== response.text # 현재는 response.text에는 비어있고, response.json에 json이 아닌 문자열이 들어있음
    
def test_login_failmorethan3times(get_lv_baseurl):
    """ N회 이상 로그인 실패 시 60sec 대기 시간등 적용 확인 """
    # fail#1 
    headers = {"Content-Type": "application/json"}
    payload = {
        "password": test_id,
        "username": "wrong_pwwww"
    }
    response = requests.post(get_lv_baseurl + APIInfo.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 403 == response.status_code

    # fail#2
    response = requests.post(get_lv_baseurl + APIInfo.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 403 == response.status_code

    # fail#3 
    response = requests.post(get_lv_baseurl + APIInfo.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 403 == response.status_code

    # fail#4
    response = requests.post(get_lv_baseurl + APIInfo.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 403 == response.status_code

    # try right id, pw
    payload = {
        "password": test_id,
        "username": test_pw
    }
    response = requests.post(get_lv_baseurl + APIInfo.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    print(response.status_code)
    assert 403 == response.status_code

    # wait 61sec, try right id, pw
    time.sleep(62)
    payload = {
        "password": test_id,
        "username": test_pw
    }
    response = requests.post(get_lv_baseurl + APIInfo.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    print(response.status_code)
    assert 403 == response.status_code

