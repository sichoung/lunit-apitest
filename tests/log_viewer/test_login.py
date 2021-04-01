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

def add_user(req_path, user_email, user_pw):
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": user_email,
        "password": user_pw,
        "username": "api test user"
    }
    response = requests.post(req_path+url_manager.signup_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    if response.status_code == 200: 
        response_body = response.json()
        return response_body.get("accessToken")
    else: 
        raise APITestException("Failed to prepare test user (add new user)- "+str(response.status_code))

def test_login_basic(get_lv_baseurl):
    try:
        add_user(get_lv_baseurl, test_email, test_pw)
    except Exception:
        print("ingore")

    headers = {"Content-Type": "application/json"}
    payload = {
        "email": test_email,
        "password": test_pw
    }
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
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
        "email": test_email,
        "password": test_pw
    }
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    first_access_token = response_body["accessToken"]
    
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    second_access_token = response_body["accessToken"]

    assert first_access_token == second_access_token


def test_login_notexistid(get_lv_baseurl):
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": "not_exist_emaillll",
        "password": test_pw
    }
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 401 == response.status_code
    # '{"code":"500.0001.0005","message":"Invalid Credentials"}'
    response_body = response.json()
    assert "401.1000.001" == response_body.get("code")
    assert "Invalid credential. Email or password not correct." == response_body.get("message")
    assert "failureCount" in response_body
    assert "lockoutCount" in response_body
    assert "coolOffSeconds" in response_body

def test_login_wrongpw(get_lv_baseurl):
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": test_email,
        "password": "wrong$(!_L:pw"
    }
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 401 == response.status_code
    # '{"code":"403.1000.001","message":"User not found."}'
    response_body = response.json()
    assert "401.1000.001" == response_body.get("code")
    assert "Invalid credential. Email or password not correct." == response_body.get("message")
    assert "failureCount" in response_body
    assert "lockoutCount" in response_body
    assert "coolOffSeconds" in response_body
    
def test_login_norequiredfield(get_lv_baseurl):
    headers = {"Content-Type": "application/json"}
    payload = {
        # "password": test_id,
        "password": test_pw
    }
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 400 == response.status_code
    # JSONDecodeError('Expecting value: line 1 column 1 (char 0)')
    
    assert ""== response.text # 현재는 response.text에는 비어있고, response.json에 json이 아닌 문자열이 들어있음
    
def test_login_failmorethan3times(get_lv_baseurl):
    """ N회 이상 로그인 실패 시 60sec 대기 시간등 적용 확인 """
    # fail#1 
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": test_email,
        "password": "wrong_pwwww"
    }
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 401 == response.status_code

    # fail#2
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 401 == response.status_code

    # fail#3 
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 401 == response.status_code

    # fail#4
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 401 == response.status_code

    # try right id, pw
    payload = {
        "email": test_email,
        "password": test_pw
    }
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    print(response.status_code)
    assert 401 == response.status_code

    # wait 61sec, try right id, pw
    time.sleep(62)
    payload = {
        "email": test_email,
        "password": test_pw
    }
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    print(response.status_code)
    assert 200 == response.status_code

def temp_add_test_account():
    """ API 테스트에 사용하는 별도 계정이 없는 경우 1회성으로 생성하는 함수 
    근데... 실행하면 "대상 컴퓨터에서 연결을 거부했으므로 연결하지 못했습니다. 뜸. 따로 swagger 페이지에서 등록함;...."
    """ 
    target_url = "https://log-collector-server-dev.lunit.io"
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": test_email,
        "password": test_pw,
        "username": url_manager.test_name
    }
    response = requests.post(target_url + url_manager.signup_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    if response.status_code == 200:
        raise Exception("Failed to add test account!! - "+response.status_code)


if __name__ == '__main__':
    # 근데... 실행하면 "대상 컴퓨터에서 연결을 거부했으므로 연결하지 못했습니다. 뜸. 따로 swagger 페이지에서 등록함;...."
    temp_add_test_account()