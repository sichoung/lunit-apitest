#-*- coding: utf-8 -*-
import os,sys
import pytest

import os, sys, io
import requests
import json, time
from common import api_test_util as util
from common.api_constants import LogViewerConstants as url_manager

test_email = url_manager.test_email
test_pw = url_manager.test_pw

def test_verifytoken_basic(get_lv_baseurl, prepare_testuser_gettoken):
    prepare_testuser_gettoken = prepare_testuser_gettoken(test_email, test_pw)
    headers = {"Content-Type": "application/json"}
    payload = {
        "token": prepare_testuser_gettoken
    }
    response = requests.post(get_lv_baseurl + url_manager.verifytkn_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    assert True == response_body.get("isVerify")


def test_verifytoken_invalidtoken(get_lv_baseurl):
    headers = {"Content-Type": "application/json"}
    payload = {
        "token": "invalidaaatokenfjasdflsjdkflasdjflasdfklasjdfljasd"
    }
    response = requests.post(get_lv_baseurl + url_manager.verifytkn_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    assert False == response_body.get("isVerify")

    
def test_verifytoken_invalidbody(get_lv_baseurl, prepare_testuser_gettoken):
    prepare_testuser_gettoken = prepare_testuser_gettoken(test_email, test_pw)
    headers = {"Content-Type": "application/json"}
    payload = {
        "access_token": prepare_testuser_gettoken
    }
    response = requests.post(get_lv_baseurl + url_manager.verifytkn_api_path, data=json.dumps(payload,indent=4), headers=headers, verify=False)
    assert 400 == response.status_code
    assert '' != response.text, "400 Bad Request에서 응답바디 내용이 존재하지 않음"
    # response_body = response.json()
    # TODO check body message 

    
















    