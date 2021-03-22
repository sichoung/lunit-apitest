#-*- coding: utf-8 -*-
import os, sys, io
import os.path
import requests
import pytest
from datetime import datetime
from common.api_constants import LogViewerConstants as url_manager

user_token = None
base_url = None

test_email = url_manager.test_email
test_pw = url_manager.test_pw


def test_addlog_basic(get_lv_baseurl, get_lv_token, get_dirpath):
    """ 테스트 목적 : 로그파일 업로드 & 조회 
    """
    time_stamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    payload = {
        "host" : "10.120.0.11:91",
        "containerId" : "qe_test",
        "file" : ("daily{}.log".format(time_stamp), open(get_dirpath + "/log_viewer/test_resource/gw_logviewertest_dailylog.log", "rb")),
    }

    response = requests.post(get_lv_baseurl + url_manager.getloglist_api_path, files=payload, headers = headers, verify = False) # = get_dirpath+'/base64_lunit_cert.cer')

    assert response.status_code == 201
    response_body = response.json()
    assert 'objectKey' in response_body
    assert time_stamp in response_body.get('objectKey')
    # '{"objectKey":"2021/02/25/GATEWAY/10.120.0.11:91.qe_test.GATEWAY.daily25022021_145027.log"}'
    test_objectkey = response_body.get('objectKey')


def test_addlog_nohostcontaineridinfo(get_lv_baseurl, get_lv_token, get_dirpath):
    """ 테스트 목적 : 로그파일 업로드 
    """
    time_stamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    payload = {
        "file" : ("daily{}.log".format(time_stamp), open(get_dirpath + "/log_viewer/test_resource/gw_logviewertest_dailylog.log", "rb")),
    }

    response = requests.post(get_lv_baseurl + url_manager.getloglist_api_path, files=payload, headers = headers, verify = False) # = get_dirpath+'/base64_lunit_cert.cer')

    assert response.status_code == 400
    assert '' != response.text

def test_addlog_noauth(get_lv_baseurl, get_lv_token, get_dirpath):
    """ 테스트 목적 : 로그파일 업로드 
    """
    time_stamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    # headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    payload = {
        "file" : ("daily{}.log".format(time_stamp), open(get_dirpath + "/log_viewer/test_resource/gw_logviewertest_dailylog.log", "rb")),
    }

    response = requests.post(get_lv_baseurl + url_manager.getloglist_api_path, files=payload, verify = False) # = get_dirpath+'/base64_lunit_cert.cer')

    assert response.status_code == 401
    assert '' != response.text
