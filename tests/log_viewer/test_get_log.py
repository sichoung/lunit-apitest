#-*- coding: utf-8 -*-
import os, sys, io
import os.path
import requests
import pytest
from datetime import datetime
from common.exceptions import APITestException
from common.api_constants import LogViewerConstants as url_manager

test_email = url_manager.test_email
test_pw = url_manager.test_pw

@pytest.fixture(scope='module')
def upload_logfile(get_lv_baseurl, get_lv_token, get_dirpath):
    time_stamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    payload = {
        "host" : "10.120.0.11:91",
        "containerId" : "qe_test",
        "file" : ("daily{}.log".format(time_stamp), open(get_dirpath + "/log_viewer/test_resource/gw_logviewertest_dailylog.log", "rb")),
    }

    response = requests.post(get_lv_baseurl + url_manager.getloglist_api_path, files=payload, headers = headers, verify = False) # = get_dirpath+'/base64_lunit_cert.cer')
    if response.status_code != 201:
        raise APITestException("Failed to upload log file - status code is not 201 "+ response.status_code)
    response_body = response.json()
    return response_body.get('objectKey')

@pytest.fixture(scope='session')
def get_logfile_idlist(get_lv_baseurl, get_lv_token):
    search_pagesize = 3
    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}
    params = {
        'size': search_pagesize
        }
    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path, headers=headers, params=params, verify = False)
    if response.status_code != 200:
        raise APITestException("Failed to list search - "+response.status_code)
    response_body = response.json()
    contents_element = response_body.get("content")
    result_list = []
    for this_record in contents_element:
        ##### 조회된 모든 데이터에 대해 검색 조건 반영됐는지 for 문 돌면서 확인 
        result_list.append(this_record.get('id'))
    if len(result_list) >0 :
        raise APITestException("Not found any data")
    else:
        return result_list


def test_getlog_basic(get_lv_baseurl, get_lv_token, get_logfile_idlist):
    """ 테스트 목적 : 로그파일 업로드 & 조회 
    """
    headers = {"Authorization": "Bearer {}".format(get_lv_token(test_email, test_pw))}

    response = requests.get(get_lv_baseurl + url_manager.getloglist_api_path + get_logfile_idlist[0], headers = headers, verify = False) # = get_dirpath+'/base64_lunit_cert.cer')

    assert 200 == response.status_code
    response_body = response.json()
    







