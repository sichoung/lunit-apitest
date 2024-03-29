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

def test_getcomponent_basic(get_lv_baseurl, prepare_testuser_gettoken):
    # headers = {"Authorization": "Bearer {}".format(get_lv_token)}
    prepare_testuser_gettoken = prepare_testuser_gettoken(test_email, test_pw)
    headers = {"Authorization": "Bearer {}".format(prepare_testuser_gettoken)}

    response = requests.get(get_lv_baseurl + url_manager.getcomponent_api_path, headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    assert len(response_body) >= 3
    assert ['BE', 'IS', 'GW'] == response_body
    # '["INSIGHT_BACKEND_MMG","INSIGHT_BACKEND_CXR","INFERENCE_SERVER","GATEWAY"]'
    

def test_getloglevel_basic(get_lv_baseurl, prepare_testuser_gettoken):
    headers = {"Authorization": "Bearer {}".format(prepare_testuser_gettoken(test_email, test_pw))}

    response = requests.get(get_lv_baseurl + url_manager.getloglevel_api_path, headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    assert len(response_body) == 4
    assert ["DEBUG","INFO","WARNING","ERROR"] == response_body
    # '["DEBUG","WARNING","ERROR","INFO","FATAL"]'

def test_getlogtype_basic(get_lv_baseurl, prepare_testuser_gettoken):
    headers = {"Authorization": "Bearer {}".format(prepare_testuser_gettoken(test_email, test_pw))}

    response = requests.get(get_lv_baseurl + url_manager.getlogtype_api_path, headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    assert len(response_body) == 2
    assert ["APP","AUDIT"] == response_body
    # '["APP","AUDIT"]'

def test_getlogstatus_basic(get_lv_baseurl, prepare_testuser_gettoken):
    headers = {"Authorization": "Bearer {}".format(prepare_testuser_gettoken(test_email, test_pw))}

    response = requests.get(get_lv_baseurl + url_manager.getlogstatus_api_path, headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    assert len(response_body) == 2
    assert ["SUCCESS", "FAIL"] == response_body

def test_getservicehost_basic(get_lv_baseurl, prepare_testuser_gettoken):
    headers = {"Authorization": "Bearer {}".format(prepare_testuser_gettoken(test_email, test_pw))}
    
    response = requests.get(get_lv_baseurl + url_manager.getservicehost_api_path, headers=headers, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    assert len(response_body) > 0

def test_lv_healthcheck(get_lv_baseurl):
    response = requests.get(get_lv_baseurl + url_manager.gethealthcheck_api_path, verify=False)
    assert 204 == response.status_code

def test_lv_settinginfo_noqueryparam(get_lv_baseurl):
        # headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    # params = {
    #     "includes":"version"
    # }
    # response = requests.get(get_lv_baseurl + url_manager.getserverinfo_api_path, params = params, verify=False)
    response = requests.get(get_lv_baseurl + url_manager.getserverinfo_api_path, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    # assert response_body["version"]
    # assert "develop" == response_body["version"]

def test_lv_settinginfo_versioninfo(get_lv_baseurl):
    # headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    params = {
        "includes":"version"
    }
    response = requests.get(get_lv_baseurl + url_manager.getserverinfo_api_path, params = params, verify=False)
    assert 200 == response.status_code
    response_body = response.json()
    assert response_body["version"]
    # assert "develop" == response_body["version"]

def test_lv_settinginfo_invalidvalue(get_lv_baseurl):
    # headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    params = {
        "includes":"invalidddd"
    }
    response = requests.get(get_lv_baseurl + url_manager.getserverinfo_api_path, params = params, verify=False)
    assert 400 == response.status_code  # 현재는 200, '{}'
    response_body = response.json()
    # assert "develop" == response_body["version"]














    