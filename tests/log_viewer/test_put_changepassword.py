#-*- coding: utf-8 -*-
import os,sys
import pytest

import os, sys, io
import requests
import json, time
from common import api_test_util as util
from common.exceptions import APITestException
from common.api_constants import LogViewerConstants as url_manager

#new_test_id = "test01"
new_test_email = "test04@lunit.io"
new_test_pw = "fnsltakstp123!"
new_test_pw_chg = "fnsltakstp123!_chg"

@pytest.fixture(scope="module")
def get_testuser_token(get_lv_baseurl):
    # 비번변경용 테스트 유저로 로그인 시도해서 토큰값 반환. 없는 경우 신규 등록?
    headers = {"Content-Type": "application/json"}
    payload = {
        "password": new_test_pw,
        "username": "api test user",
        "email": new_test_email
    }
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    if response.status_code == 200:
        print("prepare... login and get user token")
        response_body = response.json()
        return response_body.get("accessToken")
    else: 
        print("prepare... test user not exist. trying to add new user...")
        # 신규가입
        payload = {
            "email": new_test_email,
            "password": new_test_pw,
            "username": "api test user"
        }
        response = requests.post(get_lv_baseurl + url_manager.signup_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
        if response.status_code == 200: 
            response_body = response.json()
            return response_body.get("accessToken")
        else: 
            raise APITestException("Failed to prepare test user (add new user)- "+str(response.status_code))
    
def test_changepwd_basic(get_lv_baseurl, get_testuser_token):
    """ 테스트 목적 : 비번변경 기본 
    """
    # 비번변경
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(get_testuser_token)}
    payload = {
        "currentPassword": new_test_pw,
        "newPassword": new_test_pw_chg,
        "email": new_test_email
    }
    response = requests.put(get_lv_baseurl + url_manager.chgpw_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code #'{"code":"400.1000.001","message":"Invalid password. Password not correct."}'
    response_body = response.json()
    assert True == response_body.get("isChanged")

    # 바뀐 비번으로 로그인
    payload = {
        "password": new_test_pw_chg,
        "email": new_test_email
    }
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    access_token = response_body.get("accessToken")

    # 다시원래대로변경
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(access_token)}
    payload = {
        "currentPassword": new_test_pw_chg,
        "newPassword": new_test_pw,
        "email": new_test_email
    }
    response = requests.put(get_lv_baseurl + url_manager.chgpw_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    assert True == response_body.get("isChanged")    

def test_changepwd_invalidnewpassword(get_lv_baseurl, get_testuser_token):
    """ 테스트 목적 : 기준을 만족하지 못하는 신규비밀번호 
    """
    # 비번변경
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(get_testuser_token)}
    payload = {
        "currentPassword": new_test_pw,
        "newPassword": "test",
        "email": new_test_email
    }
    response = requests.put(get_lv_baseurl + url_manager.chgpw_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 400 == response.status_code 
    response_body = response.json()
    assert response_body.get("code") == "400.1000.001"
    assert response_body.get("message") == "Invalid password. Password not correct."


def test_changepwd_differentusertoken(get_lv_baseurl):
    """ 테스트 목적 : auth token과 다른 사용자의 비번변경 시도 
    """
    # 다른 사용자 토큰 값 가져오기 
    headers = {"Content-Type": "application/json"}
    payload = {
        "password": url_manager.test_pw,
        "email": url_manager.test_email
    }
    response = requests.post(get_lv_baseurl + url_manager.login_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert response.status_code == 200
    response_body = response.json()
    access_token = response_body.get("accessToken")

    # 비번변경
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(access_token)}
    payload = {
        "currentPassword": new_test_pw,
        "newPassword": new_test_pw_chg,
        "email": new_test_email
    }
    response = requests.put(get_lv_baseurl + url_manager.chgpw_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 400 == response.status_code #'{"code":"400.1000.001","message":"Invalid password. Password not correct."}'
    response_body = response.json()
    assert True == response_body.get("isChanged")

def test_changepwd_invalcurrentpw(get_lv_baseurl, get_testuser_token):
    """ 테스트 목적 : 틀린 현재비밀번호 
    """
    # 비번변경
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(get_testuser_token)}
    payload = {
        "currentPassword": "wrong_pw#!(OAKFLA",
        "newPassword": new_test_pw_chg,
        "email": new_test_email
    }
    response = requests.put(get_lv_baseurl + url_manager.chgpw_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code #'{"code":"400.1000.001","message":"Invalid password. Password not correct."}'
    response_body = response.json()
    assert True == response_body.get("isChanged")

def test_changepwd_samepw(get_lv_baseurl,get_testuser_token):
    """ 테스트 목적 : current, new 같은 비번
    """
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(get_testuser_token)}
    payload = {
        "currentPassword": "wrong_pw#!(OAKFLA",
        "newPassword": new_test_pw_chg,
        "email": new_test_email
    }
    response = requests.put(get_lv_baseurl + url_manager.chgpw_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code #'{"code":"400.1000.001","message":"Invalid password. Password not correct."}'
    response_body = response.json()
    assert True == response_body.get("isChanged")


def test_changepwd_nouser(get_lv_baseurl, get_testuser_token):
    """ 테스트 목적 : 존재하지 않는 사용자(email) 에 대한 비번변경 시도 
    """
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(get_testuser_token)}
    payload = {
        "currentPassword": new_test_pw,
        "newPassword": new_test_pw_chg,
        "email": "not_existtt@lunit.io"
    }
    response = requests.put(get_lv_baseurl + url_manager.chgpw_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code #'{"code":"400.1000.001","message":"Invalid password. Password not correct."}'
    response_body = response.json()
    assert True == response_body.get("isChanged")

