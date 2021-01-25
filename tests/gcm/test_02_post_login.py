#-*- coding: utf-8 -*-
import os
import sys
import io
import os.path
import requests
import pytest
import json
import time

this_api_path = '/gcm/auth/login/'
email_id = 'test@lunit.io'
test_pw = '1q2w3e4r%t'


def test_login_200ok(get_gcm_cxr3_baseurl):
    headers = {'Content-Type': 'application/json'}
    # Body
    payload = {'email': email_id, 'password': test_pw}

    response = requests.post(get_gcm_cxr3_baseurl + this_api_path,
                             headers=headers, data=json.dumps(payload, indent=4))

    assert 200 == response.status_code
    print(response.text)
    response_body = response.json()
    assert response_body["name"] != None
    assert response_body["key"] != None
    assert response_body["is_initial_password"] != None

def test_login_wrongpasswd(get_gcm_cxr3_baseurl):
    headers = {'Content-Type': 'application/json'}
    # Body
    payload = {'email': email_id, 'password': 'invalid_pwwwwwwww'}

    response = requests.post(get_gcm_cxr3_baseurl + this_api_path,
                             headers=headers, data=json.dumps(payload, indent=4))

    assert 400 == response.status_code
    print(response.text)
    response_body = response.json()


def test_login_notexistid(get_gcm_cxr3_baseurl):
    headers = {'Content-Type': 'application/json'}
    # Body
    payload = {'email': 'wrong_iddd', 'password': test_pw}

    response = requests.post(get_gcm_cxr3_baseurl + this_api_path,
                             headers=headers, data=json.dumps(payload, indent=4))

    assert 400 == response.status_code
    print(response.text)
    response_body = response.json()


def test_login_invalidbody(get_gcm_cxr3_baseurl):
    headers = {'Content-Type': 'application/json'}
    # Body
    payload = {'email': 'wrong_iddd'}

    response = requests.post(get_gcm_cxr3_baseurl + this_api_path,
                             headers=headers, data=json.dumps(payload, indent=4))

    assert 400 == response.status_code
    print(response.text)
    response_body = response.json()
    

def test_login_3timeswrongpw(get_gcm_cxr3_baseurl):
    headers = {'Content-Type': 'application/json'}
    # Body
    payload = {'email': email_id, 'password': 'invalid_pwwwwwwww'}

    # 1st fail
    response = requests.post(get_gcm_cxr3_baseurl + this_api_path,
                             headers=headers, data=json.dumps(payload, indent=4))
    assert 400 == response.status_code
    response_body = response.json()
    assert response_body["message"] != None
    assert response_body["failure_count"] != None
    assert "login failed" == response_body["message"]
    
    # 2nd fail
    response = requests.post(get_gcm_cxr3_baseurl + this_api_path,
                             headers=headers, data=json.dumps(payload, indent=4))
    assert 400 == response.status_code
    assert response_body["message"] != None
    assert response_body["failure_count"] != None
    assert response_body["lockout_count"] != None
    assert "login failed" == response_body["message"]
    
    # 3rd fail
    response = requests.post(get_gcm_cxr3_baseurl + this_api_path, headers=headers, data=json.dumps(payload, indent=4))
    assert 400 == response.status_code

    # 4 right password try - fail because of the cool off time
    payload = {'email': email_id, 'password': test_pw}

    response = requests.post(get_gcm_cxr3_baseurl + this_api_path, headers=headers, data=json.dumps(payload, indent=4))
    print(response.text)
    assert 403 == response.status_code

    time.sleep(61)
    response = requests.post(get_gcm_cxr3_baseurl + this_api_path, headers=headers, data=json.dumps(payload, indent=4))

    assert 200 == response.status_code




